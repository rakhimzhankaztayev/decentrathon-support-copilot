"""FastAPI service for support ticket triage."""

from fastapi import FastAPI

from app.core.preprocessor import normalize_kazakh_cp1251
from app.rag.generator import generate_rag_response
from app.schemas import TriageRequest, TriageResponse
from app.triage.classifier import classify_ticket

app = FastAPI(title="Grand Mobile Support Copilot", version="0.1.0")


async def process_single_ticket(request: TriageRequest) -> TriageResponse:
    player_texts = [
        normalize_kazakh_cp1251(message.text)
        for message in request.messages
        if message.role in ("player", "reported_player")
    ]
    full_text = "\n".join(player_texts)
    triage_result = await classify_ticket(request, full_text)
    rag_result = await generate_rag_response(
        ticket=request,
        normalized_text=full_text,
        lang=triage_result["lang"],
        category=triage_result["category"],
    )
    return TriageResponse(
        **triage_result,
        **rag_result,
    )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResponse)
async def triage_endpoint(request: TriageRequest) -> TriageResponse:
    return await process_single_ticket(request)
