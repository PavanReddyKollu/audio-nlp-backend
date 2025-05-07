import traceback
import whisper
from src.models.emotion import emotion
from src.models.wordcloud import wordcloud
from src.models.sentiment import sentiment
from src.models.sr_tone import analyze_speaking_rate_tone
from src.models.sr_tone_combined import analyze_speaking_rate_and_tone_combined
from src.models.pauses import analyze_pauses
from src.models.wordcloudnegative import wordcloud_negative
from src.models.wordcloudpositive import wordcloud_positive
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse




_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base", device="cuda" if whisper.torch.cuda.is_available() else "cpu")
    return _whisper_model


def transcribe_audio_file(file_path: str) -> dict:
    try:
        print("Starting transcription pipeline...")
        model = get_whisper_model()
        result = model.transcribe(file_path, language="en")
        
        emotion_result = emotion(result["text"])
        png_base64 = wordcloud(result["text"])
        png_base64_negative = wordcloud_negative(result["text"])
        png_base64_positive = wordcloud_positive(result["text"])

        sentiment_result = sentiment(result["text"])  
        sr_tone_result = analyze_speaking_rate_tone(file_path)
        sr_tone_result_combined = analyze_speaking_rate_and_tone_combined(file_path)
        pauses_result = analyze_pauses(file_path)
        print('in 41')
        print(type(emotion_result))
        print(type(sentiment_result))
        print(type(sr_tone_result))
        print(type(sr_tone_result_combined))
        print(type(pauses_result))
        print('in 47')

        response =  {
            "transcribed_text": result["text"],
            "emotion": emotion_result,
            "neutral_image": png_base64,
            "sentiment": sentiment_result,
            "sr_tone": sr_tone_result,
            "sr_tone_combined": sr_tone_result_combined,
            "pauses": pauses_result,
            "negative_image": png_base64_negative,
            "positive_image": png_base64_positive
        }
        return JSONResponse(content=jsonable_encoder(response))


    except Exception as e:
        print("Internal Server Error:", str(e))
        traceback.print_exc()
        return {"error": "Internal server error. Please check the logs for details."}
