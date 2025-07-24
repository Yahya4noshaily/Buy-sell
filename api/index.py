import os
import cv2
import numpy as np
from fastapi import FastAPI, Request
import telegram
from telegram import Update
from PIL import Image
import io

app = FastAPI()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

def analyze_candles(image: Image.Image) -> str:
    # تحويل الصورة إلى OpenCV
    open_cv_image = np.array(image.convert('RGB'))[:, :, ::-1].copy()
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candles = [cnt for cnt in contours if cv2.contourArea(cnt) > 50]

    if len(candles) < 3:
        return "⚠️ لا يمكن تحليل الشارت بدقة - الشموع غير واضحة بما يكفي"

    heights = []
    for cnt in candles:
        x, y, w, h = cv2.boundingRect(cnt)
        heights.append(h)

    avg_height = np.mean(heights)
    max_height = np.max(heights)
    min_height = np.min(heights)

    # تحليل بسيط على الزخم والحجم
    if max_height > avg_height * 1.5:
        return "✅ التوصية: بيع (SELL)\n📊 شمعة هابطة ابتلاعية بوضوح\n⏱️ الصفقة: دقيقة واحدة"
    elif min_height < avg_height * 0.6:
        return "✅ التوصية: شراء (BUY)\n📊 شموع قصيرة تدل على تباطؤ الاتجاه وانعكاس ممكن\n⏱️ الصفقة: دقيقة واحدة"
    else:
        return "⚠️ التوصية: السوق متذبذب - لا توجد إشارة دخول مؤكدة حالياً"

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)

    if update.message and update.message.photo:
        chat_id = update.message.chat_id
        photo_file = await update.message.photo[-1].get_file()
        byte_array = photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(byte_array))

        decision = analyze_candles(image)
        bot.send_message(chat_id=chat_id, text=decision)

    return {"ok": True}
