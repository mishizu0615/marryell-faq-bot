import re
from sheets import fetch_faq_master, append_unknown_question
from claude_api import ask_claude
from line_utils import reply_line

MATCH_THRESHOLD = 2


def _tokenize(text: str) -> set:
    text = re.sub(r"[　 、。！？!?「」『』【】\[\]()（）\-・,.]", " ", text)
    return {w for w in text.lower().split() if len(w) >= 2}


def find_best_faq(question: str, faqs: list) -> dict:
    q_tokens = _tokenize(question)
    best_score = 0
    best_faq = None
    for faq in faqs:
        target = faq["question"] + " " + faq["tags"]
        score = len(q_tokens & _tokenize(target))
        if score > best_score:
            best_score = score
            best_faq = faq
    return best_faq if best_score >= MATCH_THRESHOLD else None


def handle_faq_event(event: dict):
    event_type = event.get("type")
    reply_token = event.get("replyToken", "")
    user_id = event.get("source", {}).get("userId", "")

    # リッチメニュータップ
    if event_type == "postback":
        data = event.get("postback", {}).get("data", "")
        if data == "action=faq":
            reply_line(reply_token,
                "📋 FAQモードです！\nマリエルについて何でも聞いてみてください✨\n（例：料金は？／予約は必要？／どんな人が来てる？）")
        return

    # テキストメッセージ
    if event_type != "message":
        return
    msg = event.get("message", {})
    if msg.get("type") != "text":
        return

    question = msg.get("text", "").strip()
    if not question:
        return

    # FAQマスター検索
    try:
        faqs = fetch_faq_master()
        matched = find_best_faq(question, faqs)
    except Exception as e:
        print(f"Sheets error: {e}")
        matched = None

    if matched:
        answer = matched["answer"]
    else:
        try:
            answer = ask_claude(question)
        except Exception as e:
            print(f"Claude error: {e}")
            answer = "うまく回答できませんでした🙏\nスタッフに直接お問い合わせください！"
        try:
            append_unknown_question(user_id, question, answer)
        except Exception as e:
            print(f"Sheets append error: {e}")

    reply_line(reply_token, answer)
