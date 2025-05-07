import librosa

_sr_tone_model = None

# Function to load the necessary resources (tempo and pitch analysis)
def get_sr_tone_model():
    global _sr_tone_model
    if _sr_tone_model is None:
        # You can put any initializations if required, e.g., setting parameters.
        _sr_tone_model = True  # Mark that the model is now initialized (this is a placeholder)
    return _sr_tone_model

# Function to analyze speaking rate (tempo) and pitch (tone) based on the audio file
def analyze_speaking_rate_tone(file_path: str):
    model = get_sr_tone_model()  # Initialize model if not done already

    # Load audio
    y, sr = librosa.load(file_path)

    # Estimate speaking rate (tempo) and pitch
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    pitch = librosa.yin(y, fmin=50, fmax=300)

    # Compute average pitch
    avg_pitch = pitch.mean()

    # Speaking rate comment
    if tempo < 80:
        tempo_comment = "You are speaking slowly — this can be calming and clear."
    elif tempo <= 120:
        tempo_comment = "You are speaking at a moderate pace — this is ideal for clarity and engagement."
    else:
        tempo_comment = "You are speaking quickly — try to slow down a bit for better understanding."

    # Pitch comment
    if avg_pitch < 120:
        pitch_comment = "Your pitch is low — this may come across as calm or authoritative."
    elif avg_pitch <= 200:
        pitch_comment = "Your pitch is moderate — this is often perceived as natural and engaging."
    else:
        pitch_comment = "Your pitch is high — be mindful, as this can sound tense or overly excited."

    # Return both values and comments
    return {
    "speaking_rate_value": float(tempo),
    "speaking_rate_comment": tempo_comment,
    "pitch_value": float(avg_pitch),
    "pitch_comment": pitch_comment
}

