from pydantic import BaseModel

from .llm_models import TokenInsights


class TokenInsightsRequest(BaseModel):
    vs_currency: str
    history_data: int


class TokenData(BaseModel):
    id: str
    symbol: str
    name: str
    market_data: dict


class ModelMetaData(BaseModel):
    provider: str
    model: str

class TokenInsightsResponse(BaseModel):
    source: str
    token: TokenData
    insight: TokenInsights
    model: ModelMetaData
