"""
Scam Detection Agent:
2-step pipeline:
Step 1 — Fast filter (always runs in milliseconds via regex). If high confidence scam detected, LLM is bypassed.
Step 2 — Sent to LLM (runs only if Step 1 is unsure). Combines LLM confidence with keyword score into risk score (0-100).
Step 3 — Decision & Storage: Stored in scam_reports table (report_id, user_id, risk_score, flagged_text, reasoning).
"""
import re
from typing import Optional, Dict, Any, Tuple
from sqlmodel import Session
from dbmodel.models import ScamReport
from services.llm_service import llm_client

# Fast Filter Regex Signatures
HIGH_RISK_PATTERNS = [
    # Demanding upfront processing fee before loan disbursement
    (
        r"(?:processing|file|approval|advance|registration|verification|security)\s*(?:fee|charge|deposit|amount|cost)\s*(?:of|is|rs\.?|₹|\d+|before)",
        95.0,
        "Lender demanding upfront processing/registration fees before disbursing loan (Classic predatory loan scam; legitimate RBI banks deduct fees directly from loan proceeds)."
    ),
    # Demanding sensitive authentication (OTP / PIN / CVV / Password)
    (
        r"(?:send|share|tell|give|enter|provide)\s*(?:me|us|your)?\s*(?:the)?\s*(?:otp|pin|password|cvv|upi\s*pin)",
        98.0,
        "Requesting OTP, UPI PIN, or bank passwords. Legitimate bank staff and platforms NEVER ask for your OTP or PIN."
    ),
    # Guaranteed impossible investment returns / Doubling money / 2x returns
    (
        r"\b(?:double|triple|2x|3x|multifold)\s*(?:my|your|the)?\s*money\b|\b(?:get|give|pay|earn)\s*(?:double|triple)\b|\b100%\s*guaranteed\s*(?:profit|return)|invest\s*(?:rs\.?|₹|\d+[kK]?|\d+)\s*.*(?:get|earn)\s*(?:rs\.?|₹|\d+[kK]?|\d+)",
        98.0,
        "Unrealistic promise of doubling or multiplying money (Classic Ponzi / advance-fee fraud). Legitimate regulated investments can never guarantee instant 100% doubled returns."
    ),
    # Urgent demands to pay/transfer money for future reward
    (
        r"\b(?:pay|send|transfer|deposit)\s*(?:rs\.?|₹|\d+[kK]?|\d+)?\s*(?:on\s*urgent\s*basis|urgently|immediately|today)\b|\b(?:urgent|urgently)\s*.*(?:pay|send|transfer|deposit)\b",
        92.0,
        "High-pressure urgency tactics demanding immediate money transfer (Classic social engineering scam designed to bypass critical thinking)."
    ),
    # Pay X to get Y
    (
        r"\b(?:pay|give|send|transfer)\s*(?:rs\.?|₹|\d+[kK]?|\d+)?\s*.*(?:so\s*that|to\s*get|in\s*order\s*to\s*get)\s*.*(?:money|double|loan|cash|prize)\b",
        96.0,
        "Advance-fee scam: Demanding upfront money with a false promise of releasing higher funds, prizes, or doubled returns."
    ),
    # Suspicious contact list / gallery access for instant loan apps
    (
        r"(?:permission|access)\s*(?:to|for)?\s*(?:contact|contacts|gallery|photos|media|location)\s*(?:required|mandatory|to\s*get\s*loan)",
        90.0,
        "App demanding contact list and gallery permissions for loan approval (Signature of unauthorized Chinese / predatory blackmail lending apps)."
    ),
    # Impersonation & Arrest Threats (Digital Arrest / Customs / Electricity)
    (
        r"(?:electricity|power)\s*(?:will\s*be\s*cut|disconnected)|(?:cbi|police|customs|narcotics)\s*(?:arrest|warrant|parcel\s*seized)",
        95.0,
        "Threatening immediate utility disconnection or police arrest over SMS/WhatsApp (High-risk extortion scam)."
    ),
]

MEDIUM_RISK_PATTERNS = [
    (r"\b(?:instant\s*loan|no\s*cibil|no\s*document|within\s*5\s*minutes)\b", 45.0, "Suspicious no-documentation instant loan offer."),
    (r"\b(?:won|winner|lottery|lucky\s*draw|kbc|car\s*prize)\b", 60.0, "Unsolicited lottery or prize reward notification."),
    (r"\b(?:part-time\s*job|like\s*youtube|telegram\s*task|earn\s*from\s*home\s*daily)\b", 65.0, "Work-from-home Telegram task scam signature."),
    (r"\b(?:download\s*apk|install\s*anydesk|teamviewer|rustdesk)\b", 70.0, "Requesting installation of remote control app or unknown APK file."),
]


def fast_filter(text: str) -> Tuple[float, Optional[str], bool]:
    """
    Step 1 — Fast filter (always runs, takes milliseconds).
    Returns (risk_score, reasoning, is_decisive_scam)
    """
    text_lower = text.lower()

    # Check high-risk first
    for pattern, score, reason in HIGH_RISK_PATTERNS:
        if re.search(pattern, text_lower):
            return score, reason, True  # Decisive scam, bypass LLM!

    # Check medium-risk
    max_score = 0.0
    matched_reason = None
    for pattern, score, reason in MEDIUM_RISK_PATTERNS:
        if re.search(pattern, text_lower):
            if score > max_score:
                max_score = score
                matched_reason = reason

    if max_score > 0:
        return max_score, matched_reason, False  # Unsure -> Needs Step 2 LLM

    # Low risk / Clean text
    return 10.0, "No obvious scam keywords or suspicious demands detected.", False


