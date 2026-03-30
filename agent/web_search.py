"""Web Search using Tavily - date-aware search."""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

from config.settings import settings

logger = logging.getLogger(__name__)


class WebSearch:
    """Tavily-powered web search with date filtering."""
    
    def __init__(self):
        self.api_key = settings.tavily_api_key or os.environ.get("TAVILY_API_KEY")
        self.enabled = settings.web_search_enabled and self.api_key
        
        if TavilyClient and self.api_key:
            self.client = TavilyClient(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("Web search not configured - Tavily API key not found")
    
    def search(
        self,
        query: str,
        max_results: int = 5,
        time_range: str = "week"
    ) -> list:
        """Search the web with date awareness."""
        if not self.client:
            return []
        
        date_aware_query = f"{query} {datetime.now().strftime('%Y-%m')}"
        
        try:
            response = self.client.search(
                query=date_aware_query,
                search_depth="advanced",
                topic="news",
                time_range=time_range,
                max_results=max_results,
                include_answer=True,
                include_raw_content=False
            )
            
            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "published_date": item.get("published_date", "recent")
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Tavily search error: {e}")
            return []
    
    def search_with_date_range(
        self,
        query: str,
        start_date: str,
        end_date: Optional[str] = None,
        max_results: int = 5
    ) -> list:
        """Search with specific date range."""
        if not self.client:
            return []
        
        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                start_date=start_date,
                end_date=end_date or datetime.now().strftime("%Y-%m-%d"),
                max_results=max_results,
                include_answer=True
            )
            
            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "published_date": item.get("published_date", start_date)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Tavily date-range search error: {e}")
            return []
