# 🚀 Crypto Prediction dApp - Deployment Guide

## ✅ Contract Fixed!

The contract has been updated to use GenLayer-compatible storage types:
- Added `@gl.allow_storage` decorator for the Prediction class
- Changed `dict` to `dict[str, u256]` and `dict[str, list[Prediction]]`
- Updated all return types to simple types (str instead of dict/list for complex objects)

## 📝 Step-by-Step Deployment

### 1. Deploy the Smart Contract

1. **Open GenLayer Studio**
   - Go to: https://studio.genlayer.com

2. **Create New Contract**
   - Click "New Contract" or open the file explorer
   - Create a new file called `crypto_prediction_game.py`

3. **Copy the Contract Code**
   - Copy ALL content from `crypto_prediction_game.py`
   - Paste into GenLayer Studio

4. **Deploy the Contract**
   - Click the **"Deploy"** button
   - Wait for deployment to complete
   - **Copy the contract address** (e.g., `0x1234567890abcdef...`)

### 2. Test the Contract in GenLayer Studio

**Try these methods in order:**

#### A. Deposit Tokens
```
Method: deposit
Parameters:
  amount: 1000
```
Expected: "Deposited 1000. New balance: 1000"

#### B. Check Balance
```
Method: get_balance
Parameters: (none, or your address)
```
Expected: 1000

#### C. Get Current Price
```
Method: get_current_price
Parameters:
  crypto_symbol: "BTC"
```
Expected: {"symbol": "BTC", "price_usd": 45000.00, ...}

#### D. Place a Prediction
```
Method: place_prediction
Parameters:
  crypto_symbol: "BTC"
  direction: "UP"
  bet_amount: 100
  duration_seconds: 60
```
Expected: "Prediction #0 placed: UP on BTC at $45000.00 for 60s"

#### E. Check Your Predictions
```
Method: get_user_predictions
Parameters: (none)
```
Expected: "Total predictions: 1"

#### F. Wait 60 seconds, then Settle
```
Method: settle_prediction
Parameters:
  prediction_id: 0
```
Expected: "Settled: WON - Entry: $45000.00, Exit: $45200.00, Payout: 180"

#### G. View Leaderboard
```
Method: get_leaderboard
Parameters: (none)
```
Expected: Shows top winners

### 3. Connect Frontend (Optional)

If you want to use the HTML/CSS/JS frontend:

1. **Update Contract Address**
   - Open `app.js`
   - Line 4: Replace `contractAddress: null` with your deployed address
   - Example: `contractAddress: '0x1234567890abcdef...'`

2. **Integrate GenLayer SDK**
   - The current frontend runs in DEMO mode
   - To connect to real contract, you'll need to integrate GenLayer's JavaScript SDK
   - See: https://docs.genlayer.com/sdk

3. **Run the Frontend**
   ```bash
   # Simple HTTP server
   python -m http.server 8000
   
   # Or just open index.html in browser
   ```

## 🎮 How to Play (In GenLayer Studio)

1. **Deposit** some tokens (e.g., 1000)
2. **Get current price** to see what you're betting on
3. **Place prediction**: Choose UP or DOWN
4. **Wait** for the duration to expire (or use very short durations for testing)
5. **Settle** your prediction to see if you won
6. **Check leaderboard** to see your ranking

## 📊 Contract Methods Reference

### View Methods (Free - No Gas)
| Method | Parameters | Returns |
|--------|-----------|---------|
| `get_current_price` | `crypto_symbol: str` | Current price data |
| `get_balance` | `user_address: str` (optional) | User's balance |
| `get_user_predictions` | `user_address: str` (optional) | Prediction count |
| `get_leaderboard` | none | Top 10 players |
| `get_game_stats` | none | Overall statistics |

### Write Methods (Require Transaction)
| Method | Parameters | Description |
|--------|-----------|-------------|
| `deposit` | `amount: u256` | Add funds to play |
| `place_prediction` | `crypto_symbol, direction, bet_amount, duration_seconds` | Place a bet |
| `settle_prediction` | `prediction_id: u256` | Settle completed prediction |

## ⚠️ Important Notes

### Supported Cryptocurrencies
- BTC (Bitcoin)
- ETH (Ethereum)
- SOL (Solana)
- DOGE (Dogecoin)
- ADA (Cardano)

### API Usage
- The contract uses CoinGecko API (free tier)
- Rate limit: ~10-30 calls/minute
- If you get rate limited, wait a minute and try again

### Testing Tips
1. **Use short durations** for testing (30-60 seconds)
2. **Start with small bets** (100 tokens)
3. **Check balance** before placing predictions
4. **Wait for full duration** before settling

### Common Issues

**"Insufficient balance"**
- Solution: Call `deposit()` first

**"Prediction not yet expired"**
- Solution: Wait for the full duration to pass

**"Failed to fetch price"**
- Solution: Check internet connection or try different crypto symbol

**"ERROR: Direction must be 'UP' or 'DOWN'"**
- Solution: Use exactly "UP" or "DOWN" (case-insensitive)

## 🎯 Next Steps

Once deployed and tested:

1. **Share your contract** - Send the address to friends to play
2. **Enhance features** - Add more cryptos, longer durations, etc.
3. **Build UI** - Create custom frontend with your branding
4. **Add analytics** - Track win rates, popular coins, etc.
5. **Monetize** - Add small fees, create tournaments, etc.

## 📚 Resources

- [GenLayer Documentation](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [GenLayer Discord](https://discord.gg/genlayer) - Get help from community

## 🐛 Troubleshooting

If deployment fails:
1. Check all type annotations are correct
2. Ensure `@gl.allow_storage` is on Prediction class
3. Verify no syntax errors
4. Check GenLayer Studio console for specific errors

If methods don't appear:
1. Ensure all public methods have return type annotations
2. Check decorators are `@gl.public.view` or `@gl.public.write`
3. Try redeploying the contract

---

**Good luck with your dApp! 🚀**

If you encounter any issues, feel free to ask for help!
