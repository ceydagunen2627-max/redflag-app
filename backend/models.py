from pydantic import BaseModel, Field
from typing import List

class ScenarioRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=1000)
    nickname: str | None = "Anonim"

class FlagResult(BaseModel):
    matched_keyword: str
    flag_type: str  # "red" veya "green"
    weight: int

class AnalysisResponse(BaseModel):
    toxic_percentage: int
    red_flag_score: int
    green_flag_score: int
    verdict: str          # "RUN 🚩", "Marry Them 💚" gibi
    commentary: str       # esprili yorum
    matched_flags: List[FlagResult]