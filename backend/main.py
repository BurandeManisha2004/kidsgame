from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts
import uuid
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Req(BaseModel):
    text: str

# ✅ FIXED PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

os.makedirs(AUDIO_DIR, exist_ok=True)

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

@app.post("/speak")
async def speak(req: Req):

    file_name = f"{uuid.uuid4().hex}.mp3"
    file_path = os.path.join(AUDIO_DIR, file_name)

    communicate = edge_tts.Communicate(
        req.text,
        "mr-IN-AarohiNeural",
        rate="+9%",
        pitch="+2Hz",
        volume="+20%"
    )

    await communicate.save(file_path)

    return {"audio": f"{BASE_URL}/audio/{file_name}"}

# ✅ FIXED STATIC
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")