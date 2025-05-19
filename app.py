from flask import Flask, request, redirect, jsonify
import os
import requests

app = Flask(__name__)

# 환경 변수
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# 일정 저장용 (데모에서는 메모리 저장. 실서비스는 DB 연동 필요)
TOKENS = {}

@app.route("/")
def index():
    return "GPT Google Calendar API Server is running"

# OAuth 인증 시작
@app.route("/auth")
def auth():
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=https://www.googleapis.com/auth/calendar"
        "&access_type=offline"
        "&prompt=consent"
    )
    return redirect(auth_url)

# 인증 콜백
@app.route("/oauth2callback")
def oauth2callback():
    code = request.args.get("code")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    res = requests.post(token_url, data=data)
    token_response = res.json()

    # 데모용으로 1명 토큰만 저장
    TOKENS["access_token"] = token_response.get("access_token")
    TOKENS["refresh_token"] = token_response.get("refresh_token")

    return jsonify(token_response)

# 이벤트 조회
@app.route("/list-events", methods=["GET"])
def list_events():
    access_token = TOKENS.get("access_token")
    if not access_token:
        return {"error": "Access token missing. Please authenticate."}, 401

    calendar_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"maxResults": 5, "orderBy": "startTime", "singleEvents": True}

    res = requests.get(calendar_url, headers=headers, params=params)
    return res.json()

# 이벤트 생성
@app.route("/create-event", methods=["POST"])
def create_event():
    access_token = TOKENS.get("access_token")
    if not access_token:
        return {"error": "Access token missing. Please authenticate."}, 401

    data = request.json
    event = {
        "summary": data.get("summary", "GPT 일정"),
        "description": data.get("description", ""),
        "start": {"dateTime": data["start"], "timeZone": "Asia/Seoul"},
        "end": {"dateTime": data["end"], "timeZone": "Asia/Seoul"}
    }

    calendar_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    res = requests.post(calendar_url, headers=headers, json=event)
    return res.json()
