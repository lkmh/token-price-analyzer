from fastapi import FastAPI, HTTPException
from api.binance_client import get_kline_data, get_average_price

from datetime import datetime, timedelta

app = FastAPI()

# Simple in-memory cache
_cache = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/token_analysis")
async def token_analysis(symbol: str):
    # Check cache first
    if symbol in _cache and _cache[symbol]["expiry"] > datetime.now():
        return _cache[symbol]["data"]

    kline_data = await get_kline_data(symbol)
    if not kline_data:
        raise HTTPException(
            status_code=400, detail=f"Unable to fetch Kline data for {symbol}"
        )

    # Extract the last close price from the Kline data
    # Kline data format: [
    #   [
    #     1499040000000,      // Open time
    #     "0.01634790",       // Open
    #     "0.80000000",       // High
    #     "0.01575600",       // Low
    #     "0.01577100",       // Close   <-- This is the last close price
    #     "148.89765400",     // Volume
    #     1499644799999,      // Close time
    #     "2.43487897",       // Quote asset volume
    #     308,                // Number of trades
    #     "1756.87402397",    // Taker buy base asset volume
    #     "28.46694368",      // Taker buy quote asset volume
    #     "1792.349987"       // Ignore
    #   ]
    # ]
    last_close_price = float(kline_data[0][4])

    avg_price_data = await get_average_price(symbol)
    if not avg_price_data:
        raise HTTPException(
            status_code=400, detail=f"Unable to fetch average price data for {symbol}"
        )

    average_price = float(avg_price_data["price"])

    comparison = ""
    if last_close_price > average_price:
        comparison = "higher"
    elif last_close_price < average_price:
        comparison = "lower"
    else:
        comparison = "equal"

    response_data = {
        "symbol": symbol,
        "last_close_price": f"{last_close_price:.2f}",
        "average_price": f"{average_price:.2f}",
        "comparison": comparison,
    }

    # Store in cache
    _cache[symbol] = {
        "data": response_data,
        "expiry": datetime.now() + timedelta(minutes=1),
    }

    return response_data
