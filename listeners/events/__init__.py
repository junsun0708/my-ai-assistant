"""Event listeners for Slack events."""

from slack_bolt import App
from typing import Callable

from listeners.events.app_mentioned import app_mentioned_callback
from listeners.events.app_messaged import app_messaged_callback
from listeners.events.app_home import app_home_opened_callback


def register(app: App) -> None:
    """Register all event listeners with the app."""
    
    app.event("app_mention")(app_mentioned_callback)
    
    app.event("message")(app_messaged_callback)
    
    app.event("app_home_opened")(app_home_opened_callback)
