"""
Context Profiling Agent:
Collects information about user which is used throughout the system.
Triggers when user first interacts with system or profile is incomplete.
Asks structured questions (occupation, preferred language, financial goals, income).
Stores data in user_financial_profile table and synchronizes User table.
DOES NOT USE LLM as it performs only structured data collection and storage tasks.
"""
import re
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from sqlmodel import Session, select
from dbmodel.models import User, UserFinancialProfile


def get_or_create_profile(session: Session, user_id: int) -> UserFinancialProfile:
    profile = session.exec(
        select(UserFinancialProfile).where(UserFinancialProfile.user_id == user_id)
    ).first()
    if not profile:
        user = session.exec(select(User).where(User.id == user_id)).first()
        lang = user.language if user and user.language else "English"
        profile = UserFinancialProfile(
            user_id=user_id,
            preferred_language=lang,
            next_question="occupation",
            profile_completed=False,
        )
        session.add(profile)
        session.commit()
        session.refresh(profile)
    return profile


def extract_profile_data(text: str) -> Dict[str, Any]:
    """
    Structured rule-based entity extraction without LLM.
    """
    text_lower = text.lower()
    data: Dict[str, Any] = {}

    # 1. Occupation extraction (including common mobile typos like dilevry / dilver / omato)
    occupation_patterns = [
        (r"\b(?:delivery|dilevry|dilver|delivry|delievry|delivrey|deliveri)\s*(?:girl|boy|partner|agent|rider)?\b|\b(?:omato|zomato|swiggy|zepto|blinkit|uber\s*eats)\b", "Delivery Partner (Gig Economy)", "Gig Worker", "Variable"),
        (r"\b(driver|auto|cab|uber|ola)\b", "Commercial Driver (Gig Economy)", "Gig Worker", "Variable"),
        (r"\b(farmer|kisan|cultivator|farming)\b", "Agricultural Farmer", "Farmer", "Seasonal"),
        (r"\b(street\s*vendor|vendor|hawker|stall|shopkeeper|kirana|merchant)\b", "Small Vendor / Shopkeeper", "Micro-Entrepreneur", "Daily / Variable"),
        (r"\b(student|studying|college|school)\b", "Student", "Student", "Pocket / Allowance"),
        (r"\b(software|engineer|developer|it|coder)\b", "Software Professional", "Salaried", "Fixed Monthly"),
        (r"\b(teacher|tutor|professor)\b", "Educator", "Salaried", "Fixed Monthly"),
        (r"\b(nurse|doctor|healthcare)\b", "Healthcare Worker", "Salaried", "Fixed Monthly"),
        (r"\b(homemaker|housewife)\b", "Homemaker", "Homemaker", "Household"),
        (r"\b(freelance|designer|writer)\b", "Independent Freelancer", "Freelancer", "Variable"),
    ]

    for pat, occ, persona, inc_type in occupation_patterns:
        if re.search(pat, text_lower):
            data["occupation"] = occ
            data["persona"] = persona
            data["income_type"] = inc_type
            break

    # If user explicitly states "my occupation is X" or "i work as X"
    if "occupation" not in data:
        m = re.search(r"(?:occupation\s*(?:is|:)|i\s*work\s*as\s*(?:a|an)?|i\s*am\s*(?:a|an)?)\s*([a-zA-Z\s]{3,30})", text_lower)
        if m:
            raw_occ = m.group(1).strip()
            # Clean unwanted suffix words
            raw_occ = re.sub(r"\b(and|my|what|is|now|then)\b.*$", "", raw_occ).strip()
            if len(raw_occ) >= 3 and not any(w in raw_occ for w in ["happy", "user", "asking", "fine", "good"]):
                data["occupation"] = raw_occ.title()
                data["persona"] = raw_occ.title()
                data["income_type"] = "Variable"

    # 2. Preferred Language extraction
    lang_map = {
        "hindi": "Hindi",
        "english": "English",
        "marathi": "Marathi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "bengali": "Bengali",
        "gujarati": "Gujarati",
        "kannada": "Kannada",
        "malayalam": "Malayalam",
        "punjabi": "Punjabi"
    }
    for k, v in lang_map.items():
        if re.search(rf"\b{k}\b", text_lower):
            data["preferred_language"] = v
            break

    # 3. Financial goals extraction
    goal_patterns = [
        (r"\b(?:save|saving|savings|deposit)\b", "Increase Monthly Savings"),
        (r"\b(?:emergency\s*fund|rainy\s*day|reserve)\b", "Build Emergency Reserve"),
        (r"\b(?:loan|borrow|debt|emi|clear\s*debt)\b", "Debt Management & Micro-Credit"),
        (r"\b(?:invest|mutual\s*fund|sip|gold|fd)\b", "Long-term Wealth & Investment"),
        (r"\b(?:scheme|subsidy|govt|government\s*aid)\b", "Avail Government Welfare Schemes"),
        (r"\b(?:buy\s*bike|buy\s*car|vehicle|purchase)\b", "Asset Acquisition (Vehicle/Tools)"),
    ]
    for pat, g in goal_patterns:
        if re.search(pat, text_lower):
            data["financial_goals"] = g
            break

    # 4. Monthly income extraction
    inc_m = re.search(r"(?:income|salary|earn|earning|monthly)?\s*(?:is|of|around)?\s*(?:rs\.?|inr|₹)?\s*(\d{1,3}(?:,\d{3})+|\d+)\s*(k|thousand|lakh)?", text_lower)
    if inc_m:
        raw_val = inc_m.group(1).replace(",", "")
        multiplier = inc_m.group(2)
        try:
            val = float(raw_val)
            if multiplier in ["k", "thousand"]:
                val *= 1000
            elif multiplier == "lakh":
                val *= 100000
            if 2000 <= val <= 2000000:
                data["monthly_income"] = val
        except ValueError:
            pass

    # 5. Land ownership
    if re.search(r"\b(?:own\s*land|have\s*land|khet|zameen)\b", text_lower) and not re.search(r"\b(?:no\s*land|don't\s*own|dont\s*own)\b", text_lower):
        data["owns_land"] = True
    elif re.search(r"\b(?:no\s*land|landless|don't\s*own\s*land|dont\s*own\s*land)\b", text_lower):
        data["owns_land"] = False

    return data


