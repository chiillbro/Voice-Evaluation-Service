import assemblyai as aai
from fastapi import UploadFile, HTTPException, status
from ..core.config import settings

# api key
aai.settings.api_key = settings.ASSEMBLYAI_API_KEY

async def get_transcription(audio_file: UploadFile):
    """
    Transcribes the given audio file using AssemblyAI.
    """
    try:
        config = aai.TranscriptionConfig(
            sentiment_analysis=True,
            speaker_labels=True
        )
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_file.file)

        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Transcription failed: {transcript.error}"
            )
        
        if not transcript.words:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not detect any words in the audio. The file might be silent or corrupted."
            )

        return transcript

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during transcription: {str(e)}"
        )