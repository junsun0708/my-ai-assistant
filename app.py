"""
my-ai-assistant - Slack AI Chatbot with Claude & OpenAI

Slack Bot that responds to messages in my-ai private channel.
Supports both Claude (subscription/API) and OpenAI API.
"""

import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config.settings import Settings
from listeners.events import register as register_events
from listeners.commands import register as register_commands

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> App:
    """Create and configure Slack Bolt app."""
    settings = Settings()
    
    app = App(
        token=settings.slack_bot_token,
        signing_secret=settings.slack_signing_secret,
    )
    
    # Register event listeners
    register_events(app)
    
    # Register command listeners
    register_commands(app)
    
    return app


if __name__ == "__main__":
    settings = Settings()
    app = create_app()
    
    logger.info("Starting my-ai-assistant...")
    logger.info(f"Target channel: {settings.target_channel}")
    logger.info(f"Default AI provider: {settings.default_provider}")
    
    SocketModeHandler(
        app, 
        settings.slack_app_token
    ).start()
