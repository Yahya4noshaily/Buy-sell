
from fastapi import FastAPI, UploadFile, File, Request
import requests

app = FastAPI()

TELEGRAM_BOT_TOKEN = "7660484913:AAG1Zr1QgXIchajpnol9wiLELBG8yHTC1rU"
TELEGRAM_CHAT_ID = "293528381"

@app.get("/")
async def home():
    return {"message": "✅ البوت شغال"}

# استقبال صورة وتحويلها لتوصية
@app.post("/send-signal/")
async def send_signal(image: UploadFile = File(...)):
    contents = await image.read()
    with open("temp.jpg", "wb") as f:
        f.write(contents)

    # إرسال الصورة إلى تيليجرام
    files = {'photo': open("temp.jpg", 'rb')}
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'caption': "📊 تم استلام الشارت، جاري التحليل..."
    }
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto", data=data, files=files)

    return {"status": "تم إرسال الصورة بنجاح"}

# استقبال تنبيه من TradingView
@app.post("/tradingview-alert/")
async def tradingview_alert(request: Request):
    data = await request.json()
    message = data.get("message", "🚨 تنبيه من TradingView (لا توجد تفاصيل)")

    # إرسال التنبيه إلى تيليجرام
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message}
    )

    return {"status": "تم إرسال التنبيه إلى تيليجرام ✅"}
