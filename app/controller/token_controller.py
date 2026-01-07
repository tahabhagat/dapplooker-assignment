import os

from coingecko_sdk import AsyncClient
from coingecko_sdk.resources.coins.coins import AsyncCoinsResource
from coingecko_sdk.resources.coins.market_chart import AsyncMarketChartResource
from coingecko_sdk.types.coin_get_id_response import (
    CoinGetIDResponse,
    MarketDataCurrentPrice,
)
from fastapi import APIRouter
from loguru import logger
from models.llm_models import (
    MarketSnapshot,
    Momentum24h,
    Positioning,
    TokenIdentity,
    TokenInsightInput,
)
from models.token_models import (
    ModelMetaData,
    TokenData,
    TokenInsights,
    TokenInsightsRequest,
    TokenInsightsResponse,
)
from service import llm_service

router = APIRouter(
    prefix="/api/token",
    tags=["Token Related APIs"],
)
client = AsyncClient(demo_api_key=os.environ["COINGECKO_API_KEY"], environment="demo")
coin_resource: AsyncCoinsResource = AsyncCoinsResource(client)
market_chart_resource: AsyncMarketChartResource = AsyncMarketChartResource(client)


def generate_insights(coin_data: CoinGetIDResponse):
    md = coin_data.market_data
    distance_from_ath_pct = ((md.current_price.usd - md.ath.usd) / md.ath.usd) * 100
    token_insight_input = TokenInsightInput(
        token=TokenIdentity(
            id=coin_data.id,
            symbol=coin_data.symbol,
            name=coin_data.name,
        ),
        market_snapshot=MarketSnapshot(
            price_usd=md.current_price.usd,
            market_cap_usd=md.market_cap.usd,
            volume_24h_usd=md.total_volume.usd,
            market_cap_rank=int(coin_data.market_cap_rank)
            if coin_data.market_cap_rank is not None
            else None,
        ),
        momentum_24h=Momentum24h(
            price_change_pct=md.price_change_percentage_24h,
            high_usd=md.high_24h.usd,
            low_usd=md.low_24h.usd,
        ),
        positioning=Positioning(
            ath_usd=md.ath.usd,
            distance_from_ath_pct=distance_from_ath_pct,
        ),
    )
    insights = llm_service.generate_insights(token_insight_input)
    return insights


@router.post("/{id}/insight")
async def fetch_insights(
    id: str, 
    # request: TokenInsightsRequest
) -> TokenInsightsResponse:
    logger.info(f"Fetching insights for token {id}")

    coin_data = await coin_resource.get_id(id)
    # market_chart = await market_chart_resource.get(
    #     id, vs_currency=request.vs_currency, days=str(request.history_data)
    # )

    market_data = coin_data.market_data

    def usd(d: MarketDataCurrentPrice | None) -> float | None:
        return d.usd if d else None

    token = TokenData(
        id=coin_data.id,
        symbol=coin_data.symbol,
        name=coin_data.name,
        market_data={
            "current_price_usd": market_data.current_price.usd,
            "market_cap_usd": market_data.market_cap.usd,
            "total_volume_usd": market_data.total_volume.usd,
            "price_change_percentage_24h": market_data.price_change_percentage_24h,
        },
    )
    response = TokenInsightsResponse(
        source="coingecko",
        token=token,
        insight=generate_insights(coin_data),
        model=ModelMetaData(provider="google-genai", model="gemini-2.5-flash"),
    )
    return response

