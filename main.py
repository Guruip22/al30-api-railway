from fastapi import FastAPI, HTTPException
import os, datetime
from pyhomebroker import HomeBroker

app = FastAPI(title="AL30 Arbitrage API")

DNI       = os.getenv("HB_DNI")
USER      = os.getenv("HB_USER")
PASSWORD  = os.getenv("HB_PASS")
BROKER_ID = os.getenv("HB_BROKER", "invertironline")

def get_prices():
    hb = HomeBroker(broker=BROKER_ID)
    if not hb.session.login(dni=DNI, user=USER, password=PASSWORD, raise_exception=True):
        raise HTTPException(401, "Login failed")

    def _p(settlement):
        md = hb.markets.get_market_data(ticker="AL30", settlement=settlement)
        return float(md.last)

    price_ci  = _p("CI")
    price_24  = _p("24")
    spread_pct = abs(price_ci - price_24) / price_ci * 100
    hb.session.logout()
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "price_ci": price_ci,
        "price_24": price_24,
        "spread_pct": round(spread_pct, 4)
    }

@app.get("/prices")
async def prices():
    return get_prices()
