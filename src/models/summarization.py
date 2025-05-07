summarizer = pipeline("summarization")
summary = summarizer(transcribed_text, max_length=50, min_length=25, do_sample=False)
print(summary[0]['summary_text'])