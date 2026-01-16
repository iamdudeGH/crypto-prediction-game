# 🔧 Web Fetching API Issue

## Current Error
```
"module 'genlayer.gl' has no attribute 'web_get'"
```

## Problem
The method `gl.web_get()` doesn't exist in the current GenLayer API.

## Possible Solutions

### Option 1: Use gl.http_get() or gl.fetch()
GenLayer might use a different method name. Common alternatives:
- `gl.http_get(url)`
- `gl.fetch(url)`
- `gl.web.get(url)`
- `gl.http.get(url)`

### Option 2: Use gl.nondet.web_get()
Web access might be under the non-deterministic namespace:
- `gl.nondet.web_get(url)`
- `gl.nondet.http_get(url)`

### Option 3: Use Python's requests (if allowed)
Some blockchain platforms allow standard Python libraries:
```python
import requests
response = requests.get(url)
```

### Option 4: Mock Data for Testing
For now, we can use mock data while waiting for GenLayer docs:
```python
def get_current_price(self, crypto_symbol: str) -> dict:
    # Mock prices for testing
    mock_prices = {
        "BTC": 4500000,  # $45,000.00 in cents
        "ETH": 250000,   # $2,500.00 in cents
        "SOL": 10000,    # $100.00 in cents
        "DOGE": 10,      # $0.10 in cents
        "ADA": 50        # $0.50 in cents
    }
    
    price_cents = mock_prices.get(crypto_symbol.upper(), 4500000)
    
    return {
        "symbol": crypto_symbol.upper(),
        "price_usd_cents": price_cents,
        "timestamp": gl.block.timestamp
    }
```

## What We Need

To fix this properly, we need to know:
1. What is the correct method for HTTP requests in GenLayer?
2. Is web access allowed in view methods?
3. Do we need special permissions or imports?

## Temporary Workaround

Let me create a version with mock data so you can test the rest of the contract logic while we figure out the correct web API.
