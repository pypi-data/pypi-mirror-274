# *-* coding: utf-8 *-*
import os
import logging
import requests
from pydantic import BaseModel
from typing import Optional

from dialog.db import get_session
from dialog_lib.db.models import Chat as ChatEntity
from dialog.llm import process_user_message

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

class WatiWebhookRequest(BaseModel):
    id: str
    created: str
    whatsappMessageId: str
    conversationId: str
    ticketId: str
    text: str
    type: str
    data: Optional[str]
    timestamp: str
    owner: bool
    eventType: str
    statusString: str
    avatarUrl: Optional[str]
    assignedId: str
    operatorName: str
    operatorEmail: str
    waId: str
    messageContact: Optional[str]
    senderName: str
    listReply: Optional[str]
    replyContextId: Optional[str]


wati_router = APIRouter()

@wati_router.post("/webhook")
async def ask_question_to_llm(message: WatiWebhookRequest, session: Session = Depends(get_session)):
    if any([
        message.statusString != "SENT",
        message.eventType != "message",
        message.type != "text"
    ]):
        return {}
    logging.info(f"Received message: {message}")
    recipient_number = message.waId

    chat_instance = session.query(ChatEntity).filter(ChatEntity.session_id == message.conversationId).first()

    if not chat_instance:
        chat_instance = ChatEntity(
            session_id=message.conversationId,
        )
        session.add(chat_instance)
        session.flush()

    ai_message = process_user_message(message.messages[-1].content, chat_id=chat_instance.session_id)
    logging.info(f"AI Message: {ai_message}")

    wati_req = requests.post(
        f"{os.environ.get("WATI_API_ENDPOINT")}/api/v1/sendSessionMessage/{recipient_number}",
        json={
            "message": ai_message["text"]
        },
        headers = {
            "Authorization": os.environ.get("WATI_AUTH_KEY")
        }
    )
    return {
        "message": ai_message["text"]
    }

def register_plugin(app):
    app.include_router(wati_router, prefix="/wati")