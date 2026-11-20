"""
Nudge Engine:
Proactively generates behavioral financial nudges and reminders based on the user's database state:
- Savings goal progress
- Unapplied government welfare schemes
- Debt/EMI cautionary reminders
- Financial Health Score improvement suggestions
Does not wait passively — evaluates the user state and surfaces timely, actionable nudges.
"""
from typing import Optional, Dict, Any, List
from sqlmodel import Session, select
from dbmodel.models import UserFinancialProfile, User, FinancialHealthScore, UserSchemeMatch


def generate_proactive_nudge(session: Session, user_id: int) -> Optional[Dict[str, Any]]:
    profile = session.exec(
        select(UserFinancialProfile).where(UserFinancialProfile.user_id == user_id)
    ).first()
    user = session.exec(select(User).where(User.id == user_id)).first()
    fhs = session.exec(
        select(FinancialHealthScore).where(FinancialHealthScore.user_id == user_id)
    ).first()
    matches = session.exec(
        select(UserSchemeMatch).where(UserSchemeMatch.user_id == user_id)
    ).all()

    occupation = (profile.occupation if profile and profile.occupation else (user.persona if user and user.persona else "worker")).lower()
    savings_rate = fhs.savings_rate if fhs else 0.20
    debt_ratio = fhs.debt_ratio if fhs else 0.10
    score = fhs.score if fhs else 75.0

    # Rule 1: High Debt Alert Nudge
    if debt_ratio > 0.35:
        return {
            "type": "nudge",
            "category": "debt_alert",
            "title": "Debt Caution",
            "message": "⚠️ **Proactive Nudge:** Your monthly debt/EMI payments are currently over 35% of your income. Prioritize paying down high-cost loans to prevent interest accumulation and boost your Financial Health Score."
        }

    # Rule 2: Unclaimed Government Scheme Nudge
    enrolled_names = [m.scheme_name.lower() for m in matches]
    if ("delivery" in occupation or "gig" in occupation) and not any("svanidhi" in s for s in enrolled_names):
        return {
            "type": "nudge",
            "category": "scheme_reminder",
            "title": "Government Scheme Opportunity",
            "message": "💡 **Proactive Nudge:** As a delivery partner, you qualify for **PM SVANidhi's collateral-free working capital loan** with a 7% interest subsidy. Ask me: *'How do I apply for PM SVANidhi?'*"
        }

    if not any("shram" in s for s in enrolled_names):
        return {
            "type": "nudge",
            "category": "scheme_reminder",
            "title": "Free Accidental Insurance",
            "message": "💡 **Proactive Nudge:** You have not registered for an **e-Shram Card** yet. It provides free ₹2 Lakh accidental insurance under PMSBY for unorganized and gig workers."
        }

    # Rule 3: Savings Discipline Nudge
    if savings_rate < 0.20:
        return {
            "type": "nudge",
            "category": "savings_reminder",
            "title": "Micro-Savings Target",
            "message": "💰 **Proactive Nudge:** Try setting aside ₹250 from your next payout into your liquid savings fund to improve your Financial Health Score towards 85+!"
        }

    # Rule 4: Health Score Check
    return {
        "type": "nudge",
        "category": "wellness_reminder",
        "title": "Financial Health Tracking",
        "message": f"📊 **Proactive Nudge:** Your Financial Health Score is **{score}/100**. Maintain a consistent savings rate and low credit utilization to keep it climbing."
    }

