from PIL import Image, ImageDraw, ImageFont
import uuid
import os

def generate_card(nickname: str, toxic_pct: int, verdict: str) -> str:
    W, H = 1080, 1920  # Instagram story boyutu

    # Toxic yüzdesine göre renk seç
    if toxic_pct >= 70:
        bg_color = (139, 0, 0)
    elif toxic_pct >= 40:
        bg_color = (255, 140, 0)
    else:
        bg_color = (34, 139, 34)

    img = Image.new("RGB", (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("assets/fonts/Poppins-Bold.ttf", 100)
    font_medium = ImageFont.truetype("assets/fonts/Poppins-Bold.ttf", 60)
    font_small = ImageFont.truetype("assets/fonts/Poppins-Regular.ttf", 40)

    draw.text((W/2, 300), "İLİŞKİ GÜVENLİK RAPORU", font=font_medium, fill="white", anchor="mm")
    draw.text((W/2, 800), f"%{toxic_pct}", font=font_big, fill="white", anchor="mm")
    draw.text((W/2, 950), "TOXIC", font=font_medium, fill="white", anchor="mm")
    draw.text((W/2, 1200), verdict, font=font_medium, fill="white", anchor="mm")
    draw.text((W/2, 1700), f"@{nickname}", font=font_small, fill="white", anchor="mm")

    os.makedirs("output", exist_ok=True)
    filename = f"output/{uuid.uuid4().hex}.png"
    img.save(filename)
    return filename