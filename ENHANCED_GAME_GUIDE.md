# 🎯 Enhanced Crypto Prediction Game - Complete Guide

## What's New in Enhanced Version?

### ✨ Key Features

1. **✅ Multi-User Support** - Multiple players can play simultaneously
2. **⏰ Time-Based Settlement** - Predictions expire after a set duration
3. **🌐 Real API + Fallback** - Uses CryptoCompare API, falls back to mock prices
4. **📊 Multiple Predictions** - Users can have multiple active predictions
5. **🏆 Enhanced Leaderboard** - Track by wins OR profit
6. **📈 Comprehensive Stats** - Detailed user and game statistics
7. **🔄 Auto-Settlement** - Settle all ready predictions at once
8. **⚡ Better Error Handling** - Clear error messages and validation

---

## 🚀 Quick Start

### 1. Deploy the Contract

```python
# In GenLayer Studio:
# 1. Copy crypto_prediction_game_enhanced.py
# 2. Deploy to GenLayer
# 3. Note the contract address
```

### 2. Initial Setup

```python
# Deposit initial balance
contract.deposit("your_address_here", 1000)

# Check balance
contract.get_balance("your_address_here")
```

### 3. Place Your First Prediction

```python
# Predict BTC will go UP in 60 seconds, bet 100 tokens
contract.place_prediction(
    "your_address_here",  # Your wallet address
    "BTC",                # Crypto symbol
    "UP",                 # Direction (UP or DOWN)
    100,                  # Bet amount
    60                    # Duration in seconds
)
```

### 4. Wait for Expiry

```python
# Check prediction status
contract.get_prediction_details(0)  # prediction_id from step 3

# Simulate time passing (advance transaction counter)
contract.advance_time()
contract.advance_time()
contract.advance_time()
# ... call multiple times or make other transactions
```

### 5. Settle and Win!

```python
# Settle specific prediction
contract.settle_prediction("your_address_here", 0)

# OR settle all ready predictions at once
contract.settle_all_ready("your_address_here")
```

---

## 📖 Complete Function Reference

### 💰 Balance Management

#### `deposit(user_address: str, amount: u256) -> str`
Deposit tokens to your balance.
```python
contract.deposit("0xABC123...", 1000)
# ✅ Deposited 1000 tokens. New balance: 1000
```

#### `get_balance(user_address: str) -> u256`
Check your current balance.
```python
contract.get_balance("0xABC123...")
# 1000
```

#### `get_user_stats(user_address: str) -> dict`
Get comprehensive user statistics.
```python
contract.get_user_stats("0xABC123...")
# {
#   "balance": 1350,
#   "total_predictions": 5,
#   "active": 1,
#   "won": 3,
#   "lost": 1,
#   "expired": 0,
#   "win_rate_percent": 75,
#   "total_profit": 350
# }
```

---

### 🎯 Prediction Functions

#### `place_prediction(user_address, crypto_symbol, direction, bet_amount, duration_seconds) -> str`
Place a new prediction.

**Parameters:**
- `user_address` (str): Your wallet address
- `crypto_symbol` (str): BTC, ETH, SOL, DOGE, or ADA
- `direction` (str): "UP" or "DOWN"
- `bet_amount` (u256): Amount to bet (10-10000)
- `duration_seconds` (u256): Time until settlement (default 60)

**Examples:**
```python
# Quick 30-second BTC prediction
contract.place_prediction("0xABC...", "BTC", "UP", 100, 30)

# 2-minute ETH prediction
contract.place_prediction("0xABC...", "ETH", "DOWN", 200, 120)

# High-stakes 5-minute SOL prediction
contract.place_prediction("0xABC...", "SOL", "UP", 500, 300)
```

#### `settle_prediction(user_address: str, prediction_id: u256) -> str`
Settle a specific prediction.

```python
contract.settle_prediction("0xABC123...", 0)
# 🎉 YOU WON!
# Prediction #0: UP on BTC
# Entry: $95000.00 → Exit: $96200.00 (+1.26%)
# Bet: 100 | Payout: 180 | Profit: +80
# New Balance: 1180
```

#### `settle_all_ready(user_address: str) -> str`
Auto-settle all predictions that are ready.

