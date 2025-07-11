from fastapi import FastAPI
from .api.v1.endpoints import evaluation

app = FastAPI(
    title="Voice Evaluation Microservice",
    description="A microservice to process spoken answers and provide structured feedback.",
    version="1.0.0"
)

app.include_router(evaluation.router, prefix="/api/v1", tags=["Evaluation"])

@app.get("/", tags=["Health Check"])
async def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the Voice Evaluation Microservice!"}