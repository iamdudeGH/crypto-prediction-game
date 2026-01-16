# 🚀 Quick Test Guide - Crypto Prediction dApp

## ✅ Contract Fixed!

The contract now uses **only basic GenLayer types**:
- No custom classes
- Simple dict[key, value] structures
- All methods return strings or basic types

## 📝 Step-by-Step Testing in GenLayer Studio

### 1. Deploy the Contract

1. Go to https://studio.genlayer.com
2. Copy the entire `crypto_prediction_game.py` file
3. Paste into GenLayer Studio
4. Click **Deploy**
5. Wait for "FINALIZED" status

### 2. Test Each Method (In Order)

#### ✅ Step 1: Deposit Tokens
```
Method: deposit
Parameters:
  amount: 1000

Expected Output: "Deposited 1000. New balance: 1000"
```

#### ✅ Step 2: Check Your Balance
```
Method: get_balance
Parameters: (leave empty or enter your address)

Expected Output: 1000
```

#### ✅ Step 3: Get Current Bitcoin Price
```
Method: get_current_price
Parameters:
  crypto_symbol: BTC

Expected Output: {"symbol": "BTC", "price_usd": 45000.00, "timestamp": ...}
```

#### ✅ Step 4: Place a Prediction
```
Method: place_prediction
Parameters:
  crypto_symbol: BTC
  direction: UP
  bet_amount: 100
  duration_seconds: 60

Expected Output: "Prediction #0 placed: UP on BTC at $45123.45 for 60s"
```

#### ✅ Step 5: Get Prediction Details
```
Method: get_prediction_details
Parameters:
  prediction_id: 0

Expected Output: "Prediction #0: UP on BTC | Bet: 100 | Entry: $45123.45 | Status: ACTIVE | Time left: 45s | Owner: 0x1234567..."
```

#### ✅ Step 6: Check Your Predictions
```
Method: get_user_predictions
Parameters: (leave empty)

Expected Output: "Total: 1 predictions (Active: 1, Won: 0, Lost: 0)"
```

#### ⏰ Step 7: Wait 60 Seconds
- Wait for the full duration to complete
- You can check `get_prediction_details` to see time left

#### ✅ Step 8: Settle the Prediction
```
Method: settle_prediction
Parameters:
  prediction_id: 0

Expected Output: 
- If you won: "Settled: WON - Entry: $45123.45, Exit: $45500.00, Payout: 180"
- If you lost: "Settled: LOST - Entry: $45123.45, Exit: $44900.00, Payout: 0"
```

#### ✅ Step 9: Check Balance Again
```
Method: get_balance
Parameters: (leave empty)

Expected Output: 
- If won: 1080 (1000 - 100 bet + 180 payout)
- If lost: 900 (1000 - 100 bet)
```

#### ✅ Step 10: View Leaderboard
```
Method: get_leaderboard
Parameters: (leave empty)

Expected Output: 
- If you won: "Leaderboard:\n1. 0x1234567... - 1 wins\n"
- If you lost: "No winners yet"
```

#### ✅ Step 11: Get Game Stats
```
Method: get_game_stats
Parameters: (leave empty)

Expected Output: "Total predictions: 1, Total players: 1, Total in pool: 900"
```

## 🎮 Try Different Scenarios

### Test Scenario 1: Multiple Predictions
1. Deposit 2000 tokens
2. Place 3 predictions on different cryptos:
   - BTC UP for 30s
   - ETH DOWN for 60s
   - SOL UP for 120s
3. Check `get_user_predictions` to see all 3
4. Settle them one by one after each expires

### Test Scenario 2: Different Cryptocurrencies
Try all supported cryptos:
- `BTC` - Bitcoin
- `ETH` - Ethereum
- `SOL` - Solana
- `DOGE` - Dogecoin
- `ADA` - Cardano

### Test Scenario 3: Error Handling
Try these to see error messages:
1. Place bet without depositing: "ERROR: Insufficient balance"
2. Settle prediction too early: "ERROR: Prediction not yet expired"
3. Settle same prediction twice: "ERROR: Prediction already settled"

## 📊 Understanding the Output

### Prediction Status Values
- **ACTIVE** - Prediction is ongoing, waiting for time to expire
- **WON** - You predicted correctly and got 1.8x payout
- **LOST** - You predicted incorrectly and lost your bet

### Payout Calculation
- **Win**: Bet × 1.8 (e.g., bet 100, win 180)
- **Loss**: Lose your bet amount (e.g., bet 100, lose 100)

### Price Movement
- **UP**: Exit price > Entry price
- **DOWN**: Exit price < Entry price

## 🐛 Common Issues & Solutions

### Issue: "Failed to fetch current price"
**Solution**: 
- CoinGecko API might be rate-limited
- Wait 1 minute and try again
- Try a different crypto symbol

### Issue: "Insufficient balance"
**Solution**: 
- Call `deposit(amount)` first
- Check balance with `get_balance()`

### Issue: "Prediction not yet expired"
**Solution**: 
- Check time left with `get_prediction_details(prediction_id)`
- Wait for the full duration
- Try shorter durations for testing (30-60 seconds)

### Issue: "Not your prediction"
**Solution**: 
- You can only settle your own predictions
- Make sure you're using the correct prediction_id

## 🎯 Success Indicators

Your contract is working correctly if:
- ✅ You can deposit tokens
- ✅ Balance updates correctly
- ✅ Predictions are created with unique IDs
- ✅ Price data is fetched successfully
- ✅ Predictions settle after time expires
- ✅ Balance increases when you win
- ✅ Leaderboard updates after wins

## 📈 Next Steps After Testing

1. **Increase bet sizes** - Try larger amounts
2. **Longer durations** - Test 5-10 minute predictions
3. **Track win rate** - See which cryptos you predict best
4. **Share with friends** - Give them the contract address
5. **Build frontend** - Connect the HTML/CSS/JS interface

## 💡 Pro Tips

1. **Start with small bets** (100 tokens) to learn the system
2. **Use short durations** (30-60s) for quick testing
3. **Check price before betting** - Use `get_current_price()` to see current value
4. **Track your predictions** - Use `get_prediction_details()` to monitor status
5. **Watch the clock** - Set a timer so you know when to settle

---

**Happy Testing! 🎉**

If everything works, you've successfully deployed a Web3 prediction market on GenLayer!
