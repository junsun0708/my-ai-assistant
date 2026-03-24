"""AI Router - Route requests to Claude or OpenAI."""

import logging
from typing import Optional

from agent.providers.claude_provider import ClaudeProvider
from agent.providers.openai_provider import OpenAIProvider
from agent.web_search import WebSearch

logger = logging.getLogger(__name__)


class AIRouter:
    """Routes AI requests to appropriate provider (Claude or OpenAI)."""
    
    def __init__(self, provider: Optional[str] = None):
        self.default_provider = provider
        self.claude = ClaudeProvider()
        self.openai = OpenAIProvider()
        self.web_search = WebSearch()
    
    def get_response(
        self,
        user_id: str,
        message: str,
        conversation_history: list,
        force_provider: Optional[str] = None
    ) -> dict:
        """Get AI response for the given message."""
        provider = force_provider or self.default_provider or "claude"
        
        if self._needs_web_search(message):
            search_results = self.web_search.search(
                query=message,
                max_results=5
            )
            message = self._inject_search_context(message, search_results)
        else:
            search_results = None
        
        if provider == "openai":
            response = self.openai.generate(
                message=message,
                history=conversation_history
            )
        else:
            response = self.claude.generate(
                message=message,
                history=conversation_history
            )
        
        if search_results:
            response["search_results"] = search_results
        
        return response
    
    def _needs_web_search(self, message: str) -> bool:
        """Determine if message requires web search."""
        search_keywords = [
            "최근", "최신", "뉴스", "오늘", "어제",
            "latest", "recent", "news", "today", "current",
            "검색", "search", "찾아줘", "알려줘"
        ]
        return any(kw in message.lower() for kw in search_keywords)
    
    def _inject_search_context(self, message: str, search_results: list) -> str:
        """Inject search results as context for the AI."""
        if not search_results:
            return message
        
        context = "\n\n[웹 검색 결과]\n"
        for i, result in enumerate(search_results[:3], 1):
            context += f"{i}. {result['title']}\n"
            context += f"   {result['content'][:200]}...\n"
            context += f"   출처: {result['url']}\n\n"
        
        return f"{message}\n\n{context}[위 검색 결과를 참고하여 답변해주세요.]"
    
    def switch_provider(self, provider: str) -> bool:
        """Switch default AI provider."""
        if provider in ["claude", "openai"]:
            self.default_provider = provider
            return True
        return False
