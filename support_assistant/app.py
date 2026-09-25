from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Zepto AI Support Assistant")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

@app.post("/ask", response_model=QueryResponse)
def ask_question(req: QueryRequest):
    return QueryResponse(
        answer=f"Received query regarding Zepto services: {req.query}",
        sources=["doc_01"],
        confidence=0.95
    )
