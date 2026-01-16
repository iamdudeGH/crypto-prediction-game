# 🎯 Crypto Prediction Game - GenLayer dApp

A decentralized prediction game where users bet on cryptocurrency price movements within time-limited rounds.

## 🌟 Features

### Smart Contract (GenLayer)
- ✅ **Real-time price fetching** - Uses CoinGecko API to fetch live crypto prices
- ✅ **Multiple cryptocurrencies** - BTC, ETH, SOL, DOGE, ADA supported
- ✅ **Time-based predictions** - 30s, 60s, 2min, 5min rounds
- ✅ **Automatic settlement** - Smart contract determines winners
- ✅ **Balance management** - Deposit, withdraw, and track balances
- ✅ **Leaderboard** - Track top predictors
- ✅ **1.8x payout** - Winners get 1.8x their bet amount

### Frontend (HTML/CSS/JS)
- ✅ **Clean, modern UI** - Beautiful gradient design
- ✅ **Real-time price updates** - Auto-refresh every 5 seconds
- ✅ **Active predictions display** - Track your bets in real-time
- ✅ **Countdown timers** - See time remaining on predictions
- ✅ **Toast notifications** - Get instant feedback
- ✅ **Responsive design** - Works on mobile and desktop

## 📁 Project Structure

```
├── crypto_prediction_game.py   # Smart contract (GenLayer)
├── index.html                   # Frontend HTML
├── style.css                    # Styling
├── app.js                       # Frontend logic
├── my_first_contract.py         # Your first Hello contract
└── README.md                    # Main project readme
```

## 🚀 How to Deploy & Run

### Step 1: Deploy the Smart Contract

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Create a new file and paste `crypto_prediction_game.py`
3. Click **"Deploy"**
4. Copy the contract address (e.g., `0x1234...abcd`)

### Step 2: Connect Frontend to Contract

1. Open `app.js`
2. Find line 4: `contractAddress: null`
3. Replace with your deployed contract address:
   ```javascript
   contractAddress: '0x1234...abcd' // Your contract address
   ```

### Step 3: Run the Frontend

**Option A: Simple HTTP Server (Python)**
```bash
# In your project directory
python -m http.server 8000

# Open browser to http://localhost:8000
```

**Option B: Live Server (VS Code)**
1. Install "Live Server" extension
2. Right-click `index.html`
3. Select "Open with Live Server"

**Option C: Just open the file**
- Double-click `index.html` (works but with limited functionality)

## 🎮 How to Play

### 1. Deposit Tokens
- Enter amount (e.g., 1000)
- Click "Deposit Tokens"
- Your balance will update

### 2. Select Cryptocurrency
- Choose from dropdown: BTC, ETH, SOL, DOGE, or ADA
- Price will update automatically

### 3. Place a Prediction
- Enter bet amount (minimum 10 tokens)
- Select duration (30s, 60s, 2min, or 5min)
- Click **⬆️ UP** if you think price will go up
- Click **⬇️ DOWN** if you think price will go down

### 4. Wait for Settlement
- Watch the countdown timer
- After time expires, click "Settle Now"
- Or wait for auto-settlement

### 5. Collect Winnings
- **Win**: Get 1.8x your bet (e.g., bet 100, win 180)
- **Lose**: Lose your bet amount
- Balance updates automatically

## 🔧 Smart Contract Methods

### Read Methods (View - No gas cost)
- `get_current_price(crypto_symbol)` - Fetch live price
- `get_balance(user_address)` - Check user balance
- `get_user_predictions(user_address)` - View all predictions
- `get_leaderboard()` - See top players
- `get_game_stats()` - Overall game statistics

### Write Methods (Requires transaction)
- `deposit(amount)` - Add funds to play
- `place_prediction(symbol, direction, bet_amount, duration)` - Place bet
- `settle_prediction(prediction_id)` - Settle completed prediction

## 📊 Example Workflow

```javascript
// 1. Deploy contract
const game = new CryptoPredictionGame()

// 2. Deposit funds
game.deposit(1000)  // Deposit 1000 tokens

// 3. Check current price
const price = game.get_current_price("BTC")
// Returns: {"symbol": "BTC", "price_usd": 45000.00, "timestamp": 1234567890}

// 4. Place prediction
const prediction = game.place_prediction(
    "BTC",    // cryptocurrency
    "UP",     // direction
    100,      // bet amount
    60        // 60 seconds
)

// 5. Wait 60 seconds...

// 6. Settle prediction
const result = game.settle_prediction(prediction.id)
// Returns: {"result": "WON", "payout": 180, ...}
```

## 🎨 Customization

### Change Payout Multiplier
In `crypto_prediction_game.py`, line 139:
```python
payout = int(prediction["bet_amount"] * 1.8)  # Change 1.8 to any multiplier
```

### Add More Cryptocurrencies
In `crypto_prediction_game.py`, lines 23-29:
```python
symbol_map = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    # Add more here...
    "XRP": "ripple",
}
```

### Change Update Interval
In `app.js`, line 4:
```javascript
updateInterval: 5000,  // Change to any milliseconds (5000 = 5 seconds)
```

## ⚠️ Important Notes

### Demo Mode
The frontend currently runs in **DEMO MODE** with simulated blockchain interaction:
- Prices are fetched from real CoinGecko API
- Contract calls are simulated locally
- Data is not persisted on blockchain

### Production Integration
To connect to real GenLayer blockchain:
1. Install GenLayer SDK
2. Replace simulated functions with actual contract calls
3. Add wallet connection (MetaMask, WalletConnect, etc.)
4. Handle transaction signing and confirmations

### API Rate Limits
CoinGecko free tier allows:
- 10-30 calls/minute
- If you get rate limited, prices may not update

## 🔒 Security Considerations

⚠️ **This is a demo/educational project**:
- Not audited for production use
- No real money involved
- Use testnet tokens only

For production deployment:
- Add proper access controls
- Implement anti-manipulation measures
- Add circuit breakers
- Conduct security audit
- Add pausing mechanism

## 🛠️ Troubleshooting

**Price not loading?**
- Check browser console for errors
- CoinGecko API might be rate-limited
- Try a different cryptocurrency

**Can't place bet?**
- Make sure you have sufficient balance
- Check if amount is valid (minimum 10)
- Deposit tokens first

**Settlement not working?**
- Wait for full duration to complete
- Check browser console for errors
- Try manual settlement button

## 📚 Learning Resources

- [GenLayer Documentation](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [CoinGecko API Docs](https://www.coingecko.com/en/api)
- [Web3 Integration Guide](https://docs.genlayer.com/integration)

## 🚀 Next Steps

**Enhance the dApp:**
1. Add more cryptocurrencies
2. Implement multiplayer mode (bet against other users)
3. Add price charts/history
4. Create different game modes (longer durations, higher stakes)
5. Add social features (chat, sharing results)
6. Implement referral system
7. Add NFT rewards for top players

**Advanced Features:**
- AI-powered price prediction hints
- Historical performance analytics
- Risk management tools
- Automated trading strategies
- Mobile app version

## 📝 License

Educational/Demo purposes only. Use at your own risk.

---

**Built with ❤️ on GenLayer - The Intelligent Blockchain**

*Disclaimer: This is for educational purposes only. Not financial advice. Cryptocurrency trading involves risk.*
