from .keywords import RED_FLAGS, GREEN_FLAGS
from .models import FlagResult

def analyze_scenario(text: str) -> dict:
    text_lower = text.lower()
    matched = []
    red_score = 0
    green_score = 0

    for keyword, weight in RED_FLAGS.items():
        if keyword in text_lower:
            red_score += weight
            matched.append(FlagResult(matched_keyword=keyword, flag_type="red", weight=weight))

    for keyword, weight in GREEN_FLAGS.items():
        if keyword in text_lower:
            green_score += weight
            matched.append(FlagResult(matched_keyword=keyword, flag_type="green", weight=weight))

    total = red_score + green_score
    toxic_pct = int((red_score / total) * 100) if total > 0 else 0

    verdict = get_verdict(toxic_pct)

    return {
        "toxic_percentage": toxic_pct,
        "red_flag_score": red_score,
        "green_flag_score": green_score,
        "verdict": verdict,
        "matched_flags": matched,
    }

def get_verdict(toxic_pct: int) -> str:
    if toxic_pct >= 70:
        return "🚩🚩🚩 KOŞARAK KAÇ"
    elif toxic_pct >= 40:
        return "⚠️ Dikkatli Ol"
    elif toxic_pct >= 15:
        return "🟡 Normal Karışım"
    else:
        return "💚 Bu İlişkiyi Koru"