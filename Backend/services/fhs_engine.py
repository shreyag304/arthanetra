"""
Financial Health Score (FHS) Engine:
Pure deterministic mathematics (Zero AI):
FHS = (savings_rate_score × weight1) + (debt_ratio_inverse_score × weight2)
    + (scheme_utilization_score × weight3) + (quiz_score × weight4)

Weights:
weight1 = 0.35 (Savings Rate)
weight2 = 0.30 (Debt Ratio Inverse)
weight3 = 0.20 (Government Scheme Utilization)
weight4 = 0.15 (Financial Literacy / Quiz Score)

All four inputs pull from data sitting in the database.
Recalculated and persisted to financial_health_score whenever relevant data changes.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from dbmodel.models import FinancialHealthScore, UserFinancialProfile, User, UserSchemeMatch

WEIGHT_SAVINGS = 0.35
WEIGHT_DEBT_INVERSE = 0.30
WEIGHT_SCHEMES = 0.20
WEIGHT_QUIZ = 0.15


def get_or_create_fhs_record(session: Session, user_id: int) -> FinancialHealthScore:
    fhs = session.exec(
        select(FinancialHealthScore).where(FinancialHealthScore.user_id == user_id)
    ).first()
    if not fhs:
        fhs = FinancialHealthScore(
            user_id=user_id,
            score=75.0,
            monthly_income=25000.0,
            monthly_savings=5000.0,
            monthly_debt_emi=3000.0,
            quiz_score=70.0,
            schemes_enrolled_count=1,
            quiz_completed=True,
            updated_at=datetime.utcnow()
        )
        session.add(fhs)
        session.commit()
        session.refresh(fhs)
    return fhs


def compute_fhs_math(
    monthly_income: float,
    monthly_savings: float,
    monthly_debt_emi: float,
    schemes_count: int,
    quiz_score: float
) -> Dict[str, Any]:
    """
    Pure math calculation function.
    """
    income = max(1000.0, float(monthly_income or 25000.0))
    savings = max(0.0, float(monthly_savings or 0.0))
    emi = max(0.0, float(monthly_debt_emi or 0.0))
    quiz = max(0.0, min(100.0, float(quiz_score if quiz_score is not None else 70.0)))

    # 1. Savings Rate Score (0 - 100)
    # Benchmark: 30% savings rate achieves full 100 points
    savings_rate = min(1.0, savings / income)
    savings_score = min(100.0, (savings_rate / 0.30) * 100.0)

    # 2. Debt Ratio Inverse Score (0 - 100)
    # Lower debt is better. 0% EMI = 100 points, <=40% EMI = 50-100 points, >40% drops rapidly
    debt_ratio = min(1.0, emi / income)
    if debt_ratio == 0:
        debt_inverse_score = 100.0
    elif debt_ratio <= 0.40:
        debt_inverse_score = 100.0 - ((debt_ratio / 0.40) * 50.0)
    else:
        debt_inverse_score = max(0.0, 50.0 - (((debt_ratio - 0.40) / 0.40) * 50.0))

    # 3. Scheme Utilization Score (0 - 100)
    # Based on government scheme matches / enrollments in database
    if schemes_count <= 0:
        scheme_score = 25.0
    elif schemes_count == 1:
        scheme_score = 65.0
    elif schemes_count == 2:
        scheme_score = 85.0
    else:
        scheme_score = 100.0

    # 4. Quiz / Literacy Score (0 - 100)
    quiz_component = quiz

    # Total Weighted Formula
    final_fhs = (
        (savings_score * WEIGHT_SAVINGS) +
        (debt_inverse_score * WEIGHT_DEBT_INVERSE) +
        (scheme_score * WEIGHT_SCHEMES) +
        (quiz_component * WEIGHT_QUIZ)
    )
    final_fhs = round(max(0.0, min(100.0, final_fhs)), 1)

    return {
        "final_fhs": final_fhs,
        "sub_scores": {
            "savings_rate_score": round(savings_score, 1),
            "debt_ratio_inverse_score": round(debt_inverse_score, 1),
            "scheme_utilization_score": round(scheme_score, 1),
            "quiz_score": round(quiz_component, 1)
        },
        "metrics": {
            "monthly_income": income,
            "monthly_savings": savings,
            "monthly_debt_emi": emi,
            "savings_rate_pct": round(savings_rate * 100, 1),
            "debt_ratio_pct": round(debt_ratio * 100, 1),
            "schemes_enrolled_count": schemes_count,
            "quiz_score": quiz
        },
        "weights": {
            "weight1_savings": WEIGHT_SAVINGS,
            "weight2_debt_inverse": WEIGHT_DEBT_INVERSE,
            "weight3_scheme_utilization": WEIGHT_SCHEMES,
            "weight4_quiz_score": WEIGHT_QUIZ
        }
    }


def recalculate_and_store_fhs(
    session: Session,
    user_id: int,
    savings: Optional[float] = None,
    debt_emi: Optional[float] = None,
    income: Optional[float] = None,
    quiz_score: Optional[float] = None
) -> Dict[str, Any]:
    """
    Recalculates FHS from database state and updates financial_health_score table.
    """
    fhs = get_or_create_fhs_record(session, user_id)
    profile = session.exec(
        select(UserFinancialProfile).where(UserFinancialProfile.user_id == user_id)
    ).first()
    user = session.exec(select(User).where(User.id == user_id)).first()

    # Count schemes applied / matched in database
    schemes_count = len(session.exec(
        select(UserSchemeMatch).where(UserSchemeMatch.user_id == user_id)
    ).all())

    # Determine monthly income
    if income is not None:
        fhs.monthly_income = income
    elif profile and profile.monthly_income:
        fhs.monthly_income = profile.monthly_income

    if savings is not None:
        fhs.monthly_savings = savings
    if debt_emi is not None:
        fhs.monthly_debt_emi = debt_emi
    if quiz_score is not None:
        fhs.quiz_score = quiz_score
        fhs.quiz_completed = True

    fhs.schemes_enrolled_count = max(schemes_count, fhs.schemes_enrolled_count)

    # Execute math calculation
    calc = compute_fhs_math(
        monthly_income=fhs.monthly_income,
        monthly_savings=fhs.monthly_savings,
        monthly_debt_emi=fhs.monthly_debt_emi,
        schemes_count=fhs.schemes_enrolled_count,
        quiz_score=fhs.quiz_score
    )

    # Persist in financial_health_score table
    fhs.score = calc["final_fhs"]
    fhs.savings_score = calc["sub_scores"]["savings_rate_score"]
    fhs.debt_score = calc["sub_scores"]["debt_ratio_inverse_score"]
    fhs.scheme_score = calc["sub_scores"]["scheme_utilization_score"]
    fhs.savings_rate = calc["metrics"]["savings_rate_pct"] / 100.0
    fhs.debt_ratio = calc["metrics"]["debt_ratio_pct"] / 100.0
    fhs.updated_at = datetime.utcnow()

    session.add(fhs)

    # Synchronize with User table so frontend context reflects immediately
    if user:
        user.financial_health_score = int(fhs.score)
        session.add(user)

    session.commit()
    session.refresh(fhs)

    return calc


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


def calculate_fhs_from_dataframe(df, current_liquid_balance: float, session: Optional[Session] = None, user_id: int = 1):
    df.columns = [c.strip().title() for c in df.columns]
    df['Category'] = df.apply(
        lambda row: categorize_transaction(
            row.get('Description', ''),
            row.get('Amount', 0),
            row.get('Type', '')
        ),
        axis=1
    )
    totals = df.groupby('Category')['Amount'].sum().to_dict()
    income = totals.get('Income', 0) + totals.get('Other_Income', 0) or 50000.0
    savings = totals.get('Savings_Investment', 0)
    emis = totals.get('EMI', 0)

    if session:
        return recalculate_and_store_fhs(
            session=session,
            user_id=user_id,
            savings=savings,
            debt_emi=emis,
            income=income
        )

    # Fallback in-memory
    return compute_fhs_math(
        monthly_income=income,
        monthly_savings=savings,
        monthly_debt_emi=emis,
        schemes_count=1,
        quiz_score=70.0
    )
