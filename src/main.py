import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.models.audio_converter import transcribe_audio_file

app = FastAPI(docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    tmp_path = None

    # Read incoming bytes
    contents = await file.read()
    if not contents:
        return {"error": "Empty file uploaded"}

    original_ext = os.path.splitext(file.filename)[1].lower()
    if original_ext not in (".ogg", ".mp3"):
        return {"error": "Only .ogg and .mp3 supported"}

    # Create temp file with the same extension
    fd, tmp_path = tempfile.mkstemp(suffix=original_ext)
    os.close(fd)


    try:
        # Write the upload into the temp file
        with open(tmp_path, "wb") as f:
            f.write(contents)

        # Transcribe via whisper (which will call ffmpeg internally)
        transcript = transcribe_audio_file(tmp_path)
        return {"transcript": transcript}

    except Exception as e:
        # Catch any transcription or I/O errors
        return {"error": str(e)}

    finally:
        # Clean up the temp file if it was created
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
