"""
Seeds curated local dataset of Indian Government Schemes into the database.
Works completely offline without external API dependency.
"""
from sqlmodel import Session, select
from dbmodel.models import GovtScheme

DEFAULT_SCHEMES = [
    GovtScheme(
        scheme_name="PM SVANidhi (Street Vendor / Gig Micro-Credit)",
        description="Special Micro-Credit Facility providing affordable working capital loans for gig delivery workers, street vendors, and urban self-employed.",
        category="Gig & Urban Livelihood",
        min_age=18,
        max_age=65,
        requires_land=False,
        max_income=300000.0,
        target_occupations="delivery,delivery girl,delivery boy,gig worker,zomato,swiggy,zepto,blinkit,driver,vendor,hawker,informal",
        benefits="Initial working capital loan of ₹10,000, progressing to ₹20,000 and ₹50,000 upon timely repayment. 7% annual interest subsidy and cash-back on digital transactions up to ₹1,200/year.",
        required_documents="1. Aadhaar Card (mobile linked), 2. Identity Card / Delivery Partner ID / Urban Local Body letter, 3. Bank Account details (IFSC / Account No)."
    ),
    GovtScheme(
        scheme_name="e-Shram Social Security Scheme",
        description="National database and social security umbrella for gig workers, unorganized workers, and delivery partners across India.",
        category="Social Security & Insurance",
        min_age=16,
        max_age=59,
        requires_land=False,
        max_income=400000.0,
        target_occupations="delivery,delivery girl,delivery boy,gig worker,driver,construction,domestic worker,labour,informal,freelancer",
        benefits="Free 12-digit Universal Account Number (UAN), accidental insurance cover of ₹2 Lakh in case of death or permanent disability, access to central welfare funds.",
        required_documents="1. Aadhaar Card, 2. Active mobile number linked to Aadhaar, 3. Bank account passbook / statement."
    ),
    GovtScheme(
        scheme_name="Atal Pension Yojana (APY)",
        description="Guaranteed pension scheme for workers in the unorganized and gig economy sectors to ensure financial independence after retirement.",
        category="Pension & Retirement",
        min_age=18,
        max_age=40,
        requires_land=False,
        max_income=None,
        target_occupations="delivery,delivery girl,delivery boy,gig worker,vendor,driver,shopkeeper,student,informal,all",
        benefits="Guaranteed monthly pension between ₹1,000 and ₹5,000 starting from age 60. Same pension amount is transferred to spouse upon subscriber's death.",
        required_documents="1. Savings Bank Account, 2. Aadhaar Card, 3. Mobile Number."
    ),
    GovtScheme(
        scheme_name="Pradhan Mantri Jan Dhan Yojana (PMJDY)",
        description="National Mission for Financial Inclusion providing universal banking access with zero-balance savings accounts.",
        category="Financial Inclusion",
        min_age=10,
        max_age=None,
        requires_land=False,
        max_income=None,
        target_occupations="all,student,delivery,gig worker,farmer,unemployed,homemaker",
        benefits="Zero minimum balance savings account, free RuPay debit card with ₹2 Lakh accidental insurance cover, ₹10,000 overdraft facility for eligible active accounts.",
        required_documents="1. Aadhaar Card (or Voter ID / Driving License), 2. Passport size photographs."
    ),
    GovtScheme(
        scheme_name="PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        description="Income support scheme for small and marginal landholding farmer families.",
        category="Agriculture",
        min_age=18,
        max_age=None,
        requires_land=True,
        max_income=None,
        target_occupations="farmer,cultivator,agriculture,landowner",
        benefits="Financial benefit of ₹6,000 per year per family payable in three equal four-monthly installments of ₹2,000 directly into bank accounts via DBT.",
        required_documents="1. Aadhaar Card, 2. Land ownership papers (Khasra / Khatauni / Record of Rights), 3. Active Bank Account details."
    ),
    GovtScheme(
        scheme_name="Pradhan Mantri Mudra Yojana (PMMY - Shishu / Kishore)",
        description="Collateral-free micro-enterprise loans for individuals starting or expanding small businesses, vehicles, or trading services.",
        category="Business & Micro-Credit",
        min_age=18,
        max_age=65,
        requires_land=False,
        max_income=None,
        target_occupations="business,shop,delivery,vendor,driver,entrepreneur,freelancer",
        benefits="Loans up to ₹50,000 (Shishu) and up to ₹5,00,000 (Kishore) with zero collateral and affordable commercial rates for business assets / equipment.",
        required_documents="1. Identity & Address proof (Aadhaar/Voter ID), 2. Business quotation or registration proof, 3. 6 months bank statement."
    ),
]


def seed_schemes_if_empty(session: Session):
    existing = session.exec(select(GovtScheme)).first()
    if not existing:
        for s in DEFAULT_SCHEMES:
            session.add(s)
        session.commit()

