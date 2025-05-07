from transformers import pipeline

_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            truncation=True,
            max_length=512
        )
    return _sentiment_pipeline
    
sentiment_comments = {
    "POSITIVE": "You seem positive — keep up the great attitude!",
    "NEGATIVE": "You seem upset — try to take a break or talk to someone.",
    "NEUTRAL": "You're balanced and neutral — it's a steady state to be in."
}

def sentiment(text: str) -> str:
    print('in sentiment:', text)

    try:
        result = get_sentiment_pipeline()(text)
        label = result[0]['label']
        score = result[0]['score']

        print(f"Sentiment: {label} ({score:.4f})")
        comment = sentiment_comments.get(label, "Sentiment detected.")

        print(f"Comment: {comment}")
        return comment

    except Exception as e:
        return f"Sentiment analysis failed: {str(e)}"
