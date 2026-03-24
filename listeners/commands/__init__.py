"""Command listeners package."""
from slack_bolt import App


def register(app: App) -> None:
    """Register slash commands."""
    app.command("/ai-help")(ai_help_command)


def ai_help_command(ack, respond) -> None:
    """Handle /ai-help command."""
    ack()
    respond(
        text="*My AI Assistant 도움말*\n\n"
        "• `@my-ai [질문]` - AI에게 질문하기\n"
        "• DM으로 직접 메시지 보내기\n"
        "• `/ai-help` - 이 도움말 표시\n\n"
        "*AI 모델 전환:*\n"
        "• `@my-ai /model claude` - Claude 사용\n"
        "• `@my-ai /model openai` - OpenAI 사용\n\n"
        "*웹 검색:*\n"
        "• 자동으로 최신 정보를 검색합니다"
    )
