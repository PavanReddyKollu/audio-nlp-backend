from transformers import pipeline

_emotion_pipeline = None

def get_emotion_pipeline():
    global _emotion_pipeline
    if _emotion_pipeline is None:
        _emotion_pipeline = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None,
            truncation=True,
            max_length=512  # Explicitly setting max_length

        )
    return _emotion_pipeline

def emotion(text: str) -> str:
    print('in emotion', text)
    emotion_scores = get_emotion_pipeline()(text)
    scores = emotion_scores[0]
    top_emotion = max(scores, key=lambda x: x['score'])

    emotion_comments = {
        "joy": "You are joyful — please continue like this!",
        "sadness": "You seem sad — it's okay to feel this way, consider talking to someone.",
        "anger": "You sound angry — maybe take a moment to breathe and reflect.",
        "fear": "You're expressing fear — try to stay calm, you're not alone.",
        "surprise": "You're surprised — hope it's something good!",
        "disgust": "You sound disgusted — maybe take a step back and reconsider the situation.",
        "neutral": "You are neutral — steady and balanced!"
    }

    comment = emotion_comments.get(top_emotion["label"], "Your emotional state is recognized.")
    print(f"\nComment: {comment}")
    return comment
