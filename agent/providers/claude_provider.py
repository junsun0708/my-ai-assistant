"""Claude AI Provider - supports API key or subscription-based auth."""

import os
import logging
from typing import Optional

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from config.settings import settings

logger = logging.getLogger(__name__)


class ClaudeProvider:
    """Claude AI provider with support for API key or subscription auth."""
    
    def __init__(self):
        self.api_key = settings.anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = settings.anthropic_model
        
        if Anthropic and self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        elif Anthropic:
            self.client = Anthropic()
        else:
            self.client = None
            logger.warning("Claude provider not configured - no API key found")
    
    def generate(
        self,
        message: str,
        history: list,
        system_prompt: Optional[str] = None
    ) -> dict:
        """Generate response from Claude."""
        if not self.client:
            return {
                "text": "Claude가 설정되지 않았습니다. ANTHROPIC_API_KEY를 설정해주세요.",
                "provider": "claude",
                "error": True
            }
        
        system = system_prompt or (
            "당신은 도움이 되는 AI 어시스턴트입니다. "
            "한국어로 친절하게 답변해주세요. "
            "필요한 경우 웹 검색 결과를 참고하여 답변하세요."
        )
        
        messages = self._build_messages(history, message)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system,
                messages=messages
            )
            
            return {
                "text": response.content[0].text,
                "provider": "claude",
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return {
                "text": f"Claude API 오류: {str(e)}",
                "provider": "claude",
                "error": True
            }
    
    def _build_messages(self, history: list, new_message: str) -> list:
        """Build message list from conversation history."""
        messages = []
        
        for msg in history[-settings.max_conversation_history:]:
            role = "assistant" if msg.get("role") == "assistant" else "user"
            messages.append({
                "role": role,
                "content": msg.get("content", "")
            })
        
        messages.append({"role": "user", "content": new_message})
        
        return messages
