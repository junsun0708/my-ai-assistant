"""Handle direct messages (DMs) to the bot."""

import logging
from slack_sdk import WebClient
from slack_bolt import Say

from agent.ai_router import AIRouter
from utils.message_formatter import format_ai_response
from utils.conversation import get_thread_context, parse_conversation_history

logger = logging.getLogger(__name__)

DEFAULT_LOADING_TEXT = "🤔 생각 중입니다..."


def app_messaged_callback(client: WebClient, event: dict, say: Say) -> None:
    """Handle message events (DMs and channel messages)."""
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    event_ts = event.get("ts")
    channel_type = event.get("channel_type")
    
    if channel_type != "im":
        return
    
    thread_ts = event.get("thread_ts") or event_ts
    
    logger.info(f"DM from {user_id} in {channel_id}")
    
    try:
        if thread_ts and thread_ts != event_ts:
            conversation = get_thread_context(client, channel_id, thread_ts)
        else:
            conversation = []
        
        if not text or text.strip() == "":
            say(text="무엇을 도와드릴까요?", thread_ts=thread_ts)
            return
        
        waiting_message = say(text=DEFAULT_LOADING_TEXT, thread_ts=thread_ts)
        
        ai_router = AIRouter()
        response = ai_router.get_response(
            user_id=user_id,
            message=text,
            conversation_history=conversation
        )
        
        formatted_response = format_ai_response(response)
        
        client.chat_update(
            channel=channel_id,
            ts=waiting_message["ts"],
            text=formatted_response
        )
        
    except Exception as e:
        logger.error(f"Error in app_messaged_callback: {e}")
        say(text=f"오류가 발생했습니다: {str(e)}", thread_ts=thread_ts)
