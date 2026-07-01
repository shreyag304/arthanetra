import pytest
from Backend.agents.nudge_engine import run_nudge_engine

def test_fhs_drop(monkeypatch):
    # 1. FHS drop
    def mock_call_llm(prompt, raw_message, user_profile):
        return f"Hey! {raw_message}"
    monkeypatch.setattr("Backend.agents.nudge_engine.call_llm", mock_call_llm)
    
    profile = {"previous_fhs": 80, "monthly_income": 50000, "emergency_fund": 200000}
    result = run_nudge_engine(profile, 60, [], [])
    assert result["should_notify"] is True
    assert "drop" in result["reason"].lower()
    assert "Hey!" in result["notification"]

def test_high_spending(monkeypatch):
    # 2. High spending
    def mock_call_llm(prompt, raw_message, user_profile):
        return raw_message
    monkeypatch.setattr("Backend.agents.nudge_engine.call_llm", mock_call_llm)
    
    profile = {"monthly_income": 50000, "emergency_fund": 200000}
    transactions = [{"type": "debit", "amount": 45000}]
    result = run_nudge_engine(profile, 75, transactions, [])
    assert result["should_notify"] is True
    assert "spending" in result["reason"].lower()

def test_low_savings(monkeypatch):
    # 3. Low savings
    def mock_call_llm(prompt, raw_message, user_profile):
        return raw_message
    monkeypatch.setattr("Backend.agents.nudge_engine.call_llm", mock_call_llm)
    
    profile = {"monthly_income": 50000, "savings_balance": 1000, "emergency_fund": 200000}
    result = run_nudge_engine(profile, 75, [], [])
    assert result["should_notify"] is True
    assert "savings" in result["reason"].lower()

def test_duplicate_prevention(monkeypatch):
    # 4. Duplicate prevention
    def mock_call_llm(prompt, raw_message, user_profile):
        return raw_message
    monkeypatch.setattr("Backend.agents.nudge_engine.call_llm", mock_call_llm)
    
    profile = {"monthly_income": 50000, "emergency_fund": 200000, "savings_balance": 100000}
    transactions = [{"type": "debit", "amount": 45000}]
    
    # First call to get the high spending reason
    res1 = run_nudge_engine(profile, 75, transactions, [])
    assert res1["should_notify"] is True
    reason = res1["reason"]
    
    # Second call passing previous_nudges
    res2 = run_nudge_engine(profile, 75, transactions, [{"reason": reason}])
    # Should not notify for high spending again. And since savings/emergency fund are fine, should_notify = False
    assert res2["should_notify"] is False
    assert res2["reason"] == "No actionable nudges detected."

def test_llm_failure(monkeypatch):
    # 5. LLM failure
    def mock_call_llm(prompt, raw_message, user_profile):
        raise ValueError("Timeout")
    monkeypatch.setattr("Backend.agents.nudge_engine.call_llm", mock_call_llm)
    
    profile = {"previous_fhs": 80, "monthly_income": 50000, "emergency_fund": 200000}
    result = run_nudge_engine(profile, 60, [], [])
    assert result["should_notify"] is True
    # LLM failed, but it should fallback to raw message
    assert "dropped by 20 points" in result["notification"]
