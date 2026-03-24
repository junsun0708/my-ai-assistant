"""Conversation history utilities."""

from typing import List, Optional
from slack_sdk import WebClient

from config.settings import settings


def get_thread_context(
    client: WebClient,
    channel_id: str,
    thread_ts: str
) -> List[dict]:
    """Get conversation history from a thread."""
    try:
        result = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts,
            limit=settings.max_conversation_history + 10
        )
        
        messages = result.get("messages", [])
        
        return parse_conversation_history(messages)
        
    except Exception as e:
        return []


def parse_conversation_history(messages: List[dict]) -> List[dict]:
    """Parse Slack messages into conversation format."""
    conversation = []
    
    for msg in messages:
        role = msg.get("role")
        if not role:
            role = "assistant" if msg.get("ts", "").startswith("bot_") else "user"
        
        content = msg.get("content") or msg.get("text", "")
        
        if isinstance(content, dict):
            content = content.get("text", str(content))
        elif not isinstance(content, str):
            content = str(content)
        
        if content and role:
            conversation.append({
                "role": role,
                "content": content,
                "ts": msg.get("ts")
            })
    
    return conversation


def should_include_in_context(msg: dict, bot_user_id: Optional[str] = None) -> bool:
    """Determine if message should be included in context."""
    if msg.get("subtype") == "bot_message":
        return False
    
    if msg.get("user") == bot_user_id:
        return False
    
    content = msg.get("content") or msg.get("text", "")
    if not content:
        return False
    
    return True
