from fastapi import APIRouter, File, UploadFile, HTTPException, status
from ..schemas.evaluation import EvaluationResponse
from ....services import transcription_service, analysis_service

router = APIRouter()

@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
    summary="Evaluate a spoken answer",
    description="Upload a .wav or .mp3 audio file (<= 60 seconds) to receive a full voice evaluation."
)
async def evaluate_spoken_answer(
    file: UploadFile = File(..., description="Audio file in .wav or .mp3 format.")
):
    """
    This endpoint processes a spoken answer and provides structured feedback on:
    - **Pronunciation**: Accuracy and clarity of word articulation.
    - **Pacing**: Speech rate in words per minute (WPM).
    - **Pauses**: Count and total duration of significant pauses.
    """
    # 1. Validate file type and size
    if file.content_type not in ["audio/wav", "audio/mpeg"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Please upload a .wav or .mp3 file."
        )

    # 2. Audio Upload and Transcription (Deliverable 1)
    transcript = await transcription_service.get_transcription(file)
    
    if transcript.audio_duration and transcript.audio_duration > 60:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audio duration exceeds the 60-second limit."
        )

    # 3. Perform all analyses
    pronunciation_result = analysis_service.analyze_pronunciation(transcript.words)
    pacing_result = analysis_service.analyze_pacing(transcript)
    pause_result = analysis_service.analyze_pauses(transcript.words)
    summary_feedback = analysis_service.generate_feedback_summary(
        pronunciation_result, pacing_result, pause_result
    )

    # 4. Structure the final response according to the schema
    return EvaluationResponse(
        transcript=transcript.text,
        words=[{
            "word": w.text,
            "start": w.start / 1000,
            "end": w.end / 1000,
            "confidence": getattr(w, 'confidence', 0)
        } for w in transcript.words],
        audio_duration_sec=transcript.audio_duration,
        pronunciation_analysis=pronunciation_result,
        pacing_analysis=pacing_result,
        pause_analysis=pause_result,
        text_feedback=summary_feedback
    )