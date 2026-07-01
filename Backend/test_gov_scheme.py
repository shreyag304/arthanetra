import pytest
from Backend.agents.gov_scheme import run_gov_scheme

def test_farmer_scheme(monkeypatch):
    # 1. Farmer
    def mock_call_llm(prompt, raw_user_message, user_profile, chat_history):
        return {
            "eligibility_reason": "You are a farmer.",
            "benefits": "Financial support.",
            "next_steps": "Apply via PM-Kisan portal."
        }
    monkeypatch.setattr("Backend.agents.gov_scheme.call_llm", mock_call_llm)
    
    profile = {"occupation": "Farmer", "income_range": "Below 2L"}
    result = run_gov_scheme("What schemes can I get?", profile, [])
    assert "PM-Kisan Samman Nidhi" in result["eligible_schemes"]
    assert "Ayushman Bharat PM-JAY" in result["eligible_schemes"]
    assert "farmer" in result["eligibility_reason"].lower()

def test_student_scheme(monkeypatch):
    # 2. Student
    def mock_call_llm(prompt, raw_user_message, user_profile, chat_history):
        return {
            "eligibility_reason": "You are a student.",
            "benefits": "Scholarship.",
            "next_steps": "NSP portal."
        }
    monkeypatch.setattr("Backend.agents.gov_scheme.call_llm", mock_call_llm)
    
    profile = {"occupation": "Student", "income_range": "Below 5L"}
    result = run_gov_scheme("Any schemes?", profile, [])
    assert any("Scholarship" in s or "Vidyalakshmi" in s for s in result["eligible_schemes"])
    assert "student" in result["eligibility_reason"].lower()

def test_senior_citizen_scheme(monkeypatch):
    # 3. Senior citizen
    def mock_call_llm(prompt, raw_user_message, user_profile, chat_history):
        return {
            "eligibility_reason": "You are a senior citizen.",
            "benefits": "High interest.",
            "next_steps": "Post office."
        }
    monkeypatch.setattr("Backend.agents.gov_scheme.call_llm", mock_call_llm)
    
    profile = {"occupation": "Retired Senior Citizen", "income_range": "Above 5L"}
    result = run_gov_scheme("What can I get?", profile, [])
    assert any("Senior Citizen" in s or "SCSS" in s for s in result["eligible_schemes"])

def test_low_income_worker(monkeypatch):
    # 4. Low-income worker
    def mock_call_llm(prompt, raw_user_message, user_profile, chat_history):
        return {
            "eligibility_reason": "Low income worker.",
            "benefits": "Insurance.",
            "next_steps": "CSC."
        }
    monkeypatch.setattr("Backend.agents.gov_scheme.call_llm", mock_call_llm)
    
    profile = {"occupation": "Daily wage worker", "income_range": "Below 2L"}
    result = run_gov_scheme("Help me with schemes", profile, [])
    assert any("Jan Dhan" in s for s in result["eligible_schemes"])

def test_no_eligible_scheme():
    # 5. No eligible scheme
    profile = {"occupation": "Billionaire CEO", "income_range": "Above 100Cr"}
    result = run_gov_scheme("Are there schemes for me?", profile, [])
    assert result["eligible_schemes"] == []
    assert "couldn't find a matching scheme" in result["eligibility_reason"].lower()

def test_llm_failure(monkeypatch):
    # 6. LLM failure
    def mock_call_llm(prompt, raw_user_message, user_profile, chat_history):
        raise ValueError("Timeout")
    monkeypatch.setattr("Backend.agents.gov_scheme.call_llm", mock_call_llm)
    
    profile = {"occupation": "Farmer", "income_range": "Below 2L"}
    result = run_gov_scheme("What schemes can I get?", profile, [])
    assert "PM-Kisan Samman Nidhi" in result["eligible_schemes"]
    assert "nearest Common Service Centre" in result["next_steps"]
