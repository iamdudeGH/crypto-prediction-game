# 🚀 Quick Deploy Guide - Enhanced Crypto Prediction Game

## ✅ What Was Fixed

**Issue:** GenLayer Studio showed "invalid_contract" error

**Root Cause:** Private methods (starting with `_`) are not supported in GenLayer contracts

**Solution:** Renamed private methods:
- `_fetch_real_price()` → `fetch_real_price()`
- `_get_mock_price()` → `get_mock_price()`

---

## 🎯 Ready to Deploy: `crypto_prediction_game_enhanced.py`

### Features
✅ Multi-user support  
✅ Time-based settlement (transaction counter)  
✅ Real API + Mock fallback  
✅ Multiple predictions per user  
✅ Leaderboard (by wins or profit)  
✅ Auto-settle all ready predictions  
✅ Comprehensive stats  

---

## 📋 Deployment Steps

### 1. Open GenLayer Studio
Go to: https://studio.genlayer.com

### 2. Load the Contract
- Copy the entire contents of `crypto_prediction_game_enhanced.py`
- Paste into GenLayer Studio editor
- Click "Deploy"

### 3. Quick Test Commands

```python
# 1. Setup - deposit tokens
contract.deposit("0xYourAddress", 1000)

# 2. Check balance
contract.get_balance("0xYourAddress")
# Returns: 1000

# 3. Place a prediction
contract.place_prediction(
    "0xYourAddress",  # Your wallet address
    "BTC",            # Crypto: BTC, ETH, SOL, DOGE, ADA
    "UP",             # Direction: UP or DOWN
    100,              # Bet amount
    60                # Duration in seconds
)
# Returns: ✅ Prediction #0 placed! ...

# 4. Simulate time passing (need ~6 transactions for 60 seconds)
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()

# 5. Check if ready to settle
contract.get_prediction_details(0)
# Check "ready_to_settle": true

# 6. Settle the prediction
contract.settle_prediction("0xYourAddress", 0)
# Returns: 🎉 YOU WON! or 😔 You Lost

# 7. Check your stats
contract.get_user_stats("0xYourAddress")
# Returns: {"balance": ..., "won": ..., "lost": ..., ...}
```

---

## 🎮 Multi-User Example

```python
# User 1 joins
contract.deposit("0xUser1", 1000)
contract.place_prediction("0xUser1", "BTC", "UP", 200, 60)

# User 2 joins
contract.deposit("0xUser2", 1000)
contract.place_prediction("0xUser2", "BTC", "DOWN", 200, 60)

# User 3 joins
contract.deposit("0xUser3", 1000)
contract.place_prediction("0xUser3", "ETH", "UP", 150, 60)

# Advance time
for i in range(10):
    contract.advance_time()

# Everyone settles
contract.settle_all_ready("0xUser1")
contract.settle_all_ready("0xUser2")
contract.settle_all_ready("0xUser3")

# Check leaderboard
contract.get_leaderboard("wins")
contract.get_leaderboard("profit")

# Check game stats
contract.get_game_stats()
```

---

## 🔧 Utility Commands

### Check Active Predictions
```python
contract.get_active_predictions("0xYourAddress")
```

### Check Specific Prediction
```python
contract.get_prediction_details(0)  # prediction_id
```

### Get Current Price (for testing)
```python
contract.get_current_price("BTC")
# Returns: {"symbol": "BTC", "price_usd_cents": 9500000, "source": "api"}
```

### Advance Time Manually
```python
contract.advance_time()
# Returns: ⏰ Time advanced! Transaction #25
```

### Check Transaction Counter
```python
contract.get_current_transaction()
# Returns: 25
```

---

## 📊 Understanding Time-Based Settlement

The contract uses a **transaction counter** to simulate time:

- **1 transaction ≈ 10 seconds**
- Duration 60s = 6 transactions
- Duration 120s = 12 transactions

**Example:**
- Place prediction at TX #5 with 60s duration (6 tx)
- Can settle at TX #11 or later (5 + 6 = 11)

**Ways to advance time:**
1. Call `contract.advance_time()` multiple times
2. Make other transactions (deposit, place predictions, etc.)
3. Other users' transactions also advance the counter

---

## 🎯 Supported Cryptocurrencies

| Symbol | Full Name | Mock Base Price |
|--------|-----------|-----------------|
| BTC    | Bitcoin   | $95,000         |
| ETH    | Ethereum  | $3,500          |
| SOL    | Solana    | $150            |
| DOGE   | Dogecoin  | $0.35           |
| ADA    | Cardano   | $0.95           |

---

## 💡 Pro Tips

### 1. Start with Small Bets
```python
contract.place_prediction("0xAddr", "BTC", "UP", 10, 30)
```

### 2. Use Auto-Settlement
```python
# Instead of settling each prediction individually:
contract.settle_all_ready("0xYourAddress")
```

### 3. Check Before Settling
```python
# See if predictions are ready:
contract.get_active_predictions("0xYourAddress")
```

### 4. Monitor Your Stats
```python
contract.get_user_stats("0xYourAddress")
# Shows: balance, win rate, profit, etc.
```

### 5. Compete on Leaderboard
```python
# See top players by wins
contract.get_leaderboard("wins")

# See top players by profit
contract.get_leaderboard("profit")
```

---

## 🐛 Common Issues

### "Too early! Need X more transactions"
**Solution:**
```python
# Call advance_time() multiple times
for i in range(10):
    contract.advance_time()
```

### "Insufficient balance"
**Solution:**
```python
contract.deposit("0xYourAddress", 500)
```

### "Direction must be UP or DOWN"
**Solution:** Use uppercase strings
```python
contract.place_prediction("0xAddr", "BTC", "UP", 100, 60)  # ✅
contract.place_prediction("0xAddr", "BTC", "up", 100, 60)  # ✅ (auto-converted)
```

### Contract won't deploy - "invalid_contract"
**Solution:** Make sure you're using the **fixed** version from `crypto_prediction_game_enhanced.py` (not the old version with private methods)

---

## 📖 Full Documentation

For detailed function reference and examples, see:
- `ENHANCED_GAME_GUIDE.md` - Complete function reference
- `README.md` - Project overview

---

## ✅ Contract Validation

The enhanced contract has been fixed for:
- ✅ No private methods (GenLayer compatibility)
- ✅ TreeMaps properly declared
- ✅ All return types compatible
- ✅ Time-based settlement working
- ✅ Multi-user support enabled
- ✅ Real API + fallback implemented

---

**Ready to play! 🎮 Deploy and start predicting!**
