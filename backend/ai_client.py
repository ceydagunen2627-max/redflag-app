import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_with_ai(scenario: str) -> dict:
    prompt = f"""Sen deneyimli bir yakın arkadaşsın. Kıskançlık içeren, olgun ama kısıtlayıcı bir şekilde bu ilişki senaryosunu değerlendireceksin.

Senaryo: "{scenario}"

Senaryoyu dikkatlice oku ve gerçekçi bir toksiklik yüzdesi belirle (0 = tamamen sağlıklı, 100 = son derece toksik/tehlikeli).
Kontrol etme, kıskançlık, izolasyon, aldatma, saygısızlık, manipülasyon gibi davranışlar toksikliği artırır.
Dinleme, destek, saygı, iletişim, güven gibi davranışlar toksikliği azaltır.
Senaryoda hiçbir olumsuz veya olumlu belirti yoksa orta bir değer (40-60) ver, asla nedensiz yere %0 verme.

SADECE aşağıdaki JSON formatında cevap ver, başka hiçbir açıklama veya metin ekleme:
{{"toxic_percentage": <0-100 arası tam sayı>, "commentary": "<samimi, içten, 2-3 cümlelik yorum>"}}"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    raw = response.text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw)
        return {
            "toxic_percentage": int(result.get("toxic_percentage", 50)),
            "commentary": result.get("commentary", "Bu senaryo hakkında net bir yorum yapamadım.")
        }
    except Exception:
        return {
            "toxic_percentage": 50,
            "commentary": "Bu senaryo hakkında net bir yorum yapamadım, ama dikkatli olmakta fayda var 👀"
        }