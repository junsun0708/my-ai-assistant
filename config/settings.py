"""
Configuration settings for my-ai-assistant.
Manages environment variables and app configuration.
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Slack Configuration
    slack_bot_token: str = ""  # Bot User OAuth Token (xoxb-...)
    slack_app_token: str = ""  # App-Level Token (xapp-...)
    slack_signing_secret: str = ""
    target_channel: str = "my-ai"  # Target channel name or ID
    
    # AI Provider Configuration
    default_provider: str = "claude"  # "claude" or "openai"
    
    # Anthropic (Claude) Configuration
    # Can use API key OR rely on Claude CLI subscription
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-sonnet-4-20250514"
    
    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    
    # Tavily Web Search Configuration
    tavily_api_key: str = ""
    web_search_enabled: bool = True
    
    # Behavior Settings
    max_conversation_history: int = 20  # Max messages to keep in context
    streaming_enabled: bool = True  # Enable streaming responses
    thinking_indicator: bool = True  # Show "thinking..." status
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    def get_claude_config(self) -> dict:
        """Get Claude configuration dict."""
        config = {
            "model": self.anthropic_model,
        }
        if self.anthropic_api_key:
            config["api_key"] = self.anthropic_api_key
        return config
    
    def get_openai_config(self) -> dict:
        """Get OpenAI configuration dict."""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
        }


# Global settings instance
settings = Settings()
