from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TokenIdentity(BaseModel):
    id: str = Field(..., description="CoinGecko token id")
    symbol: str = Field(..., description="Token symbol, lowercase")
    name: str = Field(..., description="Human-readable token name")


class MarketSnapshot(BaseModel):
    price_usd: float = Field(..., description="Current price in USD")
    market_cap_usd: float = Field(..., description="Current market cap in USD")
    volume_24h_usd: float = Field(..., description="24h trading volume in USD")
    market_cap_rank: Optional[int] = Field(
        None, description="Market cap rank if available"
    )


class Momentum24h(BaseModel):
    price_change_pct: float = Field(..., description="24h price change percentage")
    high_usd: float = Field(..., description="24h high price in USD")
    low_usd: float = Field(..., description="24h low price in USD")


class Positioning(BaseModel):
    ath_usd: float = Field(..., description="All-time high price in USD")
    distance_from_ath_pct: float = Field(
        ..., description="Percent difference from ATH (negative = below ATH)"
    )


class TokenInsightInput(BaseModel):
    token: TokenIdentity
    market_snapshot: MarketSnapshot
    momentum_24h: Momentum24h
    positioning: Positioning


class TokenInsightSentiment(str, Enum):
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"


class TokenInsights(BaseModel):
    sentiment: TokenInsightSentiment = Field(
        ..., description="Sentiment value for given token"
    )
    reasoning: str = Field(..., description="Reasoning for the given sentiment")
