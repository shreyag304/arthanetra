import pandas as pd

def categorize_transaction(description, amount, txn_type):
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

def calculate_fhs_from_dataframe(df, current_liquid_balance):
    # Assume dataframe has columns: Date, Description, Amount, Type
    
    # Optional: clean column names just in case
    df.columns = [c.strip().title() for c in df.columns]
    
    # 2. Categorize each row
    df['Category'] = df.apply(
        lambda row: categorize_transaction(
            row.get('Description', ''), 
            row.get('Amount', 0), 
            row.get('Type', '')
        ), 
        axis=1
    )
    
    # 3. Aggregate Monthly Totals
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
    if spend_ratio <= 0.5: spend_score = 100
    elif spend_ratio <= 0.9: spend_score = 100 - ((spend_ratio - 0.5) * 200)
    else: spend_score = 0
        
    if save_ratio >= 0.3: save_score = 100
    elif save_ratio > 0: save_score = (save_ratio / 0.3) * 100
    else: save_score = 0
        
    if emi_ratio == 0: emi_score = 100
    elif emi_ratio <= 0.4: emi_score = 100 - ((emi_ratio / 0.4) * 60)
    else: emi_score = max(0, 40 - ((emi_ratio - 0.4) * 200))
        
    if liquid_months >= 6: emergency_score = 100
    elif liquid_months > 0: emergency_score = (liquid_months / 6) * 100
    else: emergency_score = 0
        
    insurance_score = 50 
    literacy_score = 50  
    
    # 6. Total FHS Calculation
    total_score = (spend_score * 0.25) + (save_score * 0.25) + (emi_score * 0.20) + (emergency_score * 0.15) + (insurance_score * 0.10) + (literacy_score * 0.05)
    
    return {
        "data_summary": {
            "income": income,
            "spends": spends,
            "savings": savings,
            "emis": emis
        },
        "sub_scores": {
            "spending": round(spend_score, 1),
            "savings": round(save_score, 1),
            "debt_management": round(emi_score, 1),
            "emergency": round(emergency_score, 1)
        },
        "final_fhs": round(total_score, 1)
    }
