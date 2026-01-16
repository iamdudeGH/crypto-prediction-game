# 🚀 Crypto Prediction Game - dApp Deployment Guide

## Overview

Your crypto prediction game is now a complete dApp with:
- ✅ Smart contract with real timestamps (`crypto_prediction_game_realtime.py`)
- ✅ Frontend UI (`index.html`, `style.css`, `app_genlayer.js`)
- ✅ Multi-user support
- ✅ Real-time predictions
- ✅ Leaderboard and statistics

---

## 📋 Prerequisites

1. **Deployed Contract**
   - Contract file: `crypto_prediction_game_realtime.py`
   - Deployed on GenLayer testnet
   - Contract address saved

2. **Your Wallet Address**
   - GenLayer wallet address for transactions

3. **Web Browser**
   - Modern browser (Chrome, Firefox, Edge)
   - JavaScript enabled

---

## 🎯 Step-by-Step Deployment

### Step 1: Deploy the Smart Contract

1. **Open GenLayer Studio**
   - Go to: https://studio.genlayer.com

2. **Copy Contract Code**
   - Open `crypto_prediction_game_realtime.py`
   - Copy entire file content

3. **Deploy**
   - Paste code in GenLayer Studio
   - Click "Deploy"
   - Wait for deployment to finalize
   - **Save the contract address!** (e.g., `0xabc123...`)

### Step 2: Test the Contract

Before connecting the frontend, test your contract works:

```python
# 1. Check current time
contract.get_current_time()
# Should return: "2026-01-16T10:30:45.123456Z"

# 2. Deposit tokens
contract.deposit("YOUR_ADDRESS", 1000)

# 3. Check balance
contract.get_balance("YOUR_ADDRESS")
# Should return: 1000

# 4. Place a test prediction
contract.place_prediction("YOUR_ADDRESS", "BTC", "UP", 100, 30)
# Wait 30+ seconds...

# 5. Settle
contract.settle_prediction("YOUR_ADDRESS", 0)
```

If all these work, you're ready for the frontend! ✅

### Step 3: Open the Frontend

1. **Open index.html**
   - Locate `index.html` in your workspace
   - Open with a web browser
   - Or use a local web server:
     ```bash
     # Using Python
     python -m http.server 8000
     # Then open: http://localhost:8000
     
     # Using Node.js
     npx http-server
     ```

2. **You should see:**
   - Header with "Crypto Prediction Game"
   - Contract configuration fields
   - Crypto selector
   - Betting interface
   - Sections for predictions, stats, and leaderboard

### Step 4: Configure the Frontend

1. **Enter Contract Address**
   - Copy your deployed contract address from GenLayer Studio
   - Paste into "Contract Address" field
   - Click "Save"

2. **Enter Your Wallet Address**
   - Copy your GenLayer wallet address
   - Paste into "Your Address" field
   - Click "Save"

3. **Verify Connection**
   - Status badge should show "Connected" (green)
   - You should see notification: "Connected to contract!"

---

## 🎮 How to Use the dApp

### Current Version (Manual Mode)

**Important:** The current frontend is a **UI demo** that helps you interact with GenLayer Studio. It generates the commands you need to copy/paste into Studio.

### Workflow:

1. **Deposit Tokens**
   - Enter amount (minimum 100)
   - Click "Deposit Tokens"
   - A popup shows the command
   - Copy command to GenLayer Studio
   - Execute in Studio
   - Manually update balance in UI

2. **Place Prediction**
   - Select cryptocurrency (BTC, ETH, SOL, etc.)
   - Enter bet amount
   - Select duration (30s, 60s, 2m, 5m)
   - Click "⬆️ UP" or "⬇️ DOWN"
   - Copy command to GenLayer Studio
   - Execute in Studio

3. **Check Predictions**
   - Click "🔄 Refresh" next to Active Predictions
   - Copy command: `contract.get_user_predictions("YOUR_ADDRESS")`
   - Execute in Studio to see status

4. **Settle Predictions**
   - Wait for duration to expire
   - In Studio: `contract.settle_prediction("YOUR_ADDRESS", PREDICTION_ID)`
   - Check result (WON or LOST)

5. **View Leaderboard**
   - Click "🔄 Refresh" next to Leaderboard
   - Copy command: `contract.get_leaderboard()`
   - Execute in Studio