```python
contract.settle_all_ready("0xABC123...")
# ✅ Settled 3 predictions:
# #0: 🎉 YOU WON! Prediction #0: U...
# #1: 😔 You Lost Prediction #1: D...
# #2: 🎉 YOU WON! Prediction #2: U...
```

#### `get_prediction_details(prediction_id: u256) -> dict`
Get detailed info about a prediction.

```python
contract.get_prediction_details(0)
# {
#   "id": 0,
#   "symbol": "BTC",
#   "direction": "UP",
#   "amount": 100,
#   "entry_price_cents": 9500000,
#   "entry_price_usd": 95000.0,
#   "status": "ACTIVE",
#   "owner": "0xABC123...",
#   "creation_tx": 5,
#   "duration_tx": 6,
#   "tx_passed": 3,
#   "tx_remaining": 3,
#   "ready_to_settle": false
# }
```

#### `get_active_predictions(user_address: str) -> str`
List all your active predictions.

```python
contract.get_active_predictions("0xABC123...")
# #0: UP on BTC | $95000.00 | 100 tokens | ⏳ 3 tx left
# #2: DOWN on ETH | $3500.00 | 200 tokens | ✅ READY
# #5: UP on SOL | $150.00 | 50 tokens | ⏳ 8 tx left
```

---

### 🏆 Leaderboard & Stats

#### `get_leaderboard(sort_by: str = "wins") -> str`
Get top 10 players.

**Sort options:** "wins" or "profit"

```python
# Sort by wins
contract.get_leaderboard("wins")
# 🏆 Top Players by Wins:
# 1. 0xABC123... - 15 wins (+2500 profit)
# 2. 0xDEF456... - 12 wins (+1800 profit)
# 3. 0xGHI789... - 10 wins (+1200 profit)

# Sort by profit
contract.get_leaderboard("profit")
# 🏆 Top Players by Profit:
# 1. 0xABC123... - +2500 tokens
# 2. 0xDEF456... - +1800 tokens
# 3. 0xGHI789... - +1200 tokens
```

#### `get_game_stats() -> dict`
Get overall game statistics.

```python
contract.get_game_stats()
# {
#   "total_predictions": 147,
#   "active_predictions": 12,
#   "won": 68,
#   "lost": 65,
#   "expired": 2,
#   "unique_players": 25,
#   "total_pool": 45000,
#   "transaction_counter": 523
# }
```

---

### 🛠️ Utility Functions

#### `get_current_price(crypto_symbol: str) -> dict`
Get current crypto price (real API or mock).

```python
contract.get_current_price("BTC")
# {
#   "symbol": "BTC",
#   "price_usd_cents": 9500000,
#   "source": "api"  # or "mock" if API failed
# }
```

#### `advance_time() -> str`
Simulate time passing (increment transaction counter).

```python
contract.advance_time()
# ⏰ Time advanced! Transaction #25
```

#### `get_current_transaction() -> u256`
Get current transaction counter.

```python
contract.get_current_transaction()
# 25
```

---

## 🎮 Gameplay Examples

### Example 1: Quick Game Session

```python
# 1. Setup
contract.deposit("0xABC...", 1000)

# 2. Place multiple predictions
contract.place_prediction("0xABC...", "BTC", "UP", 100, 60)    # Prediction #0
contract.place_prediction("0xABC...", "ETH", "DOWN", 150, 60)  # Prediction #1
contract.place_prediction("0xABC...", "SOL", "UP", 200, 120)   # Prediction #2

# 3. Check active predictions
contract.get_active_predictions("0xABC...")

# 4. Advance time (simulate 60+ seconds passing)
for i in range(8):
    contract.advance_time()

# 5. Settle all ready predictions
contract.settle_all_ready("0xABC...")

# 6. Check your stats
contract.get_user_stats("0xABC...")
```

### Example 2: Different Strategies

```python
# Conservative: Small bets, multiple predictions
contract.place_prediction("0xABC...", "BTC", "UP", 50, 30)
contract.place_prediction("0xABC...", "ETH", "UP", 50, 30)
contract.place_prediction("0xABC...", "SOL", "UP", 50, 30)

# Aggressive: Large bet on one prediction
contract.place_prediction("0xABC...", "BTC", "UP", 500, 120)

# Diversified: Mix of UP and DOWN
contract.place_prediction("0xABC...", "BTC", "UP", 100, 60)
contract.place_prediction("0xABC...", "BTC", "DOWN", 100, 60)
```

