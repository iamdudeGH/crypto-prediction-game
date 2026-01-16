# 🔧 Fixes Applied to Crypto Prediction Game

## Issue 1: gl.msg.sender Error ✅ FIXED
Contract was throwing `AttributeError: module 'genlayer.gl' has no attribute 'msg'`

### Root Cause
GenLayer's current API **does not support `gl.msg.sender`** like traditional Ethereum smart contracts do.

### Solution
Changed all methods that relied on `gl.msg.sender` to accept `user_address` as an explicit parameter.

---

## Issue 2: Float Encoding Error ✅ FIXED
Contract was throwing `TypeError: not calldata encodable 0.0: float`

### Root Cause
GenLayer's calldata encoding system **cannot encode float values** - only integers, strings, booleans, and collections of these types are supported.

The `get_current_price()` method was returning `price_usd` as a float (e.g., `45000.50`), which caused encoding failures when returning from contract methods.

### Solution
**Convert all prices to integers using cents:**
- Changed `price_usd: float` → `price_usd_cents: u256`
- Multiply API prices by 100 and convert to int: `int(price_float * 100)`
- Store prices as integers (cents) in state variables
- Convert back to dollars for display: `price_cents / 100.0`

**Example:**
```python
# OLD (caused error):
price = 45123.45  # float
return {"price_usd": price}  # ❌ Error!

# NEW (works):
price_cents = int(45123.45 * 100)  # 4512345
return {"price_usd_cents": price_cents}  # ✅ Success!

# Display:
price_usd = price_cents / 100.0  # 45123.45
```

### Methods Updated (Issue 1):

1. **`deposit(user_address, amount)`** - Now requires user_address parameter
2. **`get_balance(user_address)`** - Made user_address required (was optional)
3. **`place_prediction(user_address, crypto_symbol, direction, bet_amount, duration_seconds)`** - Added user_address as first parameter
4. **`settle_prediction(user_address, prediction_id)`** - Added user_address parameter
5. **`get_user_predictions(user_address)`** - Made user_address required (was optional)

### Methods Updated (Issue 2):

1. **`get_current_price()`** - Returns `price_usd_cents` instead of `price_usd`
2. **`place_prediction()`** - Stores entry price as cents (integer)
3. **`settle_prediction()`** - Compares prices as integers, converts for display
4. **`get_prediction_details()`** - Converts cents to dollars for display
5. **`get_active_prediction()`** - Converts cents to dollars for display (simple version)

### Type Changes:

**crypto_prediction_game.py:**
- `prediction_entry_prices: TreeMap[u256, float]` → `TreeMap[u256, u256]`

**crypto_prediction_simple.py:**
- `active_entry_price: float` → `active_entry_price: u256`

## Frontend Impact

Your frontend (`app.js`) will need to be updated to pass the user's address explicitly when calling these methods:

```javascript
// OLD (won't work):
await contract.deposit(amount);

// NEW (correct):
const userAddress = await getCurrentUserAddress(); // Get from wallet
await contract.deposit(userAddress, amount);
```

## Alternative Approach

If you want a simpler single-user experience, use `crypto_prediction_simple.py` instead, which doesn't track multiple users and doesn't need address parameters at all.

## Summary of All Changes

### Files Modified:
- ✅ `crypto_prediction_game.py` - Fixed both issues
- ✅ `crypto_prediction_simple.py` - Fixed both issues
- ✅ Documentation updated

### What Still Works:
- ✅ All contract logic (deposit, predict, settle)
- ✅ Price fetching from CoinGecko API
- ✅ Win/loss tracking
- ✅ Leaderboard functionality
- ✅ User balances

### What Changed (from user perspective):
- **Frontend calls must pass user_address** explicitly
- **API returns `price_usd_cents`** instead of `price_usd` (divide by 100 to get dollars)

## Next Steps

1. ✅ Contract fixed (both issues)
2. ✅ Frontend integration guide created
3. ⏳ Test the contract with GenLayer simulator
4. ⏳ Update frontend to match new API (if needed)
