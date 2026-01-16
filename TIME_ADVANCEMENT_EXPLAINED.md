# ⏰ Time Advancement Explained

## The Problem: No Real Time in Smart Contracts

GenLayer smart contracts **don't have access to real timestamps**. They can't check "has 60 seconds passed?"

So how do we make predictions that expire after a certain time? 🤔

---

## The Solution: Transaction Counter

Instead of real time, we use a **transaction counter** that acts as a "virtual clock":

- Each time someone makes a **write transaction** (deposit, place_prediction, settle, advance_time), the counter increases by 1
- We treat **1 transaction = ~10 seconds** of virtual time
- Predictions store when they were created and how many transactions must pass before settling

---

## Visual Example

### Scenario: You place a 60-second prediction

```
Duration: 60 seconds = 6 transactions (60 ÷ 10 = 6)

Timeline:
TX #1  ────  You deposit 1000 tokens
TX #2  ────  You place prediction (creation_tx = 2, duration_tx = 6)
TX #3  ────  [waiting...] ❌ Can't settle yet (only 1 tx passed, need 6)
TX #4  ────  [waiting...] ❌ Can't settle yet (only 2 tx passed, need 6)
TX #5  ────  [waiting...] ❌ Can't settle yet (only 3 tx passed, need 6)
TX #6  ────  [waiting...] ❌ Can't settle yet (only 4 tx passed, need 6)
TX #7  ────  [waiting...] ❌ Can't settle yet (only 5 tx passed, need 6)
TX #8  ────  ✅ You can settle now! (6 tx passed, reached duration)
```

**The Math:**
- Creation TX: 2
- Duration: 6 transactions
- Current TX: 8
- TX Passed: 8 - 2 = 6 ✅ (>= 6, so ready!)

---

## How `advance_time()` Works

`advance_time()` is a **utility function** that simply increments the transaction counter by 1.

### Why do we need it?

Without it, the only way to advance the counter is to make "real" transactions (deposit, place_prediction, etc.). But if you're testing alone, you'd need to do useless transactions just to make time pass!

### Example Without `advance_time()`:

```python
# Place prediction (TX #2)
contract.place_prediction("0xAddr", "BTC", "UP", 100, 60)

# Need 6 more transactions... but you don't want to make 6 more predictions!
# So you'd have to do silly stuff like:
contract.deposit("0xAddr", 1)  # TX #3
contract.deposit("0xAddr", 1)  # TX #4
contract.deposit("0xAddr", 1)  # TX #5
contract.deposit("0xAddr", 1)  # TX #6
contract.deposit("0xAddr", 1)  # TX #7
contract.deposit("0xAddr", 1)  # TX #8

# Finally settle
contract.settle_prediction("0xAddr", 0)
```

### Example With `advance_time()`:

```python
# Place prediction (TX #2)
contract.place_prediction("0xAddr", "BTC", "UP", 100, 60)

# Just advance time 6 times
contract.advance_time()  # TX #3
contract.advance_time()  # TX #4
contract.advance_time()  # TX #5
contract.advance_time()  # TX #6
contract.advance_time()  # TX #7
contract.advance_time()  # TX #8

# Settle
contract.settle_prediction("0xAddr", 0)
```

Much cleaner! 🎯

---

## Real-World Scenario (Multi-User)

In a real game with multiple users, transactions happen naturally:

```
TX #1  ─ Alice deposits 1000
TX #2  ─ Alice places prediction (UP on BTC, 60s)
TX #3  ─ Bob deposits 1000
TX #4  ─ Bob places prediction (DOWN on ETH, 60s)
TX #5  ─ Charlie deposits 500
TX #6  ─ Charlie places prediction (UP on SOL, 30s)
TX #7  ─ Dave deposits 2000
TX #8  ─ Alice settles her prediction ✅ (6 tx passed since TX #2)
TX #9  ─ Dave places prediction (DOWN on BTC, 120s)
TX #10 ─ Charlie settles his prediction ✅ (4 tx passed since TX #6)
TX #11 ─ Bob settles his prediction ✅ (7 tx passed since TX #4)
```

**Key insight:** With multiple users, you don't need `advance_time()` because other people's transactions naturally advance the counter!

---

## Code Walkthrough

### When You Place a Prediction:

```python
def place_prediction(self, user_address, crypto_symbol, direction, bet_amount, duration_seconds=60):
    self.transaction_counter += 1  # Increment counter
    self.price_counter += 1
    
    # Convert seconds to transactions (1 tx = 10 seconds)
    duration_tx = max(1, duration_seconds // 10)
    # 60 seconds → 6 transactions
    # 30 seconds → 3 transactions
    # 120 seconds → 12 transactions
    
    # Store when prediction was created
    self.prediction_creation_tx[prediction_id] = self.transaction_counter
    self.prediction_duration_tx[prediction_id] = duration_tx
```

### When You Try to Settle:

