import os
import cv2
import numpy as np
import pytesseract
from fastapi import FastAPI, Request
import telegram
from telegram import Update
from PIL import Image
import io

app = FastAPI()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

def analyze_chart_with_ocr(image: Image.Image) -> str:
    # تحويل الصورة إلى OpenCV
    img = np.array(image.convert('RGB'))[:, :, ::-1].copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # قراءة النصوص الظاهرة (OCR)
    text = pytesseract.image_to_string(gray)
    text = text.lower()

    # تحليل بناءً على الكلمات المفتاحية
    decision = ""
    reason = ""

    if "rsi" in text:
        try:
            import re
            match = re.search(r"rsi\s*[:=]?\s*(\d{1,3})", text)
            if match:
                rsi_value = int(match.group(1))
                if rsi_value > 70:
                    decision = "✅ التوصية: بيع (SELL)"
                    reason = f"📊 السبب: RSI مرتفع ({rsi_value}) - تشبع شرائي"
                elif rsi_value < 30:
                    decision = "✅ التوصية: شراء (BUY)"
                    reason = f"📊 السبب: RSI منخفض ({rsi_value}) - تشبع بيعي"
        except:
            pass

    if not decision:
        decision = "⚠️ لا توجد إشارة واضحة"
        reason = "📊 السبب: لم يتم التعرف على RSI أو نماذج قوية"

    return f"{decision}\n{reason}\n⏱️ الصفقة: دقيقة واحدة"

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)

    if update.message and update.message.photo:
        chat_id = update.message.chat_id
        photo_file = await update.message.photo[-1].get_file()
        byte_array = photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(byte_array))

        result = analyze_chart_with_ocr(image)
        bot.send_message(chat_id=chat_id, text=result)

    return {"ok": True}
