"""Handle app home opened event."""

import logging
from slack_sdk import WebClient

logger = logging.getLogger(__name__)


def app_home_opened_callback(client: WebClient, event: dict) -> None:
    """Handle app_home_opened event - update app home view."""
    user_id = event.get("user")
    
    logger.info(f"App home opened by {user_id}")
    
    try:
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🤖 My AI Assistant",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "안녕하세요! 저는 AI 어시스턴트입니다.\n\n*사용 방법:*\n• 이 채널에 메시지를 보내거나\n• @mention으로 언급해주세요"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*지원 기능:*\n• Claude (기본 AI)\n• OpenAI\n• 웹 검색 (최신 정보)\n• 대화 맥락 유지"
                        }
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing app home: {e}")
