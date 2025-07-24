import os
from fastapi import FastAPI, Request
import telegram
from telegram import Update
import io
from PIL import Image

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)

    if update.message and update.message.photo:
        chat_id = update.message.chat_id
        # تحليل وهمي مؤقت:
        message = "✅ التوصية: بيع (SELL)\n📊 RSI = 72, ترند هابط\n⏱️ الصفقة: دقيقة واحدة"
        bot.send_message(chat_id=chat_id, text=message)

    return {"ok": True}
