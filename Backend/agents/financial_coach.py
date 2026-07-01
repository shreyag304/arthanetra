import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def call_llm(
    prompt: str,
    raw_user_message: str,
    user_profile: Dict[str, Any],
    fhs: int,
    chat_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Mockable LLM call to extract reasoning, explanation, and personalized advice.
    In production, this connects to an LLM (e.g. OpenAI/Gemini) and expects
    a structured JSON response.
    """
    # For standalone structure, return an empty/mock dictionary.
    # In tests, this function will be mocked.
    return {
        "financial_coach_response": "",
        "recommendations": [],
        "follow_up_questions": []
    }

def run_financial_coach(
    raw_user_message: str,
    user_profile: Dict[str, Any],
    financial_health_score: int,
    chat_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Financial Coach Agent
    Provides personalized financial education and actionable advice.
    Reads user_profile and financial_health_score.
    Never modifies user_profile or calculates FHS.
    """
    try:
        literacy_level = user_profile.get("literacy_level", "Unknown")
        
        # Build the system prompt
        system_prompt = f"""
        You are a Financial Coach helping users understand and improve their financial health.
        Provide personalized financial education and actionable advice based on the user's profile and Financial Health Score (FHS).
        
        User FHS: {financial_health_score}
        User Profile: {user_profile}
        
        Rules:
        - Advice should depend on FHS, occupation, income_range, goals, communication language, and literacy level.
        - If literacy level is LOW, explain using very simple language and real-life Indian examples. Avoid financial jargon.
        - NEVER recommend specific stocks, mutual funds by name, crypto, trading, or guaranteed returns. Give only educational financial guidance.
        - NEVER calculate the Financial Health Score.
        - NEVER update the database or use business rules for calculations.
        """
        
        # Call the LLM
        response = call_llm(
            prompt=system_prompt,
            raw_user_message=raw_user_message,
            user_profile=user_profile,
            fhs=financial_health_score,
            chat_history=chat_history
        )
        
        # Ensure correct output schema
        return {
            "financial_coach_response": response.get("financial_coach_response", ""),
            "recommendations": response.get("recommendations", []),
            "follow_up_questions": response.get("follow_up_questions", [])
        }
        
    except Exception as e:
        logger.error(f"Financial Coach LLM failed: {e}")
        # Friendly fallback response
        return {
            "financial_coach_response": "I'm having a little trouble thinking right now. But I'm here to help you on your financial journey. Could you try asking that again?",
            "recommendations": ["Review your latest Financial Health Score"],
            "follow_up_questions": ["What is your biggest financial worry right now?"]
        }