def is_scam_followup_query(text: str) -> bool:
    t = text.lower()
    return any([
        re.search(r"\b(?:should\s*i\s*(?:pay|send|transfer|give)|can\s*i\s*(?:pay|transfer|send)|do\s*i\s*pay)\b", t),
        re.search(r"\b(?:or\s*check|how\s*to\s*check|how\s*(?:can|do)\s*i\s*verify|where\s*to\s*verify|how\s*to\s*know)\b", t),
        re.search(r"\b(?:what\s*(?:should|can)\s*i\s*do|what\s*if\s*i\s*(?:already|paid|sent)|what\s*now)\b", t),
        re.search(r"\b(?:is\s*it\s*real|is\s*it\s*fake|can\s*i\s*trust|are\s*you\s*sure|legit)\b", t),
    ])


def evaluate_scam(session: Session, user_id: Optional[int], message: str, is_followup: bool = False) -> Dict[str, Any]:
    """
    Executes the full 3-step scam detection pipeline with conversational follow-up memory.
    """
    # Check if this is an action follow-up question (e.g. "should i pay money now or check")
    has_explicit_scam_payload = any(k in message.lower() for k in ["double money", "2x money", "lottery", "processing fee", "asking me to pay"])
    
    if is_followup or (is_scam_followup_query(message) and not has_explicit_scam_payload):
        verdict = "SCAM"
        risk_score = 98.0
        reasoning = "User following up on previously flagged advance-fee/Ponzi scam or high-pressure payment demand."
        reply = (
            "🛑 **ABSOLUTELY DO NOT PAY ANY MONEY.**\n\n"
            "• **Direct Answer:** **NO**, do not send or transfer any money. Anyone demanding urgent money with the promise of 'doubling' returns or releasing loans is 100% running a fraud.\n\n"
            "• 🔍 **How to Check / Verify:**\n"
            "  1. Check if the entity is registered on the RBI official portal: **sachet.rbi.org.in**.\n"
            "  2. Genuine institutions never demand personal UPI transfers or advance deposits.\n\n"
            "• 🛡️ **What You Should Do Right Now:**\n"
            "  1. **Block** the caller/sender immediately on WhatsApp and phone.\n"
            "  2. **Do not click** any payment links or share OTP / screen-share.\n"
            "  3. Report the fraudulent number or UPI ID directly at **cybercrime.gov.in** or dial helpline **1930**."
        )
        return {
            "report_id": None,
            "risk_score": risk_score,
            "verdict": verdict,
            "reasoning": reasoning,
            "reply": reply,
            "detection_source": "scam_followup_guard"
        }

    # Step 1: Fast filter
    fast_score, fast_reason, is_decisive = fast_filter(message)

    if is_decisive:
        # Step 1 caught high-confidence scam! LLM does NOT come into picture
        risk_score = fast_score
        reasoning = fast_reason
        detection_source = "fast_filter"
        verdict = "SCAM"
    else:
        # Step 2: Unsure or medium risk -> evaluate with LLM
        detection_source = "llm_analysis"
        llm_prompt = (
            f"Analyze the following user-submitted message or offer for financial fraud/scam risk:\n\n"
            f"Message: \"{message}\"\n\n"
            f"Keyword scan detected preliminary score: {fast_score}/100 with reason: {fast_reason}.\n\n"
            f"Respond concisely with:\n"
            f"1. Risk Score: (a number between 0 and 100)\n"
            f"2. Verdict: (LOW_RISK or HIGH_RISK)\n"
            f"3. Reasoning: (2-3 sentences explaining why it is safe or a scam, citing red flags if any)."
        )
        llm_output = llm_client.generate(llm_prompt)

        # Parse score from LLM output
        score_match = re.search(r"risk\s*score\s*:\s*(\d{1,3})", llm_output, re.IGNORECASE)
        llm_score = float(score_match.group(1)) if score_match else fast_score

        # Combine Step 1 keyword score and LLM score (50/50 blend)
        risk_score = round((fast_score * 0.4) + (llm_score * 0.6), 1)
        verdict = "SCAM" if risk_score >= 60.0 else ("HIGH_RISK" if risk_score >= 40.0 else "LOW_RISK")
        reasoning = llm_output

    # Step 3: Decision & Storage in scam_reports table
    report = ScamReport(
        user_id=user_id,
        risk_score=risk_score,
        verdict=verdict,
        flagged_text=message[:500],
        reasoning=reasoning[:1000],
        detection_source=detection_source
    )
    session.add(report)
    session.commit()
    session.refresh(report)

    # User-facing structured response
    if verdict in ["SCAM", "HIGH_RISK"]:
        reply = (
            f"🚨 **SCAM ALERT: HIGH RISK DETECTED (Risk Score: {risk_score}/100)**\n\n"
            f"**Why this is dangerous:**\n{reasoning}\n\n"
            f"🛑 **Crucial Safety Actions:**\n"
            f"1. **DO NOT pay any advance fees, processing charges, or deposits.**\n"
            f"2. **NEVER share your OTP, UPI PIN, or bank credentials.**\n"
            f"3. Verify if the entity is registered on the official RBI list of NBFCs.\n"
            f"4. You can report financial cybercrime immediately at **cybercrime.gov.in** or call **1930**."
        )
    else:
        reply = (
            f"🛡️ **Scam Scan: Low Risk (Risk Score: {risk_score}/100)**\n\n"
            f"{reasoning}\n\n"
            f"💡 **Tip:** Always check official app stores and ensure bank transactions are done only via authorized banking apps."
        )

    return {
        "report_id": report.report_id,
        "risk_score": risk_score,
        "verdict": verdict,
        "reasoning": reasoning,
        "reply": reply,
        "detection_source": detection_source
    }

