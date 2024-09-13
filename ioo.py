from fastapi import FastAPI

app = FastAPI()

@app.get("/get_text")
def get_text():
    return {"text": "Hello from FastAPI on Vercel!"}
