# Token Price Analyzer

Product Requirements Document (PRD): Token Price Analyzer
1. Introduction
Project Name: Token Price Analyzer
Goal: To provide users with a simple API to compare the last known close price of a token to its average price, indicating whether the recent price is above or below the average.
2. User Stories
As an API user, I want to be able to provide a token symbol and receive the latest close price and the average price.
As an API user, I want to know if the current close price is higher or lower than the average price.
As an API user, I want the data to be reasonably up-to-date (within a few minutes).
3. Features
Core Functionality:
The following base endpoints are available. Please use whichever works best for your setup:
https://api.binance.com
An API endpoint that accepts a token symbol (symbol) as a parameter.
Fetches Kline data (candlestick data) for the specified token symbol from the /api/v3/klines endpoint.
Fetches average price data for the specified token symbol from the /api/v3/avgPrice endpoint.
Calculates the average price based on the Kline data (or uses the avgPrice endpoint, see decisions below).
Compares the latest close price from the Kline data with the average price.
Returns a JSON response indicating the last close price, the average price, and whether the close price is "higher", "lower", or "equal" to the average price.
API Endpoints:
GET /token_analysis?symbol={token_symbol}
4. API Specifications
Endpoint: GET /token_analysis
Parameters:
symbol (STRING, required): The token symbol (e.g., "BTCUSDT").
Request Example: GET /token_analysis?symbol=BTCUSDT
Response:
Generated json
{
  "symbol": "BTCUSDT",
  "last_close_price": "42500.00",
  "average_price": "42450.50",
  "comparison": "higher"  // Can be "higher", "lower", or "equal"
}
Use code with caution.
Json
Error Handling: If there are issues retrieving data from the klines endpoint or the avgPrice endpoint, return an appropriate error response.
Generated json
{
    "error": "Unable to fetch Kline data for BTCUSDT"
}
Use code with caution.
Json
5. Data Sources
Kline Data: /api/v3/klines
Average Price Data: /api/v3/avgPrice
6. Technical Design
Language: Python
Framework: FastAPI
Package Manager: uv + pip (use uv where possible)
Testing: pytest
Linting/Formatting: ruff
CI/CD: GitHub Actions
## How to Run

1. **Set up the virtual environment:**
   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

7. Implementation Details
Data Retrieval:
Implement functions to fetch data from both the /api/v3/klines and /api/v3/avgPrice endpoints.
Consider caching the data to reduce the load on the external API (implement a cache with a reasonable expiration time, e.g., 1 minute).
Average Price Calculation:
Decision: Initially, use the avgPrice endpoint directly. This simplifies the implementation.
Future Consideration: If the avgPrice endpoint is unreliable or unavailable, implement the average price calculation from the Kline data.
Further detail on the future consideration: When calculating average price from klines, the formula to use would be the average of ((high price + low price) / 2), over the entire period of klines to average.
Error Handling:
Implement proper error handling to gracefully handle API errors and data retrieval failures.
API Rate Limiting: Be mindful of rate limits on the external APIs. Implement retry mechanisms and error handling to avoid being blocked.
Asynchronous Operations: Use async and await to handle network requests efficiently.
