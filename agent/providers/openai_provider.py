"""OpenAI AI Provider - requires API key."""

import logging
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from config.settings import settings

logger = logging.getLogger(__name__)


class OpenAIProvider:
    """OpenAI API provider."""
    
    def __init__(self):
        self.api_key = settings.openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.model = settings.openai_model
        
        if OpenAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("OpenAI provider not configured - no API key found")
    
    def generate(
        self,
        message: str,
        history: list,
        system_prompt: Optional[str] = None
    ) -> dict:
        """Generate response from OpenAI."""
        if not self.client:
            return {
                "text": "OpenAI가 설정되지 않았습니다. OPENAI_API_KEY를 설정해주세요.",
                "provider": "openai",
                "error": True
            }
        
        system = system_prompt or (
            "당신은 도움이 되는 AI 어시스턴트입니다. "
            "한국어로 친절하게 답변해주세요."
        )
        
        messages = self._build_messages(history, message, system)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4096,
                temperature=0.7
            )
            
            return {
                "text": response.choices[0].message.content,
                "provider": "openai",
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens
                }
            }
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "text": f"OpenAI API 오류: {str(e)}",
                "provider": "openai",
                "error": True
            }
    
    def _build_messages(self, history: list, new_message: str, system: str) -> list:
        """Build message list from conversation history."""
        messages = [{"role": "system", "content": system}]
        
        for msg in history[-settings.max_conversation_history:]:
            role = "assistant" if msg.get("role") == "assistant" else "user"
            messages.append({
                "role": role,
                "content": msg.get("content", "")
            })
        
        messages.append({"role": "user", "content": new_message})
        
        return messages
