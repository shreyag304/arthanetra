"""
GovScheme Navigator Agent:
1. Checks user financial profile from user_financial_profile.
2. Evaluates eligibility rules against curated govt_schemes table:
   (e.g., PM-KISAN requires age >= 18, owns land, not tax payer;
    PM SVANidhi matches gig delivery partners & micro-vendors).
3. Saves qualified matches into user_scheme_matches table.
4. Generates step-by-step actionable application guides and document checklists in the user's language using LLM.
"""
from typing import Optional, Dict, Any, List
from sqlmodel import Session, select
from dbmodel.models import GovtScheme, UserSchemeMatch, UserFinancialProfile, User
from services.seed_schemes import seed_schemes_if_empty
from services.llm_service import llm_client


def match_schemes_for_user(session: Session, user_id: int) -> List[Dict[str, Any]]:
    seed_schemes_if_empty(session)

    profile = session.exec(
        select(UserFinancialProfile).where(UserFinancialProfile.user_id == user_id)
    ).first()
    user = session.exec(select(User).where(User.id == user_id)).first()

    schemes = session.exec(select(GovtScheme)).all()
    matched = []

    user_occ = (profile.occupation if profile and profile.occupation else (user.persona if user and user.persona else "")).lower()
    user_age = (profile.age if profile and profile.age else 25)
    owns_land = (profile.owns_land if profile and profile.owns_land is not None else False)
    is_tax_payer = (profile.is_tax_payer if profile and profile.is_tax_payer is not None else False)
    monthly_income = (profile.monthly_income if profile and profile.monthly_income else 20000.0)
    annual_income = monthly_income * 12

    for s in schemes:
        is_eligible = True
        reasons = []

        # Age criteria
        if s.min_age and user_age < s.min_age:
            is_eligible = False
            continue
        if s.max_age and user_age > s.max_age:
            is_eligible = False
            continue

        # Land criteria (e.g. PM-KISAN)
        if s.requires_land and not owns_land:
            is_eligible = False
            continue
        elif s.requires_land and owns_land:
            reasons.append("Eligible landholder")

        # Income ceiling
        if s.max_income and annual_income > s.max_income:
            is_eligible = False
            continue

        # Occupation match
        target_occs = [t.strip().lower() for t in (s.target_occupations or "").split(",") if t.strip()]
        if "all" in target_occs:
            reasons.append("Universal eligibility")
        elif target_occs and user_occ:
            if any(t in user_occ or user_occ in t for t in target_occs):
                reasons.append(f"Direct occupation match for '{user_occ}'")
            else:
                # If target occupations specified and no match, skip
                is_eligible = False
                continue
        elif target_occs and not user_occ:
            reasons.append("General public eligibility")

        if is_eligible:
            match_reason = "; ".join(reasons) if reasons else "Meets demographic and economic criteria"
            matched.append({
                "scheme": s,
                "reason": match_reason
            })

    return matched


def execute_scheme_navigator(session: Session, user_id: int, message: str, preferred_language: str = "English") -> Dict[str, Any]:
    matched_items = match_schemes_for_user(session, user_id)

    if not matched_items:
        return {
            "matched_schemes": [],
            "reply": (
                "Currently, no specific specialized scheme matched your exact profile filters, "
                "but you remain universally eligible for **Pradhan Mantri Jan Dhan Yojana (PMJDY)** zero-balance banking and accidental cover."
            ),
            "source_notice": "Curated local dataset used for offline reliability. Production can integrate API Setu for live government scheme feeds."
        }

    # Format guide with LLM
    scheme_names = [m["scheme"].scheme_name for m in matched_items]
    top_matches = matched_items[:3]

    # Save to user_scheme_matches table
    for m in top_matches:
        s = m["scheme"]
        existing = session.exec(
            select(UserSchemeMatch)
            .where(UserSchemeMatch.user_id == user_id)
            .where(UserSchemeMatch.scheme_id == s.scheme_id)
        ).first()

        if not existing:
            match_record = UserSchemeMatch(
                user_id=user_id,
                scheme_id=s.scheme_id,
                scheme_name=s.scheme_name,
                match_reason=m["reason"],
                step_by_step_guide=f"Apply online via official portal with Aadhaar and bank details for {s.benefits}"
            )
            session.add(match_record)
    session.commit()

    # Automatically trigger math-based FHS recalculation when schemes are matched
    try:
        from services.fhs_engine import recalculate_and_store_fhs
        recalculate_and_store_fhs(session, user_id)
    except Exception as fhs_err:
        print(f"[GovScheme] Could not auto-recalculate FHS: {fhs_err}")


    # Build clean, structured scheme cards directly from verified database records
    scheme_cards = []
    for idx, m in enumerate(top_matches, 1):
        s = m["scheme"]
        # Determine quick application portal/step
        if "svanidhi" in s.scheme_name.lower():
            apply_step = "Apply online at **pmsvanidhi.mohua.gov.in** or visit your nearest Common Service Centre (CSC) or local bank branch."
        elif "shram" in s.scheme_name.lower():
            apply_step = "Self-register free in 5 minutes at **eshram.gov.in** or visit a CSC center."
        elif "atal" in s.scheme_name.lower() or "apy" in s.scheme_name.lower():
            apply_step = "Submit the APY registration form at any public or private sector bank where you hold a savings account."
        elif "jan dhan" in s.scheme_name.lower() or "pmjdy" in s.scheme_name.lower():
            apply_step = "Walk into any bank branch or Bank Mitra kiosk with Aadhaar and 2 photos to open a zero-balance account."
        elif "kisan" in s.scheme_name.lower():
            apply_step = "Register online at **pmkisan.gov.in** under 'Farmer Corner' with Aadhaar and land record (Khasra)."
        elif "mudra" in s.scheme_name.lower():
            apply_step = "Apply online via **udyamimitra.in** or visit your lending bank with quotation & business plan."
        else:
            apply_step = "Apply at your nearest Common Service Center (CSC) or through the official state welfare portal."

        card = (
            f"**{idx}. {s.scheme_name}**\n"
            f"• **What you get:** {s.benefits}\n"
            f"• **Documents you'll need:** {s.required_documents}\n"
            f"• **How to apply:** {apply_step}"
        )
        scheme_cards.append(card)

    structured_content = "\n\n".join(scheme_cards)

    full_reply = (
        f"Based on your profile, here are the top schemes you're eligible for:\n\n"
        f"{structured_content}\n\n"
        f"💡 **Helpful Tip:** I recommend starting with the one that gives immediate benefits (like **e-Shram** for free insurance or **PM SVANidhi** for quick working credit)."
    )

    return {
        "matched_schemes": scheme_names,
        "reply": full_reply,
        "source_notice": "Curated database of verified central government schemes."
    }

