import pytest
from unittest.mock import AsyncMock, patch
from api.binance_client import get_kline_data, get_average_price


@pytest.mark.asyncio
async def test_get_kline_data_success():
    mock_response = AsyncMock()
    mock_response.json.return_value = [[1, 10, 20, 15, 12, 100, 0, 0, 0, 0, 0, 0]]
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value.get.return_value = (
            mock_response
        )
        data = await get_kline_data("BTCUSDT")
        assert data == [[1, 10, 20, 15, 12, 100, 0, 0, 0, 0, 0, 0]]


@pytest.mark.asyncio
async def test_get_kline_data_http_error():
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Bad Request", request=httpx.Request("GET", "url"), response=httpx.Response(400)
    )

    with patch("httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value.get.return_value = (
            mock_response
        )
        data = await get_kline_data("BTCUSDT")
        assert data == []


@pytest.mark.asyncio
async def test_get_kline_data_request_error():
    with patch("httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value.get.side_effect = (
            httpx.RequestError("Network Error", request=httpx.Request("GET", "url"))
        )
        data = await get_kline_data("BTCUSDT")
        assert data == []


@pytest.mark.asyncio
async def test_get_average_price_success():
    mock_response = AsyncMock()
    mock_response.json.return_value = {"mins": 5, "price": "42500.00"}
    mock_response.raise_for_status.return_value = None

    with patch("httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value.get.return_value = (
            mock_response
        )
        data = await get_average_price("BTCUSDT")
        assert data == {"mins": 5, "price": "42500.00"}


@pytest.mark.asyncio
async def test_get_average_price_http_error():
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not Found", request=httpx.Request("GET", "url"), response=httpx.Response(404)
    )

    with patch("httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value.get.return_value = (
            mock_response
        )
        data = await get_average_price("BTCUSDT")
        assert data == {}


@pytest.mark.asyncio
async def test_get_average_price_request_error():
    with patch("httpx.AsyncClient") as mock_async_client:
        mock_async_client.return_value.__aenter__.return_value.get.side_effect = (
            httpx.RequestError("Connection Error", request=httpx.Request("GET", "url"))
        )
        data = await get_average_price("BTCUSDT")
        assert data == {}
