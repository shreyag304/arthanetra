import json
import logging
import os
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "government_schemes.json")

def load_schemes() -> List[Dict[str, Any]]:
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load schemes: {e}")
        return []

def call_llm(
    prompt: str,
    raw_user_message: str,
    user_profile: Dict[str, Any],
    chat_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Mockable LLM call to explain eligibility, benefits, and next steps.
    """
    # Standalone mock response
    return {
        "eligibility_reason": "You meet the general criteria based on your occupation.",
        "benefits": "Various government benefits depending on the exact scheme.",
        "next_steps": "Check the official government portals."
    }

def run_gov_scheme(
    raw_user_message: str,
    user_profile: Dict[str, Any],
    chat_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Government Scheme Navigator Agent
    Helps users discover government schemes they are eligible for.
    Never modifies user_profile. Uses deterministic filtering first.
    """
    schemes = load_schemes()
    eligible_schemes = []
    
    # 1. Deterministic Filtering
    user_occupation = str(user_profile.get("occupation", "")).lower()
    user_income = str(user_profile.get("income_range", "")).lower()
    
    for scheme in schemes:
        scheme_occupations = [occ.lower() for occ in scheme.get("occupations", [])]
        
        occupation_match = False
        if not scheme_occupations or "any" in scheme_occupations:
            occupation_match = True
        else:
            for occ in scheme_occupations:
                if occ in user_occupation:
                    occupation_match = True
                    break
                    
        # Income check heuristic for this basic dataset
        scheme_income = scheme.get("income_max_str", "any").lower()
        income_match = True
        if scheme_income != "any":
            if "below" in scheme_income and "above" in user_income:
                income_match = False
            elif "below 2l" in scheme_income and ("5l" in user_income or "10l" in user_income or "50k-$100k" in user_income):
                # Basic string exclusion for simplistic deterministic logic
                if "above" in user_income or "50k-" in user_income:
                     income_match = False
                     
        if occupation_match and income_match:
            eligible_schemes.append(scheme["name"])
            
    if not eligible_schemes:
        return {
            "eligible_schemes": [],
            "eligibility_reason": "Based on your profile, we couldn't find a matching scheme at this moment.",
            "benefits": "N/A",
            "next_steps": "Keep updating your profile to see if new schemes become applicable."
        }
        
    try:
        system_prompt = f"""
        You are a Government Scheme Navigator.
        The user is eligible for the following schemes: {eligible_schemes}.
        User Profile: {user_profile}
        
        Rules:
        - Explain why the user is eligible.
        - Outline the main benefits of these schemes.
        - Provide simple application guidance.
        """
        
        response = call_llm(
            prompt=system_prompt,
            raw_user_message=raw_user_message,
            user_profile=user_profile,
            chat_history=chat_history
        )
        
        return {
            "eligible_schemes": eligible_schemes,
            "eligibility_reason": response.get("eligibility_reason", "You meet the general criteria."),
            "benefits": response.get("benefits", "Provides government support."),
            "next_steps": response.get("next_steps", "Visit the respective official scheme portals.")
        }
        
    except Exception as e:
        logger.error(f"Gov Scheme LLM failed: {e}")
        # Deterministic fallback
        return {
            "eligible_schemes": eligible_schemes,
            "eligibility_reason": "Based on your provided occupation and income, you are eligible for these schemes.",
            "benefits": "These schemes offer financial assistance, insurance, or educational support as per government rules.",
            "next_steps": "Please visit the official government portals or your nearest Common Service Centre (CSC) to apply."
        }
