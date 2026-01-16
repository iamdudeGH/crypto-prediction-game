# 🧪 Testing Your Fixed Crypto Prediction Game

## ✅ All Errors Fixed!

Your contracts are now ready to test with GenLayer. Both critical errors have been resolved:
1. ✅ `gl.msg.sender` error - Fixed
2. ✅ Float encoding error - Fixed

---

## 🚀 Quick Test (Recommended)

### Option 1: Test `crypto_prediction_simple.py` in GenLayer Studio

This is the **easiest way** to test your dApp!

#### Step 1: Deploy the Contract

1. Open [GenLayer Studio](https://studio.genlayer.com)
2. Copy the contents of `crypto_prediction_simple.py`
3. Paste into the editor
4. Click **"Deploy"**
5. Wait for deployment to complete

#### Step 2: Test the Contract

Try these commands in the GenLayer Studio console:

```python
# 1. Deposit some tokens to start playing
contract.deposit(1000)
# Expected: "Deposited 1000. New balance: 1000"

# 2. Check your balance
contract.get_balance()
# Expected: 1000

# 3. Get current Bitcoin price (test the API)
contract.get_current_price("BTC")
# Expected: {"symbol": "BTC", "price_usd_cents": 4512300, "success": True}
# Note: price_usd_cents means $45,123.00 (divide by 100)

# 4. Place a prediction
contract.place_prediction("BTC", "UP", 100, 60)
# Expected: "✅ Prediction #0 placed!\nUP on BTC @ $45123.00\nBet: 100 tokens | Duration: 60s"

# 5. Check your active prediction
contract.get_active_prediction()
# Expected: "🎯 Prediction #0\n⬆️ UP on BTC\nEntry: $45123.00\nBet: 100\nStatus: ACTIVE"

# 6. Wait 60+ seconds, then settle
contract.settle_prediction()
# Expected: "🎉 YOU WON!" or "😔 You Lost" with price details

# 7. Check your stats
contract.get_stats()
# Expected: "Balance: 1080 | Wins: 1 | Losses: 0 | Win Rate: 100.0%"

# 8. Reset and play again
contract.reset_prediction()
contract.place_prediction("ETH", "DOWN", 200, 30)
```

---

## 🎮 What to Test

### Basic Functionality:
- [x] Deposit tokens
- [x] Check balance
- [x] Fetch crypto prices (BTC, ETH, SOL, DOGE, ADA)
- [x] Place UP prediction
- [x] Place DOWN prediction
- [x] View active prediction
- [x] Settle after time expires
- [x] Check win/loss stats

### Edge Cases:
- [x] Try to predict with insufficient balance
- [x] Try to place prediction when one is active
- [x] Try to settle a non-existent prediction
- [x] Test with different cryptocurrencies
- [x] Test with different bet amounts

### Expected Behavior:

#### When Price Goes UP:
- UP prediction → WIN (1.8x payout)
- DOWN prediction → LOSE (no payout)

#### When Price Goes DOWN:
- DOWN prediction → WIN (1.8x payout)
- UP prediction → LOSE (no payout)

---

## 🧪 Advanced Test: Multi-User Contract

### Test `crypto_prediction_game.py`

This version supports multiple users but requires passing `user_address`.

```python
# Deploy crypto_prediction_game.py

# Simulate user1
user1 = "0x1111111111111111111111111111111111111111"

# 1. Deposit for user1
contract.deposit(user1, 1000)

# 2. Check user1's balance
contract.get_balance(user1)

# 3. Place prediction for user1
contract.place_prediction(user1, "BTC", "UP", 100, 60)

# 4. Check user1's predictions
contract.get_user_predictions(user1)

# 5. Get prediction details
contract.get_prediction_details(0)

# 6. After 60 seconds, settle
contract.settle_prediction(user1, 0)

# 7. Check leaderboard
contract.get_leaderboard()

# 8. Check game stats
contract.get_game_stats()
```

---

## 🔍 Verify the Fixes

### Test 1: Verify No `gl.msg.sender` Error
```python
# This should work without errors:
contract.deposit("0x123...", 1000)
# ✅ If it works, gl.msg.sender fix is successful
```

### Test 2: Verify No Float Encoding Error
```python
# This should return price_usd_cents (integer):
result = contract.get_current_price("BTC")
print(result)
# ✅ If you see price_usd_cents (not price_usd), float fix is successful
```

---

## 📊 Understanding the Output

### Price Format:
- **Old (broken):** `"price_usd": 45123.45` (float - caused errors)
- **New (fixed):** `"price_usd_cents": 4512345` (integer - works!)
- **To convert:** `price_usd_cents / 100 = $45,123.45`

### Example Output:

```python
# get_current_price("BTC")
{
  "symbol": "BTC",
  "price_usd_cents": 4512345,  # This is $45,123.45
  "timestamp": 1673456789,
  "success": True
}

# settle_prediction()
"🎉 YOU WON!
📈 BTC: $45123.45 → $45689.12 (+1.25%)
Your prediction: UP
Bet: 100 tokens
Payout: 180 tokens
New Balance: 1080"
```

---

## ❌ Troubleshooting

### If you see "not calldata encodable":
- ✅ Should be fixed! But if it appears, check that you're using the updated contract files.

### If you see "AttributeError: 'msg'":
- ✅ Should be fixed! Make sure you're passing `user_address` parameter.

### If price fetching fails:
- Wait a few seconds (API rate limit)
- Check internet connection
- Try a different crypto symbol

---

## 🎯 Success Criteria

Your contract is working correctly if:
- ✅ You can deposit tokens
- ✅ You can place predictions
- ✅ Prices are fetched successfully (as integers)
- ✅ You can settle predictions
- ✅ Payouts are calculated correctly (1.8x for wins)
- ✅ No encoding errors appear
- ✅ No msg.sender errors appear

---

## 🎉 Next Steps After Testing

Once everything works:
1. **Enhance the contract** - Add more features
2. **Connect the frontend** - Update `app_genlayer.js` with contract address
3. **Share your dApp** - Deploy to production
4. **Learn more** - Try the Wizard of Coin pattern for AI features

---

## 💡 Pro Tips

1. **Start with simple contract** - Test `crypto_prediction_simple.py` first
2. **Test with small amounts** - Use 10-100 tokens for testing
3. **Wait for settlement** - Ensure 60+ seconds pass before settling
4. **Check logs** - Look at console output for debugging
5. **Try different cryptos** - BTC is stable, DOGE is volatile

Happy testing! 🚀
