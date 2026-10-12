import os
from typing import List, Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from analyzer import analyze_text

app = FastAPI(
    title="BiasCheck AI API",
    description="Rule-based inclusive-language review. Findings are suggestions, not verdicts.",
    version="1.0.0",
)

def parse_origins() -> List[str]:
    raw = os.getenv("FRONTEND_ORIGINS", "*").strip()
    if raw == "*":
        return ["*"]
    return [origin.strip().rstrip("/") for origin in raw.split(",") if origin.strip()]

origins = parse_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

class Finding(BaseModel):
    phrase: str
    start: int
    end: int
    category: str
    issue: str
    suggestion: str
    reason: str
    review_level: Literal["Review", "Consider"]

class AnalyzeResponse(BaseModel):
    findings: List[Finding]
    total_findings: int
    categories: List[str]
    notice: str

NOTICE = (
    "Flags are suggestions for human review, not definitive judgments. "
    "A flagged phrase is not proof of bias or intent, and unflagged text is not guaranteed to be inclusive."
)

@app.get("/")
def root():
    return {
        "name": "BiasCheck AI API",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    findings = analyze_text(request.text)
    categories = sorted({finding["category"] for finding in findings})
    return {
        "findings": findings,
        "total_findings": len(findings),
        "categories": categories,
        "notice": NOTICE,
    }
