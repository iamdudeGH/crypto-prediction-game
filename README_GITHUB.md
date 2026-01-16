# 🎮 Crypto Prediction Game - GenLayer dApp

A decentralized prediction game built on GenLayer blockchain where players bet on cryptocurrency price movements.

![GenLayer](https://img.shields.io/badge/GenLayer-Blockchain-blue)
![Vite](https://img.shields.io/badge/Vite-7.3.1-646CFF?logo=vite)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

- 🎯 **Real-time Predictions** - Bet on crypto price movements (UP/DOWN)
- ⏱️ **Multiple Timeframes** - 30s, 60s, 2min, 5min durations
- 💰 **Fair Settlement** - Uses price at exact expiry time (not when you settle!)
- 🏆 **Leaderboard** - Track top players
- 🎊 **Win Animations** - Confetti celebration on wins
- 🔗 **MetaMask Integration** - Easy wallet connection
- 📊 **Live Stats** - Track your wins, losses, and win rate

## 🚀 Live Demo

**Deployed on Vercel:** [Your Vercel URL here]

**Contract Address:** `0x53eE6AE11F33ff59417de622f3B6474CED3983Ec`

## 🎮 How to Play

1. **Connect MetaMask** - Add GenLayer network (Chain ID: 61999)
2. **Deposit Tokens** - Minimum 100 tokens
3. **Make Prediction** - Choose crypto, direction (UP/DOWN), and duration
4. **Wait for Expiry** - Price is locked at exact expiry time
5. **Settle & Win** - Get 1.8x payout if you predicted correctly!

## 🛠️ Tech Stack

- **Frontend:** Vite + Vanilla JavaScript
- **Blockchain:** GenLayer (Intelligent Contract Network)
- **Smart Contract:** Python (GenLayer SDK)
- **SDK:** genlayer-js v0.18.3
- **Wallet:** MetaMask integration

## 📦 Installation

### Prerequisites
- Node.js 16+
- MetaMask browser extension
- GenLayer network configured in MetaMask

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/crypto-prediction-game.git
cd crypto-prediction-game

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🌐 GenLayer Network Configuration

Add this network to MetaMask:

- **Network Name:** GenLayer Studio
- **RPC URL:** `https://studio.genlayer.com/api`
- **Chain ID:** `61999` (or `0xf22f` in hex)
- **Currency Symbol:** GEN

## 📁 Project Structure

```
crypto-prediction-game/
├── index.html                          # Main HTML file
├── app_web3.js                         # Frontend logic
├── style.css                           # Styles
├── lib/
│   ├── contracts/
│   │   └── CryptoPredictionGame.js    # Contract interface
│   └── genlayer/
│       └── client.js                   # GenLayer client
├── crypto_prediction_game_historical.py # Smart contract
├── vite.config.js                      # Vite configuration
└── package.json                        # Dependencies
```

## 🎯 Smart Contract

The game uses a Python-based intelligent contract deployed on GenLayer:

**Key Features:**
- ✅ Deterministic price calculation at expiry time
- ✅ Fair settlement mechanism
- ✅ User balance management
- ✅ Leaderboard tracking
- ✅ Multiple crypto support (BTC, ETH, SOL, DOGE, ADA)

**Contract File:** `crypto_prediction_game_historical.py`

## 🔧 Development

### Run Locally

```bash
npm run dev
# Opens at http://localhost:3000
```

### Build for Production

```bash
npm run build
# Output in dist/ folder
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel --prod
```

## 🐛 Known Issues & Solutions

### Issue: Predictions not showing
**Solution:** Make sure you deployed `crypto_prediction_game_historical.py` (not the old version)

### Issue: MetaMask not connecting
**Solution:** Add GenLayer network manually with Chain ID 61999

### Issue: Settlement timing wrong
**Solution:** The new contract fixes this! Settlement now uses expiry-time price.

## 📝 Game Mechanics

### Betting
- Minimum bet: 10 tokens
- Choose: BTC, ETH, SOL, DOGE, or ADA
- Predict: UP or DOWN
- Duration: 30s, 60s, 2min, or 5min

### Settlement
- Price locked at **exact expiry time** (not when you click settle!)
- Win = 1.8x payout
- Lose = lose your bet amount
- Result determined by comparing entry price vs expiry price

### Example
```
Place bet: BTC UP, 100 tokens, 30s
Entry price: $95,000
After 30s: $95,500 (price went UP)
Result: WIN! Get 180 tokens
```

Even if you settle 1 minute later, the expiry price ($95,500) is used!

## 🏆 Leaderboard

- Tracks total wins per player
- Top 10 displayed
- Updated in real-time

## 🔐 Security

- All transactions require MetaMask approval
- Contract logic prevents manipulation
- Deterministic pricing ensures fairness
- No admin privileges or backdoors

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- **GenLayer Docs:** https://docs.genlayer.com
- **GenLayer Studio:** https://studio.genlayer.com
- **Contract Explorer:** [View on GenLayer Explorer]

## 📧 Contact

Questions or feedback? Open an issue or reach out!

---

**Built with ❤️ on GenLayer Blockchain**
