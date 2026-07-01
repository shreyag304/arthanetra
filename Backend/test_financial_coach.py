import pytest
from Backend.agents.financial_coach import run_financial_coach

@pytest.fixture
def default_profile():
    return {
        "preferred_language": "English",
        "occupation": "Software Engineer",
        "income_range": "$50k-$100k",
        "literacy_level": "High"
    }

def test_budgeting_advice(monkeypatch, default_profile):
    # 1. User asking budgeting advice
    def mock_call_llm(prompt, raw_user_message, user_profile, fhs, chat_history):
        return {
            "financial_coach_response": "Budgeting is the process of creating a plan to spend your money.",
            "recommendations": ["Use the 50/30/20 rule"],
            "follow_up_questions": ["Do you track your expenses?"]
        }
    monkeypatch.setattr("Backend.agents.financial_coach.call_llm", mock_call_llm)
    
    result = run_financial_coach("How can I budget better?", default_profile, 75, [])
    assert "Budgeting" in result["financial_coach_response"]
    assert "Use the 50/30/20 rule" in result["recommendations"]

def test_low_fhs_advice(monkeypatch, default_profile):
    # 2. User asking about low FHS
    def mock_call_llm(prompt, raw_user_message, user_profile, fhs, chat_history):
        return {
            "financial_coach_response": "A score of 42 indicates you might have high debt or low savings.",
            "recommendations": ["Start an emergency fund"],
            "follow_up_questions": ["What are your current debts?"]
        }
    monkeypatch.setattr("Backend.agents.financial_coach.call_llm", mock_call_llm)
    
    result = run_financial_coach("Why is my FHS only 42?", default_profile, 42, [])
    assert "42" in result["financial_coach_response"]

def test_savings_advice(monkeypatch, default_profile):
    # 3. User asking about savings
    def mock_call_llm(prompt, raw_user_message, user_profile, fhs, chat_history):
        return {
            "financial_coach_response": "Saving helps you build an emergency fund.",
            "recommendations": ["Automate your savings"],
            "follow_up_questions": ["How much do you currently save?"]
        }
    monkeypatch.setattr("Backend.agents.financial_coach.call_llm", mock_call_llm)
    
    result = run_financial_coach("How can I save more money?", default_profile, 80, [])
    assert result["recommendations"] == ["Automate your savings"]

def test_debt_advice(monkeypatch, default_profile):
    # 4. User asking about debt
    def mock_call_llm(prompt, raw_user_message, user_profile, fhs, chat_history):
        assert "NEVER recommend" in prompt # Ensure rules are in prompt
        return {
            "financial_coach_response": "Reducing EMI can help free up cash flow.",
            "recommendations": ["Prepay high interest loans"],
            "follow_up_questions": ["What is your highest interest loan?"]
        }
    monkeypatch.setattr("Backend.agents.financial_coach.call_llm", mock_call_llm)
    
    result = run_financial_coach("Should I reduce my EMI?", default_profile, 65, [])
    assert "EMI" in result["financial_coach_response"]

def test_low_literacy_profile(monkeypatch):
    # 5. Low literacy profile
    low_lit_profile = {
        "preferred_language": "Hindi",
        "occupation": "Farmer",
        "income_range": "Below 2L",
        "literacy_level": "LOW"
    }
    
    def mock_call_llm(prompt, raw_user_message, user_profile, fhs, chat_history):
        # We can assert that the prompt correctly passed the low literacy level instructions
        assert "LOW" in prompt
        assert "simple language and real-life Indian examples" in prompt
        return {
            "financial_coach_response": "Socho ki tumhare pas ek matka hai...",
            "recommendations": ["Roz thoda paisa bachao"],
            "follow_up_questions": ["Kya tum gudiya ke liye paise bacha rahe ho?"]
        }
    monkeypatch.setattr("Backend.agents.financial_coach.call_llm", mock_call_llm)
    
    result = run_financial_coach("What is an emergency fund?", low_lit_profile, 50, [])
    assert "Socho" in result["financial_coach_response"]

def test_llm_failure(monkeypatch, default_profile):
    # 6. LLM failure
    def mock_call_llm(prompt, raw_user_message, user_profile, fhs, chat_history):
        raise ValueError("API Timeout")
    monkeypatch.setattr("Backend.agents.financial_coach.call_llm", mock_call_llm)
    
    result = run_financial_coach("What is SIP?", default_profile, 70, [])
    assert "having a little trouble thinking" in result["financial_coach_response"]
    assert len(result["recommendations"]) > 0
    assert len(result["follow_up_questions"]) > 0
