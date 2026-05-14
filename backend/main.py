import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class Req(BaseModel):
    text: str


# ---------------- TTS API (FIXED) ----------------
@app.post("/speak")
async def speak(req: Req):

    # Edge TTS setup
    communicate = edge_tts.Communicate(
        req.text,
        "mr-IN-ManoharNeural",
        rate="+9%",
        pitch="+2Hz",
        volume="+20%"
    )

    audio_stream = io.BytesIO()

    # stream audio directly (NO FILE SAVE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])

    audio_stream.seek(0)

    return StreamingResponse(audio_stream, media_type="audio/mpeg")