import os
from fastapi import FastAPI, Request
import telegram
from telegram import Update
from PIL import Image
import io

app = FastAPI()

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

@app.post("/")
async def root(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)

    if update.message and update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        byte_array = photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(byte_array))

        # تحليل وهمي بسيط
        decision = "✅ التوصية: بيع (SELL)\n📊 RSI = 72, ترند هابط\n⏱️ الصفقة: دقيقة واحدة"
        bot.send_message(chat_id=update.message.chat_id, text=decision)

    return {"status": "ok"}
