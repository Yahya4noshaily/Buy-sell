
from fastapi import FastAPI, UploadFile
import easyocr
from PIL import Image
import io

app = FastAPI()
reader = easyocr.Reader(['en'])

@app.post("/predict/")
async def predict_chart(file: UploadFile):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    result = reader.readtext(image)
    text_detected = " ".join([res[1] for res in result])

    if "RSI" in text_detected and "80" in text_detected:
        signal = "بيع قوي 🔻 (Overbought)"
    elif "RSI" in text_detected and "30" in text_detected:
        signal = "شراء قوي 🔼 (Oversold)"
    else:
        signal = "📉 لا توجد بيانات RSI كافية للتحليل."

    return {"التوصية": signal, "النص المقروء": text_detected}
