from typing import Optional, Dict, Any, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from sqlmodel import Session
from dbmodel.Database import get_db
from dbmodel.models import User

router = APIRouter(prefix="/chat", tags=["chat"])
ws_router = APIRouter(tags=["chat-websocket"])


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None
    conversation_id: Optional[str] = None
    language: Optional[str] = "English"
    request_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    reply: str
    user_id: Optional[int] = None
    conversation_id: Optional[str] = None
    language: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@router.post("", response_model=ChatResponse)
def handle_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    reply_text = f"ArthaNetra AI ({payload.language or 'English'}): I received your message '{payload.message}'."
    
    fhs_score = 75
    if payload.user_id:
        reply_text += f" Assisting User ID #{payload.user_id}."
        user = db.get(User, payload.user_id)
        if user and user.fhs_score is not None:
            fhs_score = user.fhs_score

    default_context = {
        "financial_health_score": fhs_score,
        "persona": "Standard User",
        "income_type": "Variable",
        "language": payload.language or "English",
        "goal": "Budget Optimization",
        "eligible_schemes": ["PM Jan Dhan Yojana", "Atal Pension Yojana"],
    }

    return ChatResponse(
        message="Chat processed successfully",
        reply=reply_text,
        user_id=payload.user_id,
        conversation_id=payload.conversation_id,
        language=payload.language,
        context=default_context,
        request_id=payload.request_id,
    )


async def process_chat_websocket(websocket: WebSocket, db: Session):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            try:
                payload = ChatRequest(**data)
            except Exception as validation_error:
                req_id = data.get("request_id") if isinstance(data, dict) else None
                await manager.send_personal_message(
                    {
                        "error": "Invalid request payload format",
                        "detail": str(validation_error),
                        "request_id": req_id,
                    },
                    websocket,
                )
                continue

            reply_text = f"ArthaNetra AI ({payload.language or 'English'}): I received your message '{payload.message}'."
            
            fhs_score = 75
            if payload.user_id:
                reply_text += f" Assisting User ID #{payload.user_id}."
                user = db.get(User, payload.user_id)
                if user and user.fhs_score is not None:
                    fhs_score = user.fhs_score

            msg_lower = payload.message.lower()
            default_context = {
                "financial_health_score": fhs_score,
                "persona": "Standard User",
                "income_type": "Variable",
                "language": payload.language or "English",
                "goal": "Budget Optimization",
                "eligible_schemes": ["PM Jan Dhan Yojana", "Atal Pension Yojana"],
            }

            if "loan" in msg_lower or "scam" in msg_lower:
                reply_text = (
                    "This loan appears risky. Please verify if the lender is RBI registered before proceeding."
                )
            elif "budget" in msg_lower or "save" in msg_lower:
                reply_text = "Let's create a monthly budget. First, tell me your monthly income."
            elif "scheme" in msg_lower:
                reply_text = "Based on your profile, you may be eligible for PM-KISAN and PM Jan Dhan Yojana."
                default_context["eligible_schemes"] = ["PM-KISAN", "PM Jan Dhan Yojana"]
            elif "health score" in msg_lower:
                reply_text = (
                    "Your Financial Health Score is currently 75. Increasing savings and reducing debt can improve it."
                )

            response = ChatResponse(
                message="Chat processed successfully via WebSocket",
                reply=reply_text,
                user_id=payload.user_id,
                conversation_id=payload.conversation_id,
                language=payload.language,
                context=default_context,
                request_id=payload.request_id,
            )

            await manager.send_personal_message(response.model_dump(), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


@router.websocket("/ws")
async def chat_websocket_subpath(websocket: WebSocket, db: Session = Depends(get_db)):
    await process_chat_websocket(websocket, db)


@ws_router.websocket("/ws/chat")
async def chat_websocket_root(websocket: WebSocket, db: Session = Depends(get_db)):
    await process_chat_websocket(websocket, db)
