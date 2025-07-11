# Voice Evaluation Microservice

This microservice provides a comprehensive evaluation of spoken audio, delivering structured feedback on pronunciation, pacing, and pause patterns. It is built with Python, FastAPI, and AssemblyAI, and is fully containerized with Docker for easy deployment and scalability.

This project fulfills all the requirements of the "Voice Evaluation Microservice" pre-work assignment.

## Features

- **Transcription**: Highly accurate speech-to-text using AssemblyAI.
- **Pronunciation Analysis**: Provides a 0-100 score based on word confidence and flags potentially mispronounced words.
- **Pacing Evaluation**: Calculates speech rate in Words Per Minute (WPM) and gives contextual feedback.
- **Pause Detection**: Identifies and quantifies significant pauses to analyze speech fluency.
- **Natural Language Summary**: Generates a consolidated, user-friendly feedback summary.
- **Production Ready**: Built with a scalable architecture, containerized with Docker, and served via a Gunicorn/Uvicorn production server.

## API Endpoint

### Evaluate Audio

- **URL**: `/api/v1/evaluate`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: The audio file to be evaluated.
    - **Type**: `.wav` or `.mp3`
    - **Constraints**: Audio duration should be less than or equal to 60 seconds.

## Setup and Running

### Prerequisites

- Git
- Docker and Docker Compose
- An AssemblyAI API Key

### Instructions

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/chiillbro/Voice-Evaluation-Service.git
    cd voice-evaluation-service
    ```

2.  **Create Environment File**
    Create a `.env` file in the root directory and add your AssemblyAI API key:

    ```env
    ASSEMBLYAI_API_KEY="YOUR_ASSEMBLYAI_API_KEY_HERE"
    ```

3.  **Build and Run with Docker**
    From the root directory, run the following command:
    ```bash
    docker-compose up --build
    ```
    The service will be available at `http://localhost:8000`.

## Usage

### Interactive Docs (Swagger UI)

Once the service is running, you can access the interactive API documentation in your browser at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

From here, you can directly upload an audio file and test the endpoint.

### cURL Example

Use the following cURL command to send an audio file for evaluation. Replace `/path/to/your/audio.mp3` with the actual path to your file.

```bash
curl -X POST "http://localhost:8000/api/v1/evaluate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/audio.mp3;type=audio/mpeg"
```

### Sample Audio Files

- [harvard.wav](./test-audio-files/harvard.wav)
- [audio_2.wav](./test-audio-files/audio_2.wav)
- [audio_3.wav](./test-audio-files/audio_3.wav)

## Assumptions and Notes

- **Pronunciation Score**: The pronunciation score is calculated as the average word confidence score, scaled to 100. A "mispronounced" word is any word with a confidence below `0.85`.
- **Pacing Thresholds**: The pacing is considered "Too slow" if below `90 WPM` and "Too fast" if above `150 WPM`.
- **Pause Threshold**: A pause is considered significant if it is longer than `0.5` seconds.
- **Error Handling**: The API includes robust error handling for unsupported file types, transcription failures, and silent audio files.
- **Third-Party Service**: This service relies on the AssemblyAI API for transcription. Its performance and availability are dependent on AssemblyAI.