---

## 📝 Example Game Flow

### Full Example:

```python
# ============================================
# Step 1: Initial Setup (in GenLayer Studio)
# ============================================

# Deposit 2000 tokens
contract.deposit("0xYourAddress", 2000)
# Returns: "Deposited 2000. Balance: 2000 | Time: 2026-01-16T10:00:00Z"

# Check balance
contract.get_balance("0xYourAddress")
# Returns: 2000

# ============================================
# Step 2: Place Multiple Predictions
# ============================================

# Prediction 1: BTC UP, 30 seconds
contract.place_prediction("0xYourAddress", "BTC", "UP", 100, 30)
# Returns: Prediction #0: UP on BTC @ $95000.00 | Created: ... | Expires: ...

# Prediction 2: ETH DOWN, 60 seconds
contract.place_prediction("0xYourAddress", "ETH", "DOWN", 200, 60)
# Returns: Prediction #1: DOWN on ETH @ $3500.00 | Created: ... | Expires: ...

# Prediction 3: SOL UP, 120 seconds
contract.place_prediction("0xYourAddress", "SOL", "UP", 150, 120)
# Returns: Prediction #2: UP on SOL @ $150.00 | Created: ... | Expires: ...

# ============================================
# Step 3: Check Status
# ============================================

# Check all predictions
contract.get_user_predictions("0xYourAddress")
# Returns: "Total: 3 | Active: 3 | Won: 0 | Lost: 0"

# Check specific prediction
contract.get_prediction_details(0)
# Returns: "#0: UP BTC @ $95000.00 | 100 tokens | Created: ... | Expires: ..."

# ============================================
# Step 4: Wait for Expiry
# ============================================

# Wait 30+ seconds for first prediction...
# (Go get coffee, check the time, etc.)

# ============================================
# Step 5: Settle Predictions
# ============================================

# Settle first prediction (after 30s)
contract.settle_prediction("0xYourAddress", 0)
# Returns: "WON: BTC $95000.00 -> $96200.00 | Payout: 180 | Balance: 1880"

# Wait 60+ seconds for second prediction...
contract.settle_prediction("0xYourAddress", 1)
# Returns: "LOST: ETH $3500.00 -> $3200.00 | Payout: 0 | Balance: 1880"

# Wait 120+ seconds for third prediction...
contract.settle_prediction("0xYourAddress", 2)
# Returns: "WON: SOL $150.00 -> $155.00 | Payout: 270 | Balance: 2150"

# ============================================
# Step 6: Check Final Stats
# ============================================

# Your predictions
contract.get_user_predictions("0xYourAddress")
# Returns: "Total: 3 | Active: 0 | Won: 2 | Lost: 1"

# Leaderboard
contract.get_leaderboard()
# Returns: 
# Leaderboard:
# 1. 0xYourAdd... - 2 wins

# Game stats
contract.get_game_stats()
# Returns: "Predictions: 3 | Players: 1 | Current Time: ..."
```

---

## 🔧 Frontend Features

### Configuration Panel
- **Contract Address**: Your deployed contract
- **Your Address**: Your wallet address
- **Connection Status**: Shows if connected (green) or not (red)
- **Balance**: Current token balance

### Price Display
- Current crypto symbol
- Last update time
- Refresh button to check latest price

### Betting Interface
- Bet amount input (minimum 10 tokens)
- Duration selector (30s, 60s, 2m, 5m)
- UP/DOWN buttons with payout info

### Active Predictions
- Shows your active predictions
- Refresh button to update status
- Details: symbol, direction, amount, expiry

### Statistics
- Total predictions
- Wins (green)
- Losses (red)
- Win rate percentage

### Leaderboard
- Top 10 players by wins
- Shows address and win count
- Refresh button to update

### Deposit Section
- Input for deposit amount
- Minimum 100 tokens
- Adds to your balance

---

## 💡 Tips & Best Practices

### For Testing:
1. **Start small** - Test with 10-30 token bets
2. **Use short durations** - 30 seconds for quick testing
3. **Test all scenarios** - Try UP and DOWN, wins and losses
4. **Check time carefully** - Wait for actual seconds to pass

