# My AI Assistant

Slack AI 챗봇 - Claude + OpenAI + 웹 검색

## 주요 기능

- **다중 AI 지원**: Claude (구독/API) 및 OpenAI API
- **웹 검색**: Tavily API를 통한 최신 정보 검색 (날짜 필터링)
- **스레드 대화**: 이전 대화 맥락 유지
- **Private Channel**: `my-ai` 채널에서 동작

## 사전 요구사항

- Python 3.10+
- Slack Workspace 관리자 권한
- 다음 중 하나:
  - Claude Pro/Max 구독 OR Anthropic API 키
  - OpenAI API 키

## 설치

```bash
cd my-ai-assistant

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Slack App 설정

1. [Slack API](https://api.slack.com/)에서 새 앱 생성
2. **Socket Mode** 활성화
3. **App Token** 생성 (`xapp-`로 시작)
4. **Bot Token** 생성 (`xoxb-`로 시작)
5. **Event Subscriptions** 설정:
   - `app_mention` 구독
   - `message.channels` 구독
6. **Permissions** 설정:
   - `app_mentions:read`
   - `channels:history`
   - `chat:write`
   - `im:history`
   - `im:read`

## 환경 설정

```bash
cp .env.example .env
```

`.env` 파일을 편집:

```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_SIGNING_SECRET=...

ANTHROPIC_API_KEY=sk-ant-...  # 또는 비워두기 (CLI 구독 사용)
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

## 실행

```bash
# 개발 모드
python app.py

# 또는
bolt run
```

## 사용 방법

1. Slack에서 `my-ai` 비공개 채널 생성 (또는 기존 채널 사용)
2. Bot을 채널에 초대
3. 채널에서 `@my-ai [질문]` 또는 DM으로 질문

## AI 모델 전환

기본값은 Claude입니다. OpenAI 사용 시:

```python
# app.py에서 기본값 변경
default_provider = "openai"
```

## 비용

| 서비스 | 비용 |
|--------|------|
| Claude 구독 | $20/월 (Pro) |
| Claude API | 사용량 기반 |
| OpenAI API | 사용량 기반 (약 $0.075/1M tokens) |
| Tavily | 무료 tier 있음 |

## 라이선스

MIT
