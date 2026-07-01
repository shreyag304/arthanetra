import pandas as pd
import json
import os

def categorize_transaction(description, amount, txn_type):
    """
    Very basic keyword-based categorization for hackathon MVP purposes.
    (Pro Tip: In a real app or for a hackathon flex, you can pass unclassified 
    transactions to an LLM like Gemini to categorize them instantly).
    """
    desc = str(description).lower()
    
    if txn_type == 'CREDIT':
        if any(keyword in desc for keyword in ['salary', 'neft', 'wages']):
            return 'Income'
        return 'Other_Income'
    
    if txn_type == 'DEBIT':
        if any(keyword in desc for keyword in ['emi', 'loan', 'bajaj', 'hdfc bank loan']):
            return 'EMI'
        if any(keyword in desc for keyword in ['zerodha', 'groww', 'mutual fund', 'sip', 'fd']):
            return 'Savings_Investment'
        return 'Spend'

def calculate_fhs(csv_file_path, current_liquid_balance):
    # 1. Read the uploaded Bank Statement CSV
    df = pd.read_csv(csv_file_path)
    
    # 2. Categorize each row
    df['Category'] = df.apply(lambda row: categorize_transaction(row['Description'], row['Amount'], row['Type']), axis=1)
    
    # 3. Aggregate Monthly Totals
    # (Assuming the uploaded CSV represents exactly 1 month of data for simplicity)
    totals = df.groupby('Category')['Amount'].sum().to_dict()
    
    income = totals.get('Income', 0) + totals.get('Other_Income', 0)
    spends = totals.get('Spend', 0)
    savings = totals.get('Savings_Investment', 0)
    emis = totals.get('EMI', 0)
    
    if income == 0:
        return {"error": "No income found to calculate ratios."}
        
    # 4. Calculate Ratios
    spend_ratio = spends / income
    save_ratio = savings / income
    emi_ratio = emis / income
    liquid_months = current_liquid_balance / spends if spends > 0 else 0
    
    # 5. Apply FHS Algorithm
    # Spend Score (25%)
    if spend_ratio <= 0.5: spend_score = 100
    elif spend_ratio <= 0.9: spend_score = 100 - ((spend_ratio - 0.5) * 200)
    else: spend_score = 0
        
    # Save Score (25%)
    if save_ratio >= 0.3: save_score = 100
    elif save_ratio > 0: save_score = (save_ratio / 0.3) * 100
    else: save_score = 0
        
    # EMI Score (20%)
    if emi_ratio == 0: emi_score = 100
    elif emi_ratio <= 0.4: emi_score = 100 - ((emi_ratio / 0.4) * 60)
    else: emi_score = max(0, 40 - ((emi_ratio - 0.4) * 200))
        
    # Emergency Fund Score (15%)
    if liquid_months >= 6: emergency_score = 100
    elif liquid_months > 0: emergency_score = (liquid_months / 6) * 100
    else: emergency_score = 0
        
    # Mocked Advanced Scores for MVP
    insurance_score = 50 # Assume they answered 'Health Insurance' only in onboarding
    literacy_score = 50  # Default baseline
    
    # 6. Total FHS Calculation
    total_score = (spend_score * 0.25) + (save_score * 0.25) + (emi_score * 0.20) + (emergency_score * 0.15) + (insurance_score * 0.10) + (literacy_score * 0.05)
    
    return {
        "Data Summary": {
            "Income": income,
            "Spends": spends,
            "Savings": savings,
            "EMIs": emis
        },
        "Sub Scores": {
            "Spending": round(spend_score, 1),
            "Savings": round(save_score, 1),
            "Debt Management": round(emi_score, 1),
            "Emergency": round(emergency_score, 1)
        },
        "Final FHS": round(total_score, 1)
    }

if __name__ == "__main__":
    # --- MOCK EXECUTION FOR TESTING ---
    mock_csv_path = "mock_statement.csv"
    mock_data = """Date,Description,Amount,Type
01-07-2024,TCS Salary NEFT,100000,CREDIT
02-07-2024,HDFC Bank Loan EMI,25000,DEBIT
05-07-2024,Groww Mutual Fund SIP,15000,DEBIT
10-07-2024,Zomato UPI,1500,DEBIT
15-07-2024,Amazon Shopping,8500,DEBIT
20-07-2024,Grocery Store,10000,DEBIT
"""
    with open(mock_csv_path, "w") as f:
        f.write(mock_data)
        
    print("Processing mock statement...")
    result = calculate_fhs(mock_csv_path, current_liquid_balance=150000)
    
    print("\n=== ArthaNetra FHS Result ===")
    print(json.dumps(result, indent=2))
    
    # Cleanup
    os.remove(mock_csv_path)
