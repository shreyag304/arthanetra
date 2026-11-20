"""
LangGraph Multi-Agent Orchestration for ArthaNetra:
Coordinates the 4 core specialized agents:
1. Context Profiling Agent (Structured non-LLM onboarding & profiling)
2. Scam Detection Agent (2-step fast-filter + LLM pipeline)
3. GovScheme Navigator Agent (Rule-matching + customized application guide)
4. Financial Coach Agent (Personalized financial advice using profile context & LLM)
"""
import re
from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph, END
from sqlmodel import Session, select
from dbmodel.models import User, UserFinancialProfile, ChatMessageHistory
from services.profiling_agent import process_profiling_turn, get_or_create_profile
from services.scam_detector import evaluate_scam, is_scam_followup_query
from services.gov_scheme_navigator import execute_scheme_navigator
from services.financial_coach import execute_financial_coach


class ArthaNetraState(TypedDict):
    session: Any
    user_id: int
    message: str
    language: str
    route: str
    reply: str
    context: Dict[str, Any]
    risk_score: Optional[float]
    eligible_schemes: List[str]


def router_node(state: ArthaNetraState) -> Dict[str, Any]:
    msg = state["message"].lower().strip()
    session = state["session"]
    user_id = state["user_id"]

    profile = get_or_create_profile(session, user_id)

    # 0. Friendly Greetings & Casual acknowledgements (Prevent dumping full financial plans on "hi")
    is_greeting = bool(
        re.search(r"^(?:hi+|hey+|hello+|namaste+|pranam+|good\s*(?:morning|afternoon|evening)|yo|sup)[\s!.,?]*$", msg)
        or re.search(r"^(?:kaise\s*ho|kya\s*hal\s*hai|how\s*are\s*you)[\s!.,?]*$", msg)
    )
    is_acknowledgement = bool(
        re.search(r"^(?:thanks?|thank\s*you|dhanyawad|shukriya|thx)[\s!.,?]*$", msg)
        or re.search(r"^(?:ok+|okay+|got\s*it|alright|fine|cool|sure)[\s!.,?]*$", msg)
    )

    # 1. Direct Scam / Fraud detection
    is_direct_scam = any([
        re.search(r"\b(scam|fraud|fake|suspicious|phishing|legit|is\s*this\s*safe|processing\s*fee|registration\s*fee|lottery|otp|cvv|pin|won\s*prize)\b", msg),
        re.search(r"\b(asking\s*.*(?:fee|money|otp|contact|pin|pay)|double\s*money|urgent\s*basis|urgent\s*.*pay|pay\s*.*urgent|2x\s*money)\b", msg),
        re.search(r"\b(?:pay|give|send|transfer)\s*.*(?:to\s*get|so\s*that|in\s*order\s*to)\s*.*(?:money|double|cash)\b", msg)
    ])

    # 2. Context-aware Scam Follow-Up: If user was previously in scam detection or asking follow-up on safety/paying
    is_scam_followup = (
        (profile.last_route == "scam_detection" or is_scam_followup_query(msg))
        and any([
            re.search(r"\b(should\s*i\s*(?:pay|send|transfer|give)|can\s*i\s*(?:pay|transfer|send)|do\s*i\s*pay)\b", msg),
            re.search(r"\b(or\s*check|how\s*to\s*check|verify|what\s*(?:should|can)\s*i\s*do|what\s*now|what\s*if)\b", msg),
            re.search(r"\b(pay\s*money|transfer\s*money|send\s*money|block|report)\b", msg),
            re.search(r"\b(is\s*it\s*real|is\s*it\s*fake|can\s*i\s*trust|are\s*you\s*sure)\b", msg)
        ])
    )

    # 3. Explicit Government Scheme queries & Follow-ups
    is_scheme_query = any([
        re.search(r"\b(scheme|schemes|yojana|subsidy|sarkari|govt|government\s*aid|pm-kisan|svanidhi|shram|pension|pmjdy)\b", msg)
    ])
    is_scheme_followup = (
        profile.last_route == "gov_scheme"
        and any([
            re.search(r"\b(how\s*to\s*apply|documents?|link|website|portal|first\s*one|second\s*one|third\s*one|eligibility)\b", msg)
        ])
    )

    # 4. Explicit profiling inputs (occupation, language, goal, income)
    is_explicit_profiling = any([
        re.search(r"\b(occupation|work\s*as|job\s*is|my\s*income|earn|earning|preferred\s*language|financial\s*goal|target)\b", msg),
        re.search(r"\b(delivery\s*(?:girl|boy|partner|agent|rider)?|delievry\s*(?:partner)?|dilevry\s*(?:partner)?|delivry\s*(?:partner)?|driver|student|farmer|vendor|hawker|shopkeeper|homemaker|zomato|swiggy|zepto|blinkit)\b", msg)
    ])

    # 5. In-progress profiling answers (short replies when onboarding is active and no specific question asked)
    is_onboarding_answer = (
        not profile.profile_completed
        and not any(q in msg for q in ["how", "what", "why", "can i", "is it", "help me", "tell me"])
        and len(msg.split()) <= 6
    )

    if is_greeting or is_acknowledgement:
        route = "greeting"
    elif is_direct_scam or is_scam_followup:
        route = "scam_detection"
    elif is_scheme_query or is_scheme_followup:
        route = "gov_scheme"
    elif is_explicit_profiling or is_onboarding_answer:
        route = "profiling"
    else:
        route = "financial_coach"

    return {"route": route}


