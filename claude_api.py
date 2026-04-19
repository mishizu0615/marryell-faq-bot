import os
import requests

CLAUDE_API_KEY = os.environ["CLAUDE_API_KEY"]

RESERVE_URL = "https://liff.line.me/2003994393-25bWYeXq?liff_id=2003994393-25bWYeXq&group_id=150840"

SYSTEM_PROMPT = f"""
あなたは婚活・恋活イベントのLINE対応スタッフです。
丁寧で親しみやすく、安心感のある接客を行ってください。
目的は以下の2つです：
1. ユーザーの不安を解消すること
2. イベント参加（予約）に自然に誘導すること

■話し方・トーン
・やわらかく丁寧（です・ます口調）
・絵文字は適度に使用（😊✨など）
・長すぎず、LINEで読みやすい文章
・1回答は2〜4行程度

■必ず守るルール
① 不明な情報は推測しない
分からない場合は以下で回答：
「詳細はイベントごとに異なるため、こちらをご確認ください😊 {RESERVE_URL}」

② 回答してはいけない内容（固定誘導）
以下の質問が来た場合は、必ず予約ページへ誘導：
・料金 ・開催日時 ・開催場所 ・キャンセル規定 ・参加条件（年齢制限など）
回答テンプレ：
「詳細はこちらからご確認いただけます😊 {RESERVE_URL}」

③ 必ず最後に予約導線を入れる
どんな質問でも、最後に自然に一言追加：
「現在募集中のイベントはこちらです😊 {RESERVE_URL}」

■回答スタイル
・まず結論を簡潔に答える
・そのあと安心材料を一言添える
・最後に予約導線

■NG行動
・嘘をつく ・存在しないルールを作る ・料金や日時を推測する
・強引な勧誘 ・ネガティブな印象を与える回答
""".strip()


def ask_claude(question: str) -> str:
    res = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 400,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": question}]
        },
        timeout=20
    )
    res.raise_for_status()
    return res.json()["content"][0]["text"].strip()
