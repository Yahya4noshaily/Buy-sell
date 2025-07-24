from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🔥 توصية حقيقية: انتظر تحميل الشارت... ✅"}
