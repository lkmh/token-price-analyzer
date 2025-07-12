import httpx

BINANCE_API_BASE_URL = "https://api.binance.com"


async def get_kline_data(symbol: str, interval: str = "1m", limit: int = 1):
    """Fetches Kline (candlestick) data for a given symbol.

    Args:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        interval (str): The candlestick interval (e.g., "1m", "1h", "1d").
        limit (int): The number of candlesticks to retrieve.

    Returns:
        list: A list of Kline data, or an empty list if an error occurs.
    """
    url = f"{BINANCE_API_BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
    except httpx.HTTPStatusError as e:
        print(
            f"Error fetching Kline data: {e.response.status_code} - {e.response.text}"
        )
        return []
    except httpx.RequestError as e:
        print(f"An error occurred while requesting Kline data: {e}")
        return []


async def get_average_price(symbol: str):
    """Fetches the average price for a given symbol.

    Args:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").

    Returns:
        dict: A dictionary containing the average price, or an empty dictionary if an error occurs.
    """
    url = f"{BINANCE_API_BASE_URL}/api/v3/avgPrice"
    params = {"symbol": symbol}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
    except httpx.HTTPStatusError as e:
        print(
            f"Error fetching average price: {e.response.status_code} - {e.response.text}"
        )
        return {}
    except httpx.RequestError as e:
        print(f"An error occurred while requesting average price: {e}")
        return {}