### Example 3: Multi-User Competition

```python
# User A
contract.deposit("0xAAA...", 1000)
contract.place_prediction("0xAAA...", "BTC", "UP", 200, 60)

# User B
contract.deposit("0xBBB...", 1000)
contract.place_prediction("0xBBB...", "BTC", "DOWN", 200, 60)

# Advance time
for i in range(10):
    contract.advance_time()

# Both settle
contract.settle_prediction("0xAAA...", 0)
contract.settle_prediction("0xBBB...", 1)

# Check leaderboard
contract.get_leaderboard("profit")
```

---

## ⚙️ How It Works

### Time-Based Settlement

The contract uses a **transaction counter** instead of real timestamps:

1. Each write transaction increments `transaction_counter`
2. Predictions store `creation_tx` and `duration_tx`
3. Settlement is allowed when: `current_tx - creation_tx >= duration_tx`
4. Approximate conversion: **1 transaction ≈ 10 seconds**

**Example:**
- Place prediction at TX #10, duration 60s (6 tx)
- Prediction can be settled at TX #16 or later
- Call `advance_time()` or make other transactions to advance the counter

### Price Fetching

1. **Primary:** Fetch from CryptoCompare API
2. **Fallback:** Use mock prices with ±10% variation
3. Mock prices use `price_counter` for realistic variation

### Payout Calculation

- **Win:** 1.8x your bet (stored as 18/10)
- **Lose:** Lose your bet
- **Example:** Bet 100, win 180 (80 profit)

---

## 🎯 Supported Cryptocurrencies

| Symbol | Name | Mock Base Price |
|--------|------|-----------------|
| BTC | Bitcoin | $95,000 |
| ETH | Ethereum | $3,500 |
| SOL | Solana | $150 |
| DOGE | Dogecoin | $0.35 |
| ADA | Cardano | $0.95 |

---

## 🐛 Troubleshooting

### "Too early! Need X more transactions"
**Solution:** Call `advance_time()` multiple times or make other transactions.

```python
for i in range(10):
    contract.advance_time()
```

### "Insufficient balance"
**Solution:** Deposit more tokens.

```python
contract.deposit("your_address", 500)
```

### "Failed to fetch price"
**Solution:** Contract automatically falls back to mock prices. Try again.

### "Not your prediction"
**Solution:** Make sure you're using the correct user address that placed the prediction.

---

## 📊 Best Practices

### 1. Start Small
```python
# Test with small bets first
contract.place_prediction("0xABC...", "BTC", "UP", 10, 30)
```

### 2. Diversify
```python
# Don't put all tokens in one prediction
contract.place_prediction("0xABC...", "BTC", "UP", 100, 60)
contract.place_prediction("0xABC...", "ETH", "DOWN", 100, 60)
contract.place_prediction("0xABC...", "SOL", "UP", 100, 60)
```

### 3. Monitor Active Predictions
```python
# Check regularly
contract.get_active_predictions("0xABC...")
```

### 4. Use Auto-Settlement
```python
# Settle all ready predictions at once
contract.settle_all_ready("0xABC...")
```

### 5. Track Your Performance
```python
# Review stats periodically
contract.get_user_stats("0xABC...")
```

---

## 🎯 Contract Limits

- **Min Bet:** 10 tokens
- **Max Bet:** 10,000 tokens
- **Min Deposit:** 100 tokens
- **Min Duration:** 10 seconds (1 tx)
- **Payout Multiplier:** 1.8x

---

## 🚀 Next Steps

1. **Deploy:** Copy `crypto_prediction_game_enhanced.py` to GenLayer Studio
2. **Test:** Follow the Quick Start guide above
3. **Play:** Invite friends and compete on the leaderboard!
4. **Integrate:** Connect the frontend UI (coming soon)

---

## 📝 Version History

- **v1.0.0** - Initial enhanced release
  - Multi-user support
  - Time-based settlement
  - Real API + fallback
  - Multiple predictions
  - Enhanced leaderboard
  - Comprehensive stats

---

**Happy Predicting! 🎯🚀**
