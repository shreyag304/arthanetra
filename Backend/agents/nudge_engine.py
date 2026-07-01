import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def call_llm(prompt: str, raw_message: str, user_profile: Dict[str, Any]) -> str:
    """
    Mockable LLM call to rewrite the notification into friendly language.
    Never used to decide IF a nudge should be generated.
    """
    return f"Friendly rewrite: {raw_message}"

def run_nudge_engine(
    user_profile: Dict[str, Any],
    financial_health_score: int,
    recent_transactions: List[Dict[str, Any]],
    previous_nudges: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Nudge Engine Agent
    Generates proactive financial reminders based on user behaviour (deterministic rules).
    Never sends notifications directly.
    """
    # Track past reasons to prevent duplicate nudges
    past_reasons = [nudge.get("reason") for nudge in previous_nudges if "reason" in nudge]
    
    candidate_nudges = []
    
    # 1. FHS Drop
    prev_fhs = user_profile.get("previous_fhs")
    if prev_fhs is not None and financial_health_score < prev_fhs - 5:
        reason_str = "Financial Health Score drop detected."
        if reason_str not in past_reasons:
            candidate_nudges.append({
                "priority": "high",
                "reason": reason_str,
                "raw_message": f"Your financial health score dropped by {prev_fhs - financial_health_score} points. Let's get it back on track!"
            })
            
    monthly_income = user_profile.get("monthly_income", 50000) # Default to 50k to prevent divide by zero
    
    # 2. High spending
    total_spent = sum(t.get("amount", 0) for t in recent_transactions if t.get("type", "debit").lower() == "debit")
    if total_spent > (monthly_income * 0.8):
        reason_str = "High spending detected."
        if reason_str not in past_reasons:
            candidate_nudges.append({
                "priority": "high",
                "reason": reason_str,
                "raw_message": "You have spent a large portion of your monthly income recently. Keep an eye on your budget."
            })
            
    # 3. Low savings
    savings = user_profile.get("savings_balance", 0)
    if savings < (monthly_income * 0.1):
        reason_str = "Low savings balance."
        if reason_str not in past_reasons:
            candidate_nudges.append({
                "priority": "medium",
                "reason": reason_str,
                "raw_message": "Your savings are quite low. Try to save a little extra this month."
            })
            
    # 4. Emergency fund below target
    emergency_fund = user_profile.get("emergency_fund", 0)
    ef_target = user_profile.get("emergency_fund_target", monthly_income * 3)
    if emergency_fund < ef_target:
        reason_str = "Emergency fund below target."
        if reason_str not in past_reasons:
            candidate_nudges.append({
                "priority": "medium",
                "reason": reason_str,
                "raw_message": "Your emergency fund needs a top-up to keep you secure."
            })
            
    # 5. Increasing EMI burden
    emi_amount = user_profile.get("emi_amount", 0)
    if emi_amount > (monthly_income * 0.4):
        reason_str = "High EMI burden."
        if reason_str not in past_reasons:
            candidate_nudges.append({
                "priority": "high",
                "reason": reason_str,
                "raw_message": "Your loan EMIs are taking up a big part of your income. Consider reviewing your debts."
            })
            
    if not candidate_nudges:
        return {
            "should_notify": False,
            "priority": "low",
            "reason": "No actionable nudges detected.",
            "notification": ""
        }
        
    # Sort by priority
    priority_map = {"high": 3, "medium": 2, "low": 1}
    candidate_nudges.sort(key=lambda x: priority_map.get(x["priority"], 0), reverse=True)
    
    selected_nudge = candidate_nudges[0]
    
    # Use LLM ONLY to rewrite the message
    pref_lang = user_profile.get("preferred_language", "English")
    lit_level = user_profile.get("literacy_level", "Medium")
    
    system_prompt = f"""
    You are a friendly financial assistant. Rewrite the following notification for the user.
    Preferred Language: {pref_lang}
    Literacy Level: {lit_level}
    
    If Literacy Level is Low, use very simple, non-jargon language.
    Return ONLY the rewritten notification text.
    """
    
    try:
        rewritten_message = call_llm(
            prompt=system_prompt,
            raw_message=selected_nudge["raw_message"],
            user_profile=user_profile
        )
    except Exception as e:
        logger.error(f"Nudge Engine LLM failed: {e}")
        rewritten_message = selected_nudge["raw_message"] # Safe fallback
        
    return {
        "should_notify": True,
        "priority": selected_nudge["priority"],
        "reason": selected_nudge["reason"],
        "notification": rewritten_message
    }
