"""Message formatting utilities for Slack responses."""

import re
from typing import Optional


def format_ai_response(response: dict) -> str:
    """Format AI response for Slack display."""
    if response.get("error"):
        return response.get("text", "오류가 발생했습니다.")
    
    text = response.get("text", "")
    
    formatted = clean_markdown(text)
    
    if len(formatted) > 4000:
        formatted = formatted[:3997] + "..."
    
    return formatted


def clean_markdown(text: str) -> str:
    """Convert markdown to Slack-compatible formatting."""
    text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', text)
    
    text = re.sub(r'\*(.+?)\*', r'_\1_', text)
    
    text = re.sub(r'```(\w+)?\n?', '```', text)
    
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        if re.match(r'^#{1,6}\s', line):
            line = re.sub(r'^#+\s', '• ', line)
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)


def extract_code_blocks(text: str) -> list:
    """Extract code blocks from markdown text."""
    pattern = r'```(\w+)?\n?(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [{'language': m[0], 'code': m[1].strip()} for m in matches]


def create_blocks(text: str, source_url: Optional[str] = None) -> list:
    """Create Slack Block Kit blocks from text."""
    blocks = []
    
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    })
    
    if source_url:
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"출처: <{source_url}|{source_url}>"
                }
            ]
        })
    
    return blocks
