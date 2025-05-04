from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from src.models.audio_converter import transcribe_audio_file

app = FastAPI(
    title="Audio Upload API",
    docs_url="/"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
print(UPLOAD_DIR)

# @app.post("/upload/")
# async def upload_audio(file: UploadFile = File(...)):
#     try:

#         temp_filename = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}.mp3")
#         with open(temp_filename, "wb") as f:
#             f.write(await file.read())

#         transcript = transcribe_audio_file(temp_filename)
#         return {"transcript": transcript}
#     except Exception as e:
#         return {"error": str(e)}
#     finally:
#         if os.path.exists(temp_filename):
#             os.remove(temp_filename)
