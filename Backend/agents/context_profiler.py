import logging
from typing import Optional, Dict, Any, Union
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class UserProfile(BaseModel):
    preferred_language: Optional[str] = None
    occupation: Optional[str] = None
    income_range: Optional[str] = None
    state: Optional[str] = None
    financial_goals: Optional[str] = None
    communication_mode: Optional[str] = None
    has_loan: Optional[bool] = None
    has_health_insurance: Optional[bool] = None

class AppState(BaseModel):
    user_profile: UserProfile

QUESTIONS = {
    "preferred_language": "What is your preferred language?",
    "occupation": "What is your occupation?",
    "income_range": "What is your approximate income range?",
    "state": "Which state do you live in?",
    "financial_goals": "What are your primary financial goals?",
    "communication_mode": "What is your preferred communication mode?",
    "has_loan": "Do you currently have any loans?",
    "has_health_insurance": "Do you have health insurance?"
}

ORDERED_FIELDS = [
    "preferred_language",
    "occupation",
    "income_range",
    "state",
    "financial_goals",
    "communication_mode",
    "has_loan",
    "has_health_insurance"
]

def call_llm(user_message: str, current_profile: dict) -> dict:
    """
    Mockable LLM call to extract structured fields from free text.
    In production, replace with actual LLM inference that returns a dictionary
    of extracted fields.
    """
    # For standalone structure, return an empty dict by default or raise NotImplementedError.
    # In tests, this will be mocked.
    return {}

def run_context_profiler(raw_user_message: Union[str, Dict[str, Any]], existing_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Context Profiler Agent
    Updates the user's financial profile based on structured or free-text input.
    """
    profile = existing_profile.copy()
    
    if isinstance(raw_user_message, dict):
        # Structured frontend input -> update directly, do not call LLM
        for key, value in raw_user_message.items():
            if key in ORDERED_FIELDS:
                profile[key] = value
                
    elif isinstance(raw_user_message, str) and raw_user_message.strip():
        # Free-text input -> call LLM to extract
        try:
            extracted_fields = call_llm(raw_user_message, profile)
            if isinstance(extracted_fields, dict):
                for key, value in extracted_fields.items():
                    if key in ORDERED_FIELDS and value is not None:
                        profile[key] = value
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            # If extraction fails, keep existing profile and do not crash
            pass
            
    # Determine the missing field to ask next
    next_question = None
    profile_completed = True
    
    for field in ORDERED_FIELDS:
        if profile.get(field) is None:
            next_question = QUESTIONS[field]
            profile_completed = False
            break
            
    return {
        "updated_profile": profile,
        "profile_completed": profile_completed,
        "next_question": next_question
    }
