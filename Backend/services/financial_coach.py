"""
Financial Coach Agent:
Provides personalized budgeting, savings, debt management, and financial planning advice.
Always references the user's financial profile (occupation, income structure, goals, score)
to craft actionable, empathetic financial recommendations.
"""
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from dbmodel.models import UserFinancialProfile, User
from services.llm_service import llm_client


def execute_financial_coach(session: Session, user_id: int, message: str, language: str = "English") -> Dict[str, Any]:
    profile = session.exec(
        select(UserFinancialProfile).where(UserFinancialProfile.user_id == user_id)
    ).first()
    user = session.exec(select(User).where(User.id == user_id)).first()

    occupation = profile.occupation if profile and profile.occupation else (user.persona if user and user.persona else "Working Professional")
    income_type = user.income_type if user and user.income_type else "Variable"
    goal = user.goal if user and user.goal else (profile.financial_goals if profile and profile.financial_goals else "Savings & Financial Stability")
    health_score = user.financial_health_score if user and user.financial_health_score else 75
    monthly_income = profile.monthly_income if profile and profile.monthly_income else "Variable"

    system_instruction = (
        f"You are ArthaNetra's AI Financial Coach for India.\n"
        f"Always reply in: {language}.\n"
        f"Format rules:\n"
        f"- Be concise, direct, and user-friendly.\n"
        f"- Use bold headings and bullet points.\n"
        f"- Give 3 actionable, realistic steps (budgeting, emergency fund, avoiding loan traps).\n"
        f"- No robotic filler or generic disclaimers."
    )

    # Calculate precise personalized targets
    try:
        inc = float(monthly_income)
        daily_save = round(inc * 0.15 / 30, 0)
        monthly_save = round(inc * 0.20, 0)
        emergency_fund = round(inc * 3, 0)
    except Exception:
        daily_save = 150
        monthly_save = 4000
        emergency_fund = 30000

    prompt = (
        f"User Profile:\n"
        f"- Occupation: {occupation}\n"
        f"- Income: ₹{monthly_income}/month ({income_type})\n"
        f"- Financial Goal: {goal}\n"
        f"- Financial Health Score: {health_score}/100\n\n"
        f"User Question: \"{message}\"\n\n"
        f"Give a precise, user-friendly reply tailored to their livelihood with clear bullet points."
    )

    coach_response = None
    if llm_client.is_available():
        try:
            llm_text = llm_client.generate(prompt, system_instruction=system_instruction)
            # If it fell back to offline generic template, use our richer mathematical tailored plan
            if llm_text and not llm_text.startswith("💡 **Smart Financial Action Plan**") and not llm_text.startswith("💡 Financial Coaching:"):
                coach_response = llm_text
        except Exception:
            coach_response = None

    if not coach_response:
        # Context-sensitive loan/credit advice based on livelihood
        occ_lower = occupation.lower()
        if any(w in occ_lower for w in ["farmer", "kisan", "cultivat", "agricult"]):
            credit_tip = "Avoid high-interest local moneylenders. Instead, use the **Kisan Credit Card (KCC)** which offers short-term crop loans at an effective 4% interest rate with prompt repayment."
        elif any(w in occ_lower for w in ["delivery", "driver", "vendor", "hawker", "gig"]):
            credit_tip = "Stay clear of 7-day mobile loan apps with hidden fees. If you need working funds, the government-backed **PM SVANidhi** provides collateral-free loans starting at ₹10,000 at 7% subsidized interest."
        elif "student" in occ_lower:
            credit_tip = "Be cautious with 'Buy Now, Pay Later' (BNPL) offers or easy digital loans that harm your future credit score before you begin your career."
        else:
            credit_tip = "Stay clear of unregulated instant loan apps. Stick to RBI-approved banks or NBFCs to protect your credit score."

        coach_response = (
            f"Glad you asked! Here is a simple, realistic way to work toward **{goal}**:\n\n"
            f"1. **Put aside a small daily amount:**\n"
            f"   Try setting aside **₹{int(daily_save)} a day** (around ₹{int(monthly_save)} a month). Small daily amounts build up quietly without pinching your daily routine.\n\n"
            f"2. **Build an emergency cushion:**\n"
            f"   Aim to build an initial buffer of **₹{int(emergency_fund)}** in a zero-balance account. Having this ready covers unexpected repairs or medical needs without forcing you into debt.\n\n"
            f"3. **Borrowing safely:**\n"
            f"   {credit_tip}\n\n"
            f"Your Financial Health Score is currently **{int(health_score)}/100**. Would you like tips on cutting down daily costs or checking schemes you can apply for?"
        )

    return {
        "reply": coach_response,
        "persona_used": occupation,
        "goal_used": goal,
        "health_score": health_score
    }

    return {
        "reply": coach_response,
        "persona_used": occupation,
        "goal_used": goal,
        "health_score": health_score
    }