def greeting_node(state: ArthaNetraState) -> Dict[str, Any]:
    msg = state["message"].lower().strip()
    session = state["session"]
    user_id = state["user_id"]
    profile = get_or_create_profile(session, user_id)
    occ = profile.occupation or "Friend"

    if any(w in msg for w in ["thank", "dhanyawad", "shukriya", "thx"]):
        reply = "You're very welcome! Feel free to ask anytime you want to check a scheme, verify a loan offer, or get quick budgeting tips. 😊"
    elif any(w in msg for w in ["ok", "okay", "got it", "alright", "fine", "cool", "sure"]):
        reply = "Sounds good! I'm right here whenever you have any financial questions or need to verify an offer."
    else:
        reply = (
            f"Hello! 👋 Glad you're here.\n\n"
            f"I'm your personal financial companion. How can I help you today? You can ask me about:\n\n"
            f"• 🏛️ **Government Schemes:** Which welfare or loan schemes you qualify for\n"
            f"• 💰 **Smart Budgeting:** Simple, practical ways to save and manage daily expenses\n"
            f"• 🛡️ **Scam & Loan Check:** Checking if a message, loan app, or payment request is safe"
        )

    return {
        "reply": reply,
        "context": state.get("context", {})
    }



def profiling_node(state: ArthaNetraState) -> Dict[str, Any]:
    session = state["session"]
    user_id = state["user_id"]
    message = state["message"]

    reply, context_dict, is_completed = process_profiling_turn(session, user_id, message)
    return {
        "reply": reply,
        "context": context_dict,
    }


def scam_detection_node(state: ArthaNetraState) -> Dict[str, Any]:
    session = state["session"]
    user_id = state["user_id"]
    message = state["message"]
    profile = get_or_create_profile(session, user_id)
    is_followup = bool(profile.last_route == "scam_detection" and is_scam_followup_query(message))

    result = evaluate_scam(session, user_id, message, is_followup=is_followup)
    return {
        "reply": result["reply"],
        "risk_score": result["risk_score"],
        "context": {
            **state.get("context", {}),
            "last_scam_risk": result["risk_score"],
            "last_scam_verdict": result["verdict"]
        }
    }


def gov_scheme_node(state: ArthaNetraState) -> Dict[str, Any]:
    session = state["session"]
    user_id = state["user_id"]
    message = state["message"]
    language = state.get("language") or "English"

    result = execute_scheme_navigator(session, user_id, message, preferred_language=language)
    return {
        "reply": result["reply"],
        "eligible_schemes": result.get("matched_schemes", []),
        "context": {
            **state.get("context", {}),
            "eligible_schemes": result.get("matched_schemes", ["PM Jan Dhan Yojana", "Atal Pension Yojana"])
        }
    }


