# 🧪 Test Guide - Final Crypto Prediction Game

## ✅ Contract Deployed Successfully!

**File:** `crypto_prediction_game_final.py`
**Version:** v0.1.0 (changed from v0.2.0)

---

## 🎯 What's New - Time-Based Settlement

This version adds **transaction-based time tracking**:
- ⏰ Predictions must wait for a specific number of transactions before settling
- 📊 Transaction counter tracks "time" progression
- 🔄 `advance_time()` function to simulate time passing
- ✅ Prevents early settlement

**Time Conversion:**
- **1 transaction ≈ 10 seconds**
- 60 seconds = 6 transactions
- 120 seconds = 12 transactions

---

## 🧪 Test Sequence

### Test 1: Basic Deposit & Balance
```python
# Deposit funds
contract.deposit("0xYourAddress", 1000)
# Expected: "Deposited 1000. New balance: 1000"

# Check balance
contract.get_balance("0xYourAddress")
# Expected: 1000
```

### Test 2: Place Prediction
```python
# Place a 60-second prediction
contract.place_prediction("0xYourAddress", "BTC", "UP", 100, 60)
# Expected: "Prediction #0 placed: UP on BTC at $95000.00 | Bet: 100 | Expires in 6 transactions (~60s) | Source: api or mock"

# Check balance (should be reduced)
contract.get_balance("0xYourAddress")
# Expected: 900 (1000 - 100)
```

### Test 3: Try Early Settlement (Should Fail)
```python
# Try to settle immediately
contract.settle_prediction("0xYourAddress", 0)
# Expected: "ERROR: Too early to settle. Need X more transactions. Call advance_time() or make other transactions."

# Check prediction details
contract.get_prediction_details(0)
# Expected: "Prediction #0: UP on BTC | Bet: 100 | Entry: $95000.00 | X tx remaining | Owner: 0xYourAdd..."
```

### Test 4: Advance Time
```python
# Check current transaction counter
contract.get_current_transaction()
# Expected: Some number (e.g., 2)

# Advance time 6 times
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()

# Check transaction counter again
contract.get_current_transaction()
# Expected: Previous number + 6
```

### Test 5: Settle After Time Expires
```python
# Check if ready
contract.get_prediction_details(0)
# Expected: "...Ready to settle!..."

# Settle the prediction
contract.settle_prediction("0xYourAddress", 0)
# Expected: "Settled: WON - Entry: $95000.00, Exit: $96200.00, Payout: 180, New Balance: 1080"
# OR: "Settled: LOST - Entry: $95000.00, Exit: $94500.00, Payout: 0, New Balance: 900"
```

### Test 6: Check Stats
```python
# Check your predictions
contract.get_user_predictions("0xYourAddress")
# Expected: "Total: 1 predictions (Active: 0, Won: 1, Lost: 0)"
# OR: "Total: 1 predictions (Active: 0, Won: 0, Lost: 1)"

# Check leaderboard
contract.get_leaderboard()
# Expected: "Leaderboard:\n1. 0xYourAdd... - 1 wins\n"
# (only shows if you won)

# Check game stats
contract.get_game_stats()
# Expected: "Total predictions: 1, Total players: 1, Total in pool: 1080 (or 900), Transaction counter: X"
```

---

## 🎮 Test 7: Multi-User Scenario

```python
# User 1 deposits and predicts UP
contract.deposit("0xUser1", 1000)
contract.place_prediction("0xUser1", "BTC", "UP", 200, 60)

# User 2 deposits and predicts DOWN
contract.deposit("0xUser2", 1000)
contract.place_prediction("0xUser2", "BTC", "DOWN", 200, 60)

# User 3 deposits and predicts on ETH
contract.deposit("0xUser3", 1000)
contract.place_prediction("0xUser3", "ETH", "UP", 150, 60)

# Advance time (enough for all predictions)
for i in range(10):
    contract.advance_time()

# All users settle
contract.settle_prediction("0xUser1", 1)  # or whatever ID was returned
contract.settle_prediction("0xUser2", 2)
contract.settle_prediction("0xUser3", 3)

# Check leaderboard
contract.get_leaderboard()

# Check game stats
contract.get_game_stats()
```

---

## 🧪 Test 8: Multiple Predictions per User

