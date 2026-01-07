from typing import List, Optional

from pydantic import BaseModel


class DailyPnl(BaseModel):
    date: str
    realized_pnl_usd: float
    unrealized_pnl_usd: Optional[float]
    fees_usd: float
    funding_usd: float
    net_pnl_usd: Optional[float]
    equity_usd: Optional[float]


class WalletPnlResponse(BaseModel):
    wallet: str
    start: str
    end: str
    daily: List[DailyPnl]
