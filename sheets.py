import os
import json
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID  = os.environ["MARIEL_FAQ_SPREADSHEET_ID"]
SERVICE_ACCOUNT = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
FAQ_SHEET       = "FAQマスター"
NEWQ_SHEET      = "未収録質問ログ"
JST             = timezone(timedelta(hours=9))


def _get_service():
    info = json.loads(SERVICE_ACCOUNT)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("sheets", "v4", credentials=creds).spreadsheets()


def fetch_faq_master() -> list:
    svc = _get_service()
    result = svc.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{FAQ_SHEET}!A2:D"
    ).execute()
    rows = result.get("values", [])
    return [
        {
            "question": row[0] if len(row) > 0 else "",
            "answer":   row[1] if len(row) > 1 else "",
            "category": row[2] if len(row) > 2 else "",
            "tags":     row[3] if len(row) > 3 else "",
        }
        for row in rows
    ]


def append_unknown_question(user_id: str, question: str, ai_answer: str):
    svc = _get_service()
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    svc.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{NEWQ_SHEET}!A:E",
        valueInputOption="USER_ENTERED",
        body={"values": [[now, question, ai_answer, user_id, "未対応"]]}
    ).execute()
