from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch
import pytest

client = TestClient(app)


@pytest.mark.asyncio
async def test_token_analysis_success():
    mock_kline_data = [[1, 10, 20, 15, "42500.00", 100, 0, 0, 0, 0, 0, 0]]
    mock_avg_price_data = {"mins": 5, "price": "42450.50"}

    with (
        patch("main.get_kline_data", new_callable=AsyncMock) as mock_get_kline_data,
        patch(
            "main.get_average_price", new_callable=AsyncMock
        ) as mock_get_average_price,
    ):
        mock_get_kline_data.return_value = mock_kline_data
        mock_get_average_price.return_value = mock_avg_price_data

        response = client.get("/token_analysis?symbol=BTCUSDT")
        assert response.status_code == 200
        assert response.json() == {
            "symbol": "BTCUSDT",
            "last_close_price": "42500.00",
            "average_price": "42450.50",
            "comparison": "higher",
        }


@pytest.mark.asyncio
async def test_token_analysis_kline_data_failure():
    with (
        patch("main.get_kline_data", new_callable=AsyncMock) as mock_get_kline_data,
        patch(
            "main.get_average_price", new_callable=AsyncMock
        ) as mock_get_average_price,
    ):
        mock_get_kline_data.return_value = []
        mock_get_average_price.return_value = {"mins": 5, "price": "42450.50"}

        response = client.get("/token_analysis?symbol=BTCUSDT")
        assert response.status_code == 400
        assert response.json() == {"detail": "Unable to fetch Kline data for BTCUSDT"}


@pytest.mark.asyncio
async def test_token_analysis_avg_price_data_failure():
    mock_kline_data = [[1, 10, 20, 15, "42500.00", 100, 0, 0, 0, 0, 0, 0]]

    with (
        patch("main.get_kline_data", new_callable=AsyncMock) as mock_get_kline_data,
        patch(
            "main.get_average_price", new_callable=AsyncMock
        ) as mock_get_average_price,
    ):
        mock_get_kline_data.return_value = mock_kline_data
        mock_get_average_price.return_value = {}

        response = client.get("/token_analysis?symbol=BTCUSDT")
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Unable to fetch average price data for BTCUSDT"
        }


@pytest.mark.asyncio
async def test_token_analysis_comparison_lower():
    mock_kline_data = [[1, 10, 20, 15, "42000.00", 100, 0, 0, 0, 0, 0, 0]]
    mock_avg_price_data = {"mins": 5, "price": "42450.50"}

    with (
        patch("main.get_kline_data", new_callable=AsyncMock) as mock_get_kline_data,
        patch(
            "main.get_average_price", new_callable=AsyncMock
        ) as mock_get_average_price,
    ):
        mock_get_kline_data.return_value = mock_kline_data
        mock_get_average_price.return_value = mock_avg_price_data

        response = client.get("/token_analysis?symbol=BTCUSDT")
        assert response.status_code == 200
        assert response.json() == {
            "symbol": "BTCUSDT",
            "last_close_price": "42000.00",
            "average_price": "42450.50",
            "comparison": "lower",
        }


@pytest.mark.asyncio
async def test_token_analysis_comparison_equal():
    mock_kline_data = [[1, 10, 20, 15, "42450.50", 100, 0, 0, 0, 0, 0, 0]]
    mock_avg_price_data = {"mins": 5, "price": "42450.50"}

    with (
        patch("main.get_kline_data", new_callable=AsyncMock) as mock_get_kline_data,
        patch(
            "main.get_average_price", new_callable=AsyncMock
        ) as mock_get_average_price,
    ):
        mock_get_kline_data.return_value = mock_kline_data
        mock_get_average_price.return_value = mock_avg_price_data

        response = client.get("/token_analysis?symbol=BTCUSDT")
        assert response.status_code == 200
        assert response.json() == {
            "symbol": "BTCUSDT",
            "last_close_price": "42450.50",
            "average_price": "42450.50",
            "comparison": "equal",
        }
