from datetime import date, timedelta
import os
from hyperliquid.info import Info

info = Info(os.environ["HYPERLIQUID_API_URL"], skip_ws=True)


def _day_ts_range(d: date):
    start = int(d.strftime("%s")) * 1000
    end = int((d + timedelta(days=1)).strftime("%s")) * 1000 - 1
    return start, end


def compute_unrealized_and_equity(wallet: str):
    state = info.user_state(wallet)

    # Equity (authoritative)
    equity = float(state["marginSummary"]["accountValue"])

    unrealized = 0.0

    for asset in state["assetPositions"]:
        pos = asset["position"]

        size = float(pos["szi"])
        if size == 0:
            continue

        # Hyperliquid already computes this correctly
        unrealized += float(pos["unrealizedPnl"])

    return unrealized, equity


def get_wallet_pnl(wallet: str, start: date, end: date):
    unrealized, base_equity = compute_unrealized_and_equity(wallet)

    results = []
    d = start

    while d <= end:
        start_ts, end_ts = _day_ts_range(d)

        fills = info.user_fills_by_time(wallet, start_ts, end_ts)
        funding_events = info.user_funding_history(wallet, start_ts, end_ts)

        realized = sum(float(f.get("closedPnl", 0)) for f in fills)
        fees = sum(float(f.get("fee", 0)) for f in fills)
        funding = sum(float(ev["delta"]["usdc"]) for ev in funding_events)

        net = realized + unrealized - fees + funding
        equity = base_equity

        results.append(
            {
                "date": d.isoformat(),
                "realized_pnl_usd": round(realized, 2),
                "unrealized_pnl_usd": round(unrealized, 2),
                "fees_usd": round(fees, 2),
                "funding_usd": round(funding, 2),
                "net_pnl_usd": round(net, 2),
                "equity_usd": round(equity, 2),
            }
        )

        d += timedelta(days=1)

    return results