```python
def settle_prediction(self, user_address, prediction_id):
    self.transaction_counter += 1  # Increment counter
    
    # Check if enough transactions have passed
    creation_tx = self.prediction_creation_tx[prediction_id]
    duration_tx = self.prediction_duration_tx[prediction_id]
    tx_passed = self.transaction_counter - creation_tx
    
    if tx_passed < duration_tx:
        tx_remaining = duration_tx - tx_passed
        return f"ERROR: Too early. Need {tx_remaining} more transactions"
    
    # Enough time passed, proceed with settlement...
```

### The `advance_time()` Function:

```python
def advance_time(self):
    self.transaction_counter += 1  # That's it! Just increment the counter
    return f"Time advanced! Current TX: {self.transaction_counter}"
```

---

## Practical Examples

### Example 1: Quick 30-second Prediction

```python
# TX #1: Deposit
contract.deposit("0xAddr", 1000)
# Counter: 1

# TX #2: Place prediction (30s = 3 tx)
contract.place_prediction("0xAddr", "BTC", "UP", 100, 30)
# Counter: 2, Creation: 2, Duration: 3

# TX #3: Advance time
contract.advance_time()
# Counter: 3, TX passed: 3-2=1, Need: 3 ❌

# TX #4: Advance time
contract.advance_time()
# Counter: 4, TX passed: 4-2=2, Need: 3 ❌

# TX #5: Advance time
contract.advance_time()
# Counter: 5, TX passed: 5-2=3, Need: 3 ✅

# TX #6: Settle (works!)
contract.settle_prediction("0xAddr", 0)
# Counter: 6, TX passed: 6-2=4, Need: 3 ✅
```

### Example 2: Multiple Predictions with Different Durations

```python
# TX #1: Deposit
contract.deposit("0xAddr", 2000)

# TX #2: Place 30s prediction
contract.place_prediction("0xAddr", "BTC", "UP", 100, 30)  # Needs 3 tx

# TX #3: Place 60s prediction
contract.place_prediction("0xAddr", "ETH", "DOWN", 200, 60)  # Needs 6 tx

# TX #4: Place 120s prediction
contract.place_prediction("0xAddr", "SOL", "UP", 150, 120)  # Needs 12 tx

# TX #5: Advance
contract.advance_time()

# TX #6: Settle first prediction (30s)
contract.settle_prediction("0xAddr", 0)  # ✅ Works! (4 tx passed, needs 3)

# TX #7-10: Advance more
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()

# TX #11: Settle second prediction (60s)
contract.settle_prediction("0xAddr", 1)  # ✅ Works! (8 tx passed, needs 6)

# TX #12-15: Advance more
contract.advance_time()
contract.advance_time()
contract.advance_time()
contract.advance_time()

# TX #16: Settle third prediction (120s)
contract.settle_prediction("0xAddr", 2)  # ✅ Works! (13 tx passed, needs 12)
```

---

## Why This Design?

### ✅ Advantages:
1. **No timestamp dependency** - Works on any blockchain
2. **Deterministic** - All validators agree on transaction count
3. **Simple** - Easy to understand and debug
4. **Flexible** - Can simulate different time scales
5. **Multi-user compatible** - Everyone's transactions advance time for everyone

### ❌ Limitations:
1. **Not real time** - 1 tx doesn't always = 10 real seconds
2. **Needs activity** - In a dead game with no users, time doesn't advance
3. **Testing overhead** - Need to call `advance_time()` multiple times when testing alone

---

## Common Questions

### Q: Why not use real timestamps?

**A:** GenLayer contracts don't have access to `block.timestamp` or real time. Even if they did, it wouldn't be reliable for consensus.

### Q: What if I'm the only user playing?

**A:** Use `advance_time()` to simulate time passing. In production with multiple users, their transactions naturally advance time.

### Q: Can I change the time conversion (1 tx = 10s)?

**A:** Yes! Just modify this line in `place_prediction()`:
```python
duration_tx = max(1, duration_seconds // 10)  # Change 10 to whatever you want
```

### Q: What happens if I try to settle too early?

**A:** You get an error message telling you how many more transactions you need:
```
"ERROR: Too early. Need 3 more transactions"
```

### Q: Do all write functions advance time?

**A:** Yes! Every function marked `@gl.public.write` increments the counter:
- `deposit()` ✅
- `place_prediction()` ✅
- `settle_prediction()` ✅
- `advance_time()` ✅

But read-only functions (`@gl.public.view`) don't:
- `get_balance()` ❌
- `get_prediction_details()` ❌
- `get_current_price()` ❌

---

## Summary

**The transaction counter is a virtual clock:**
- 📊 Each write transaction = +1 to counter
- ⏰ 1 transaction ≈ 10 seconds of virtual time
- 🎯 Predictions require X transactions to pass before settling
- 🔧 `advance_time()` is a utility to simulate time when testing alone
- 👥 With multiple users, time advances naturally from their activity

**Think of it like a video game:**
- Transaction counter = Game tick
- Real users = NPCs performing actions
- advance_time() = Fast-forward button for testing

---

Hope this helps! Let me know if you have any questions! 🚀
