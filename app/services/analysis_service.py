import assemblyai as aai

# --- Analysis Configuration ---
CONFIDENCE_THRESHOLD = 0.85
PACING_WPM_SLOW = 90
PACING_WPM_FAST = 150
PAUSE_THRESHOLD_SECONDS = 0.5

def analyze_pronunciation(words: list):
    """
    Computes pronunciation score and identifies mispronounced words.
    """
    if not words:
        return {"pronunciation_score": 0, "mispronounced_words": []}

    total_confidence = 0
    mispronounced_words = []

    for word in words:
        confidence = getattr(word, 'confidence', 0)
        total_confidence += confidence
        if confidence < CONFIDENCE_THRESHOLD:
            mispronounced_words.append({
                "word": word.text,
                "start": word.start / 1000,
                "confidence": round(confidence, 2)
            })

    pronunciation_score = round((total_confidence / len(words)) * 100) if words else 0
    return {
        "pronunciation_score": pronunciation_score,
        "mispronounced_words": mispronounced_words
    }

def analyze_pacing(transcript):
    """
    Calculates words per minute (WPM) and provides feedback.
    """
    words = getattr(transcript, "words", None)
    audio_duration = getattr(transcript, "audio_duration", None)
    if not words or not audio_duration:
        return {"pacing_wpm": 0, "pacing_feedback": "Not enough data to calculate pacing."}

    word_count = len(words)
    duration_minutes = audio_duration / 60
    if duration_minutes == 0:
        return {"pacing_wpm": 0, "pacing_feedback": "Audio is too short to calculate pacing."}

    wpm = round(word_count / duration_minutes)
    if wpm < PACING_WPM_SLOW:
        feedback = "Your speaking pace is too slow. Try to speak a bit more quickly and naturally."
    elif wpm > PACING_WPM_FAST:
        feedback = "Your speaking pace is too fast. Try to slow down to ensure your message is clear."
    else:
        feedback = "Your speaking pace is appropriate."

    return {"pacing_wpm": wpm, "pacing_feedback": feedback}

def analyze_pauses(words: list):
    """
    Identifies, counts, and measures significant pauses between words.
    """
    pause_count = 0
    total_pause_duration = 0

    if len(words) < 2:
        feedback = "Not enough words to analyze pause patterns."
        return {"pause_count": 0, "total_pause_time_sec": 0, "pause_feedback": feedback}

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        pause_duration = (next_word.start - current_word.end) / 1000
        if pause_duration >= PAUSE_THRESHOLD_SECONDS:
            pause_count += 1
            total_pause_duration += pause_duration

    total_pause_duration = round(total_pause_duration, 2)
    if pause_count > 5:
        feedback = f"You paused {pause_count} times, which might interrupt the flow. Try to reduce long pauses to improve fluency."
    elif total_pause_duration > 5:
        feedback = f"Your total pause time is {total_pause_duration} seconds. Focus on speaking more continuously."
    else:
        feedback = "Your use of pauses is good. They are natural and do not disrupt the flow."

    return {
        "pause_count": pause_count,
        "total_pause_time_sec": total_pause_duration,
        "pause_feedback": feedback
    }

def generate_feedback_summary(pronunciation, pacing, pauses):
    """
    Creates a final, user-friendly natural language summary.
    """
    feedback_parts = []

    if pacing['pacing_wpm'] < PACING_WPM_SLOW:
        feedback_parts.append("You spoke a bit slowly.")
    elif pacing['pacing_wpm'] > PACING_WPM_FAST:
        feedback_parts.append("You spoke quite quickly.")
    else:
        feedback_parts.append("You spoke at a good pace.")

    if pronunciation['mispronounced_words']:
        words_to_fix = [f"'{w['word']}'" for w in pronunciation['mispronounced_words']]
        feedback_parts.append(f"Focus on pronouncing {', '.join(words_to_fix)} more clearly.")

    if pauses['pause_count'] > 3:
        feedback_parts.append("Try to reduce long pauses to improve your speech fluency.")

    if not feedback_parts:
        return "Excellent job! Your delivery was clear, well-paced, and fluent."
    return " ".join(feedback_parts)