def process_profiling_turn(session: Session, user_id: int, message: str) -> Tuple[str, Dict[str, Any], bool]:
    """
    Executes a turn of the Context Profiling Agent.
    Returns: (reply_text, context_dict, is_completed)
    """
    profile = get_or_create_profile(session, user_id)
    user = session.exec(select(User).where(User.id == user_id)).first()

    extracted = extract_profile_data(message)

    # Update profile fields if found
    updated = False
    if "occupation" in extracted and extracted["occupation"]:
        profile.occupation = extracted["occupation"]
        if user:
            user.persona = extracted.get("persona", profile.occupation)
            user.income_type = extracted.get("income_type", "Variable")
        updated = True

    if "preferred_language" in extracted and extracted["preferred_language"]:
        profile.preferred_language = extracted["preferred_language"]
        if user:
            user.language = extracted["preferred_language"]
        updated = True

    if "financial_goals" in extracted and extracted["financial_goals"]:
        profile.financial_goals = extracted["financial_goals"]
        if user:
            user.goal = extracted["financial_goals"]
        updated = True

    if "monthly_income" in extracted and extracted["monthly_income"]:
        profile.monthly_income = extracted["monthly_income"]
        updated = True

    if "owns_land" in extracted:
        profile.owns_land = extracted["owns_land"]
        updated = True

    # Advance state machine
    if not profile.occupation:
        profile.next_question = "occupation"
    elif not profile.preferred_language:
        profile.next_question = "language"
    elif not profile.financial_goals:
        profile.next_question = "financial_goals"
    elif not profile.monthly_income:
        profile.next_question = "monthly_income"
    else:
        profile.profile_completed = True
        profile.next_question = "complete"

    profile.updated_at = datetime.utcnow()
    session.add(profile)
    if user:
        session.add(user)
    session.commit()
    session.refresh(profile)
    if user:
        session.refresh(user)

    # Recalculate deterministic math-based Financial Health Score on profile update
    try:
        from services.fhs_engine import recalculate_and_store_fhs
        fhs_data = recalculate_and_store_fhs(session, user_id)
        current_health_score = int(fhs_data["final_fhs"])
    except Exception:
        current_health_score = user.financial_health_score if user else 75


    context_dict = {
        "persona": user.persona if user and user.persona else (profile.occupation or "Standard User"),
        "income_type": user.income_type if user and user.income_type else "Variable",
        "goal": user.goal if user and user.goal else (profile.financial_goals or "Budget Optimization"),
        "language": profile.preferred_language or "English",
        "financial_health_score": user.financial_health_score if user else 75,
        "eligible_schemes": ["PM SVANidhi", "e-Shram Card", "PM Jan Dhan Yojana"] if "delivery" in (profile.occupation or "").lower() else ["PM Jan Dhan Yojana", "Atal Pension Yojana"],
    }

    # Generate next question based on current state
    if profile.next_question == "occupation":
        reply = (
            "Welcome to ArthaNetra! 👋 To help me tailor practical money tips and find government schemes you qualify for, "
            "what do you currently do for work? (e.g. delivery partner, student, farmer, driver, shopkeeper)"
        )
        return reply, context_dict, False

    if profile.next_question == "language":
        reply = (
            f"Noted — **{profile.occupation}**! "
            "Which language do you feel most comfortable chatting in? (e.g. English, Hindi)"
        )
        return reply, context_dict, False

    if profile.next_question == "financial_goals":
        reply = (
            f"Got it! What is your main financial priority right now? "
            "(e.g., saving money, building an emergency fund, managing debt, or finding government schemes?)"
        )
        return reply, context_dict, False

    if profile.next_question == "monthly_income":
        reply = (
            f"Understood! Roughly what is your **monthly income**? "
            "(This helps me figure out a comfortable savings target and check scheme eligibility for you.)"
        )
        return reply, context_dict, False

    reply = (
        f"You're all set! 🎉 Profile saved.\n\n"
        f"How can I help you today? You can ask me to check government schemes for you, give tips on managing your budget, or verify if a loan offer is safe."
    )
    return reply, context_dict, True
