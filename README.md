# GPT Google Calendar 연동 Flask 서버

이 프로젝트는 GPT와 Google Calendar를 연동하기 위한 백엔드 API입니다. Render 무료 서버에 배포하여 사용할 수 있습니다.

## 주요 기능

- Google OAuth 2.0 인증
- 일정 조회 (/list-events)
- 일정 생성 (/create-event)
- G메일 조회 (/list_gmail)
 
## 사용법

1. Google Cloud에서 OAuth 클라이언트 생성
2. Render 환경 변수에 CLIENT_ID, CLIENT_SECRET, REDIRECT_URI 설정
3. `/auth` 경로로 이동하여 인증