def financial_coach_node(state: ArthaNetraState) -> Dict[str, Any]:
    session = state["session"]
    user_id = state["user_id"]
    message = state["message"]
    language = state.get("language") or "English"

    result = execute_financial_coach(session, user_id, message, language=language)
    return {
        "reply": result["reply"],
        "context": {
            **state.get("context", {}),
            "persona": result.get("persona_used", "Standard User"),
            "goal": result.get("goal_used", "Budget Optimization"),
            "financial_health_score": result.get("health_score", 75)
        }
    }


def route_decision(state: ArthaNetraState) -> str:
    return state["route"]


# Build the LangGraph StateGraph
def create_arthanetra_graph():
    workflow = StateGraph(ArthaNetraState)

    # Add Nodes
    workflow.add_node("router", router_node)
    workflow.add_node("greeting", greeting_node)
    workflow.add_node("profiling", profiling_node)
    workflow.add_node("scam_detection", scam_detection_node)
    workflow.add_node("gov_scheme", gov_scheme_node)
    workflow.add_node("financial_coach", financial_coach_node)

    # Set Entry Point
    workflow.set_entry_point("router")

    # Add Conditional Edges from Router
    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "greeting": "greeting",
            "profiling": "profiling",
            "scam_detection": "scam_detection",
            "gov_scheme": "gov_scheme",
            "financial_coach": "financial_coach",
        }
    )

    # Terminal Edges to END
    workflow.add_edge("greeting", END)
    workflow.add_edge("profiling", END)
    workflow.add_edge("scam_detection", END)
    workflow.add_edge("gov_scheme", END)
    workflow.add_edge("financial_coach", END)

    return workflow.compile()


arthanetra_graph = create_arthanetra_graph()


def process_agent_message(session: Session, user_id: int, message: str, language: str = "English") -> Dict[str, Any]:
    """
    Synchronous entry point that invokes the LangGraph multi-agent graph.
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    profile = get_or_create_profile(session, user_id)

    initial_context = {
        "persona": user.persona if user and user.persona else (profile.occupation or "Standard User"),
        "income_type": user.income_type if user and user.income_type else "Variable",
        "goal": user.goal if user and user.goal else (profile.financial_goals or "Budget Optimization"),
        "language": language or profile.preferred_language or "English",
        "financial_health_score": user.financial_health_score if user else 75,
        "eligible_schemes": ["PM Jan Dhan Yojana", "Atal Pension Yojana"],
    }

    initial_state: ArthaNetraState = {
        "session": session,
        "user_id": user_id,
        "message": message,
        "language": language,
        "route": "financial_coach",
        "reply": "",
        "context": initial_context,
        "risk_score": None,
        "eligible_schemes": [],
    }

    result = arthanetra_graph.invoke(initial_state)

    final_reply = result.get("reply", "Response processed by ArthaNetra AI.")
    final_route = result.get("route", "financial_coach")
    final_risk = result.get("risk_score")

    # Persist conversational memory and active state
    try:
        # 1. Update user profile active state
        profile.last_route = final_route
        profile.last_user_query = message
        if final_risk is not None:
            profile.last_scam_risk = final_risk
        session.add(profile)

        # 2. Record messages in chat message history
        user_msg = ChatMessageHistory(
            user_id=user_id,
            sender="user",
            message=message,
            route=final_route
        )
        assistant_msg = ChatMessageHistory(
            user_id=user_id,
            sender="assistant",
            message=final_reply,
            route=final_route
        )
        session.add(user_msg)
        session.add(assistant_msg)
        session.commit()
    except Exception as mem_err:
        print(f"[AgentGraph] Note: History tracking commit deferred: {mem_err}")

    return {
        "reply": final_reply,
        "context": result.get("context", initial_context),
        "route": final_route,
        "risk_score": final_risk,
        "eligible_schemes": result.get("eligible_schemes", []),
    }
