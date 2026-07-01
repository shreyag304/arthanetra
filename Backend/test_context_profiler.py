import pytest
from Backend.agents.context_profiler import run_context_profiler, ORDERED_FIELDS

def test_new_user():
    # 1. New user
    existing_profile = {}
    raw_user_message = ""
    result = run_context_profiler(raw_user_message, existing_profile)
    
    assert result["profile_completed"] is False
    assert result["next_question"] == "What is your preferred language?"
    assert result["updated_profile"] == {}

def test_structured_input():
    # 2. Structured input
    existing_profile = {}
    raw_user_message = {"preferred_language": "English", "occupation": "Software Engineer"}
    result = run_context_profiler(raw_user_message, existing_profile)
    
    assert result["profile_completed"] is False
    assert result["next_question"] == "What is your approximate income range?"
    assert result["updated_profile"]["preferred_language"] == "English"
    assert result["updated_profile"]["occupation"] == "Software Engineer"

def test_free_text_extraction(monkeypatch):
    # 3. Free-text extraction
    def mock_call_llm(msg, profile):
        return {"income_range": "$50k-$100k", "state": "California"}
    
    monkeypatch.setattr("Backend.agents.context_profiler.call_llm", mock_call_llm)
    
    existing_profile = {"preferred_language": "English", "occupation": "Software Engineer"}
    raw_user_message = "I make around 75k and live in California."
    
    result = run_context_profiler(raw_user_message, existing_profile)
    assert result["updated_profile"]["income_range"] == "$50k-$100k"
    assert result["updated_profile"]["state"] == "California"
    assert result["next_question"] == "What are your primary financial goals?"

def test_existing_profile_update():
    # 4. Existing profile update
    # The prompt explicitly asks to test "Existing profile update"
    existing_profile = {"preferred_language": "English", "occupation": "Software Engineer"}
    raw_user_message = {"occupation": "Senior Software Engineer"}
    
    result = run_context_profiler(raw_user_message, existing_profile)
    assert result["updated_profile"]["occupation"] == "Senior Software Engineer"
    assert result["updated_profile"]["preferred_language"] == "English"
    assert result["next_question"] == "What is your approximate income range?"

def test_profile_completion():
    # 5. Profile completion
    existing_profile = {
        "preferred_language": "English",
        "occupation": "Doctor",
        "income_range": "$100k+",
        "state": "NY",
        "financial_goals": "Retirement",
        "communication_mode": "Email",
        "has_loan": False,
    }
    raw_user_message = {"has_health_insurance": True}
    
    result = run_context_profiler(raw_user_message, existing_profile)
    assert result["profile_completed"] is True
    assert result["next_question"] is None
    assert result["updated_profile"]["has_health_insurance"] is True

def test_llm_failure(monkeypatch):
    # 6. LLM failure
    def mock_call_llm_fail(msg, profile):
        raise ValueError("LLM is down")
    
    monkeypatch.setattr("Backend.agents.context_profiler.call_llm", mock_call_llm_fail)
    
    existing_profile = {"preferred_language": "English"}
    raw_user_message = "I am a teacher"
    
    # Should catch the error, not crash, keep profile, and ask for occupation again
    result = run_context_profiler(raw_user_message, existing_profile)
    assert result["updated_profile"] == {"preferred_language": "English"}
    assert result["profile_completed"] is False
    assert result["next_question"] == "What is your occupation?"