```python
# Deposit
contract.deposit("0xYourAddress", 2000)

# Place 3 predictions with different durations
contract.place_prediction("0xYourAddress", "BTC", "UP", 100, 30)    # 3 tx
contract.place_prediction("0xYourAddress", "ETH", "DOWN", 200, 60)  # 6 tx
contract.place_prediction("0xYourAddress", "SOL", "UP", 150, 120)   # 12 tx

# Check all predictions
contract.get_user_predictions("0xYourAddress")
# Expected: "Total: 3 predictions (Active: 3, Won: 0, Lost: 0)"

# Advance time partially (4 transactions)
for i in range(4):
    contract.advance_time()

# Check which are ready
contract.get_prediction_details(0)  # Should be ready (3 tx needed)
contract.get_prediction_details(1)  # Should be ready (6 tx needed? Check actual ID)
contract.get_prediction_details(2)  # Should NOT be ready (12 tx needed)

# Settle the ready ones
contract.settle_prediction("0xYourAddress", 0)
contract.settle_prediction("0xYourAddress", 1)

# Try to settle the one that's not ready (should fail)
contract.settle_prediction("0xYourAddress", 2)
# Expected: ERROR: Too early...

# Advance more time and settle the last one
for i in range(10):
    contract.advance_time()

contract.settle_prediction("0xYourAddress", 2)
```

---

## 🧪 Test 9: Different Cryptocurrencies

```python
# Test all supported cryptos
contract.deposit("0xYourAddress", 3000)

contract.place_prediction("0xYourAddress", "BTC", "UP", 100, 60)
contract.place_prediction("0xYourAddress", "ETH", "DOWN", 100, 60)
contract.place_prediction("0xYourAddress", "SOL", "UP", 100, 60)
contract.place_prediction("0xYourAddress", "DOGE", "UP", 100, 60)
contract.place_prediction("0xYourAddress", "ADA", "DOWN", 100, 60)

# Check prices
contract.get_current_price("BTC")
contract.get_current_price("ETH")
contract.get_current_price("SOL")
contract.get_current_price("DOGE")
contract.get_current_price("ADA")

# Advance time and settle all
for i in range(10):
    contract.advance_time()

# Settle all predictions...
```

---

## 🧪 Test 10: Edge Cases

### A. Insufficient Balance
```python
contract.deposit("0xYourAddress", 50)
contract.place_prediction("0xYourAddress", "BTC", "UP", 100, 60)
# Expected: "ERROR: Insufficient balance. You have 50, need 100"
```

### B. Invalid Direction
```python
contract.deposit("0xYourAddress", 500)
contract.place_prediction("0xYourAddress", "BTC", "SIDEWAYS", 100, 60)
# Expected: "ERROR: Direction must be 'UP' or 'DOWN'"
```

### C. Wrong Owner Settlement
```python
# User1 places prediction
contract.deposit("0xUser1", 500)
contract.place_prediction("0xUser1", "BTC", "UP", 100, 60)

# User2 tries to settle User1's prediction
for i in range(10):
    contract.advance_time()

contract.settle_prediction("0xUser2", <prediction_id>)
# Expected: "ERROR: Not your prediction"
```

### D. Double Settlement
```python
contract.deposit("0xYourAddress", 500)
contract.place_prediction("0xYourAddress", "BTC", "UP", 100, 60)

for i in range(10):
    contract.advance_time()

contract.settle_prediction("0xYourAddress", <prediction_id>)
# First time: Success

contract.settle_prediction("0xYourAddress", <prediction_id>)
# Second time: "ERROR: Prediction already settled: WON (or LOST)"
```

---

## ✅ Expected Behavior Summary

| Action | When | Expected Result |
|--------|------|-----------------|
| Place prediction | Anytime with balance | Success, balance reduced |
| Settle early | Before duration expires | ERROR: Too early |
| Settle on time | After duration expires | Success: WON or LOST |
| Settle twice | After first settlement | ERROR: Already settled |
| Wrong owner settle | Anytime | ERROR: Not your prediction |
| Insufficient balance | Anytime | ERROR: Insufficient balance |
| Invalid direction | Anytime | ERROR: Direction must be UP or DOWN |

---

## 🎯 Success Criteria

✅ **Core Functionality:**
- [ ] Deposits work
- [ ] Balance tracking works
- [ ] Predictions are placed correctly
- [ ] Early settlement is blocked
- [ ] Time advancement works
- [ ] Settlements work after time expires
- [ ] Payouts are calculated correctly (1.8x)

✅ **Multi-User:**
- [ ] Multiple users can play simultaneously
- [ ] Each user has separate balance
- [ ] Leaderboard tracks winners
- [ ] Game stats show total players

✅ **Time-Based:**
- [ ] Transaction counter increments
- [ ] Duration is enforced
- [ ] `advance_time()` works
- [ ] Predictions become settleable after duration

✅ **Edge Cases:**
- [ ] All error messages work correctly
- [ ] Can't steal others' predictions
- [ ] Can't settle twice
- [ ] Balance checks work

---

## 📝 Report Your Results

After testing, please share:
1. ✅ Which tests passed
2. ❌ Which tests failed (if any)
3. 🐛 Any unexpected behavior
4. 💡 Suggestions for improvements

---

**Happy Testing! 🎮**
