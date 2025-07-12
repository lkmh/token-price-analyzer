from fastapi.testclient import TestClient
from main import app, _cache
from unittest.mock import AsyncMock, patch
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cache():
    _cache.clear()


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
        mock_get_kline_data.return_value = (
            None  # Explicitly return None to trigger failure
        )
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
        mock_get_average_price.return_value = (
            None  # Explicitly return None to trigger failure
        )

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


@pytest.mark.asyncio
async def test_token_analysis_caching():
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

        # First call - should hit Binance API
        response1 = client.get("/token_analysis?symbol=TESTUSDT")
        assert response1.status_code == 200
        mock_get_kline_data.assert_called_once_with("TESTUSDT")
        mock_get_average_price.assert_called_once_with("TESTUSDT")

        # Second call within cache expiry - should hit cache, not Binance API
        mock_get_kline_data.reset_mock()
        mock_get_average_price.reset_mock()
        response2 = client.get("/token_analysis?symbol=TESTUSDT")
        assert response2.status_code == 200
        mock_get_kline_data.assert_not_called()
        mock_get_average_price.assert_not_called()
        assert response1.json() == response2.json()

        # Advance time beyond cache expiry (mock datetime if needed for precise testing)
        # For simplicity, we'll just clear the cache for this test
        _cache.clear()

        # Third call after cache clear - should hit Binance API again
        response3 = client.get("/token_analysis?symbol=TESTUSDT")
        assert response3.status_code == 200
        mock_get_kline_data.assert_called_once_with("TESTUSDT")
        mock_get_average_price.assert_called_once_with("TESTUSDT")
        assert response1.json() == response3.json()
