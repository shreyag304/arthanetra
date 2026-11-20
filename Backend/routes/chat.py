from typing import Optional, Dict, Any, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlmodel import Session
from pydantic import BaseModel
from dbmodel.Database import get_db, engine
from services.agent_graph import process_agent_message

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
    user_id = payload.user_id or 1
    result = process_agent_message(
        session=db,
        user_id=user_id,
        message=payload.message,
        language=payload.language or "English",
    )

    return ChatResponse(
        message="Chat processed successfully",
        reply=result["reply"],
        user_id=payload.user_id,
        conversation_id=payload.conversation_id,
        language=payload.language,
        context=result["context"],
        request_id=payload.request_id,
    )


async def process_chat_websocket(websocket: WebSocket):
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

            with Session(engine) as session:
                user_id = payload.user_id or 1
                result = process_agent_message(
                    session=session,
                    user_id=user_id,
                    message=payload.message,
                    language=payload.language or "English",
                )

            response = ChatResponse(
                message="Chat processed successfully via WebSocket",
                reply=result["reply"],
                user_id=payload.user_id,
                conversation_id=payload.conversation_id,
                language=payload.language,
                context=result["context"],
                request_id=payload.request_id,
            )

            await manager.send_personal_message(response.model_dump(), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


@router.websocket("/ws")
async def chat_websocket_subpath(websocket: WebSocket):
    await process_chat_websocket(websocket)


@ws_router.websocket("/ws/chat")
async def chat_websocket_root(websocket: WebSocket):
    await process_chat_websocket(websocket)