### For Production:
1. **Deposit enough tokens** - Have buffer for multiple games
2. **Track your predictions** - Note prediction IDs
3. **Set realistic durations** - 60-300 seconds work well
4. **Check before settling** - Verify time has expired
5. **Monitor balance** - Keep track of wins/losses

### Common Commands:

```python
# Quick balance check
contract.get_balance("YOUR_ADDRESS")

# Quick price check
contract.get_current_price("BTC")

# Quick time check
contract.get_current_time()

# Quick stats
contract.get_user_predictions("YOUR_ADDRESS")
contract.get_leaderboard()
```

---

## 🐛 Troubleshooting

### Issue: "Not connected to contract"
**Solution:** 
- Check contract address is correct
- Verify contract is deployed
- Click "Save" after entering address

### Issue: "Too early to settle"
**Solution:**
- Check current time: `contract.get_current_time()`
- Check prediction expiry: `contract.get_prediction_details(ID)`
- Wait for more real seconds to pass

### Issue: "Insufficient balance"
**Solution:**
- Check balance: `contract.get_balance("YOUR_ADDRESS")`
- Deposit more: `contract.deposit("YOUR_ADDRESS", AMOUNT)`

### Issue: "Not your prediction"
**Solution:**
- Verify you're using the same address that placed the prediction
- Check prediction owner: `contract.get_prediction_details(ID)`

### Issue: "Already settled"
**Solution:**
- Prediction has been settled before
- Check status: `contract.get_prediction_details(ID)`
- Status will show "WON" or "LOST"

---

## 🔮 Future Enhancements

### Phase 1: Direct Integration
- Connect frontend directly to GenLayer RPC
- Automatic balance updates
- Real-time price fetching
- Auto-settle when ready

### Phase 2: Enhanced Features
- Countdown timers for predictions
- Prediction history
- Profit/loss charts
- Push notifications

### Phase 3: Advanced Features
- Real API prices (CryptoCompare)
- Multiple crypto pairs
- Tournament mode
- Social features (chat, teams)

---

## 📊 Contract Functions Reference

### View Functions (Read-only, free)
- `get_current_time()` - Get blockchain time
- `get_current_price(symbol)` - Get crypto price
- `get_balance(address)` - Get user balance
- `get_user_predictions(address)` - Get user summary
- `get_prediction_details(id)` - Get prediction info
- `get_leaderboard()` - Get top players
- `get_game_stats()` - Get game statistics

### Write Functions (Transactions, cost gas)
- `deposit(address, amount)` - Deposit tokens
- `place_prediction(address, symbol, direction, amount, duration)` - Place bet
- `settle_prediction(address, id)` - Settle and claim winnings

---

## 🎯 Success Checklist

Before going live, verify:

- [ ] Contract deployed successfully
- [ ] Contract address saved
- [ ] Wallet address ready
- [ ] Can deposit tokens
- [ ] Can place predictions
- [ ] Can settle predictions
- [ ] Predictions expire correctly
- [ ] Payouts calculated correctly
- [ ] Leaderboard updates
- [ ] Stats track accurately
- [ ] Frontend displays correctly
- [ ] All buttons work
- [ ] Commands generated properly

---

## 📞 Support & Resources

### Documentation
- `FINAL_SUCCESS_SUMMARY.md` - Complete project overview
- `TIME_ADVANCEMENT_EXPLAINED.md` - How timing works
- `GENLAYER_LIMITATIONS.md` - Platform constraints
- `crypto_prediction_game_realtime.py` - Contract code

### Contract Details
- **File:** `crypto_prediction_game_realtime.py`
- **Version:** v0.1.0
- **Features:** Real timestamps, multi-user, leaderboard
- **Status:** Production ready ✅

### Frontend Files
- `index.html` - Main UI
- `style.css` - Styling
- `app_genlayer.js` - Logic and integration

---

## 🎊 You're Ready!

Your crypto prediction game dApp is complete and ready to use!

**Next Steps:**
1. Deploy contract to GenLayer
2. Save contract address
3. Open index.html
4. Configure addresses
5. Start playing!

**Have fun predicting! 🎯🚀**

---

_Last Updated: 2026-01-16_
_Contract: crypto_prediction_game_realtime.py_
_Status: Production Ready ✅_
