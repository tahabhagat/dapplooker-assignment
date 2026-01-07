from datetime import date

from fastapi import APIRouter, Query
from models.wallet_models import WalletPnlResponse
from service.wallet_service import get_wallet_pnl

router = APIRouter(prefix="/api/hyperliquid", tags=["wallet related apis"])


@router.get("/{wallet}/pnl", response_model=WalletPnlResponse)
def wallet_pnl(
    wallet: str,
    start: date = Query(..., description="YYYY-MM-DD"),
    end: date = Query(..., description="YYYY-MM-DD"),
):
    if start > end:
        raise ValueError("Start date must be less than or equal to end date")

    daily = get_wallet_pnl(wallet, start, end)

    return WalletPnlResponse(
        wallet=wallet,
        start=start.isoformat(),
        end=end.isoformat(),
        daily=daily,
    )
