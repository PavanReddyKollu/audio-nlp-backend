import whisper

# Load model only once
model = whisper.load_model("large")

def transcribe_audio_file(file_path: str) -> str:
    print("inside transcribe")
    result = model.transcribe(file_path, language="en")
    return result["text"]
