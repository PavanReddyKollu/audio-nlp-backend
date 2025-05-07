import io
import base64
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import opinion_lexicon, stopwords

# Ensure these are downloaded before deployment (via: python -m nltk.downloader opinion_lexicon stopwords)
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

stop_words = set(stopwords.words('english'))
stop_words.update(["um", "uh", "like", "you know", "I mean", "so", "actually"])

def wordcloud_positive(text: str) -> str:
    words = [w for w in text.split() if w.lower() not in stop_words]

    words = " ".join([W for W in words if W in positive_words])
    joined = " ".join(words)
    wc = WordCloud(background_color='white', width=1800, height=1400).generate(joined)

    fig = plt.figure(figsize=(10, 7))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")
