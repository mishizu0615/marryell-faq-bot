import os
import requests

CLAUDE_API_KEY = os.environ["CLAUDE_API_KEY"]

SYSTEM_PROMPT = """
あなたは婚活バー「マリエル」の案内スタッフ「マリ」です。

【マリエルについて】
コンセプト：楽しくなくちゃ婚活じゃない
営業場所：代々木・恵比寿・自由が丘の3拠点
雰囲気：カジュアルで温かく、プレッシャーなしで出会えるバー形式

【回答スタイル】
・温かく、親しみやすいトーンで短めに（3〜5文程度）
・押しつけがましくない、来店を急かさない
・具体的な情報がない場合は「詳しくはスタッフまで♪」と案内
・絵文字は1〜2個まで
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
