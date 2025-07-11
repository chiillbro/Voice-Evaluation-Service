from pydantic import BaseModel
from typing import List, Optional

class WordDetail(BaseModel):
    word: str
    start: float
    end: float
    confidence: float

class MispronouncedWord(BaseModel):
    word: str
    start: float
    confidence: float

class PronunciationAnalysis(BaseModel):
    pronunciation_score: int
    mispronounced_words: List[MispronouncedWord]

class PacingAnalysis(BaseModel):
    pacing_wpm: int
    pacing_feedback: str

class PauseAnalysis(BaseModel):
    pause_count: int
    total_pause_time_sec: float
    pause_feedback: str


# Main Response Model

class EvaluationResponse(BaseModel):
    transcript: str
    words: List[WordDetail]
    audio_duration_sec: float
    pronunciation_analysis: PronunciationAnalysis
    pacing_analysis: PacingAnalysis
    pause_analysis: PauseAnalysis
    text_feedback: str