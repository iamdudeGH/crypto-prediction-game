# 🚀 Web3 dApp Setup Guide

## 🎉 You Now Have a REAL Web3 dApp!

Your crypto prediction game is now a **fully functional Web3 application** that connects to the GenLayer blockchain using MetaMask!

---

## 📋 Prerequisites

1. **Node.js** installed (v18 or higher)
2. **MetaMask** browser extension installed
3. **Deployed contract** on GenLayer (using `crypto_prediction_game_realtime.py`)
4. **Contract address** from your deployment

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Install genlayer-js SDK and dependencies
npm install
```

This will install:
- `genlayer-js` - GenLayer blockchain SDK
- `viem` - Ethereum library
- `vite` - Development server

### Step 2: Run Development Server

```bash
# Start the dev server
npm run dev
```

The app will open at: `http://localhost:3000`

### Step 3: Configure Contract

1. **Copy your deployed contract address** from GenLayer Studio
2. **Paste it** in the "Contract Address" field
3. **Click "Save"**

### Step 4: Connect MetaMask

1. **Click "Connect MetaMask"** button
2. **Approve** the connection in MetaMask
3. **Switch to GenLayer network** (it will prompt you to add the network)
4. **You're connected!** 🎉

### Step 5: Start Playing!

1. **Deposit tokens** - Click "Deposit Tokens" (e.g., 1000)
2. **Place predictions** - Select crypto, amount, duration
3. **Click UP or DOWN** - Transaction will be sent to blockchain
4. **Wait for settlement** - Based on real timestamps
5. **Check results** - Win or lose, balance updates automatically

---

## 🎮 How It Works

### Architecture

```
Frontend (HTML/CSS/JS)
    ↓
app_web3.js (Your dApp logic)
    ↓
lib/contracts/CryptoPredictionGame.js (Contract wrapper)
    ↓
lib/genlayer/client.js (GenLayer SDK)
    ↓
genlayer-js SDK
    ↓
MetaMask
    ↓
GenLayer Blockchain
    ↓
Your Smart Contract (crypto_prediction_game_realtime.py)
```

### Key Features

✅ **MetaMask Integration**
- Auto-detect MetaMask
- Connect/disconnect wallet
- Auto-add GenLayer network
- Handle account/network changes

✅ **Real Blockchain Transactions**
- All deposits, predictions, settlements are real transactions
- Sign with MetaMask
- Wait for confirmations
- Get transaction receipts

✅ **Live Data**
- Read contract state (balance, predictions, leaderboard)
- Auto-refresh every 10 seconds
- Real-time updates after transactions

✅ **Error Handling**
- Network switching
- Transaction failures
- User rejection
- Clear error messages

---

## 📁 File Structure

```
crypto-prediction-game/
├── index_web3.html              # Main HTML (Web3 version)
├── app_web3.js                  # Main app logic (Web3)
├── style.css                    # Styling
├── package.json                 # Dependencies
├── vite.config.js               # Vite configuration
├── lib/
│   ├── genlayer/
│   │   └── client.js            # GenLayer SDK wrapper
│   └── contracts/
│       └── CryptoPredictionGame.js  # Contract class
└── crypto_prediction_game_realtime.py  # Smart contract
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file:

```env
VITE_CONTRACT_ADDRESS=0xYourContractAddress
VITE_GENLAYER_RPC=https://studio.genlayer.com/api
```

### Network Configuration

The dApp auto-configures GenLayer network:

```javascript
{
  chainId: '0xF22F',  // 61999
  chainName: 'GenLayer Studio',
  symbol: 'GEN',
  rpcUrls: ['https://studio.genlayer.com/api']
}
```

---

## 🎯 Contract Functions

### View Functions (No Gas)

```javascript
// Get balance
await contract.getBalance(userAddress);

// Get current price
await contract.getCurrentPrice('BTC');

// Get predictions
await contract.getUserPredictions(userAddress);

// Get leaderboard
await contract.getLeaderboard();

// Get current time
await contract.getCurrentTime();
```

### Write Functions (Requires Gas)

```javascript
// Deposit tokens
await contract.deposit(userAddress, 1000);

// Place prediction
await contract.placePrediction(
  userAddress,
  'BTC',      // symbol
  'UP',       // direction
  100,        // bet amount
  60          // duration (seconds)
);

// Settle prediction
await contract.settlePrediction(userAddress, predictionId);
```

---

## 🧪 Testing the Web3 dApp

### Test Sequence:

1. **Install and run**
   ```bash
   npm install
   npm run dev
   ```

2. **Connect MetaMask**
   - Click "Connect MetaMask"
   - Approve connection
   - Switch to GenLayer network

3. **Enter contract address**
   - Paste your deployed contract address
   - Click "Save"

4. **Deposit tokens**
   - Enter amount (e.g., 1000)
   - Click "Deposit Tokens"
   - Approve in MetaMask
   - Wait for confirmation ✅

5. **Place prediction**
   - Select BTC, 100 tokens, 60 seconds
   - Click "UP"
   - Approve in MetaMask
   - Wait for confirmation ✅

6. **Wait for expiry**
   - Wait 60+ real seconds
   - Blockchain time is real!

7. **Settle**
   - Click "Settle" (when available)
   - Approve in MetaMask
   - See result: WON or LOST ✅

8. **Check stats**
   - Balance updates automatically
   - Stats refresh
   - Leaderboard updates

---

## 🔄 Development Workflow

### During Development:

```bash
# Terminal 1: Run dev server
npm run dev

# Terminal 2: Watch for changes
# (Vite auto-reloads on file changes)
```

### Building for Production:

```bash
# Build optimized version
npm run build

# Preview production build
npm run preview
```

### Deploying:

```bash
# Build
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - GitHub Pages
# - IPFS
# - Any static hosting
```

---

## 🆚 Comparison: Versions

| Feature | Automated (Local) | Web3 (This Version) |
|---------|------------------|---------------------|
| Blockchain | ❌ Simulated | ✅ Real GenLayer |
| MetaMask | ❌ Not needed | ✅ Required |
| Transactions | ❌ Instant (fake) | ✅ Real (with confirmations) |
| Contract | ❌ JS simulation | ✅ Deployed smart contract |
| Data | ❌ localStorage | ✅ Blockchain state |
| Multi-user | ❌ Single browser | ✅ True multi-user |
| Testing | ✅ Perfect for demos | ✅ Perfect for production |

---

## 🐛 Troubleshooting

### Issue: "MetaMask not installed"
**Solution:** Install MetaMask browser extension

### Issue: "Wrong network"
**Solution:** 
- Click "Connect MetaMask"
- Approve network switch
- MetaMask will add GenLayer network automatically

### Issue: "Contract not configured"
**Solution:** 
- Enter your deployed contract address
- Click "Save"

### Issue: "Transaction failed"
**Solution:**
- Check you have enough balance
- Check network connection
- Try again

### Issue: "Module not found"
**Solution:**
```bash
rm -rf node_modules
npm install
```

---

## 📊 Network Information

### GenLayer Studio (Testnet)

- **Chain ID:** 61999 (0xF22F)
- **RPC URL:** https://studio.genlayer.com/api
- **Symbol:** GEN
- **Explorer:** Coming soon
- **Faucet:** Available in Studio

---

## 🎯 Next Steps

### For Testing:
1. ✅ Deploy contract
2. ✅ Configure dApp
3. ✅ Connect MetaMask
4. ✅ Test all functions

### For Production:
1. 📝 Security audit
2. 🎨 UI improvements
3. 📱 Mobile optimization
4. 🌐 Custom domain
5. 📊 Analytics

### For Enhancement:
1. 💰 Real API prices
2. 📈 Price charts
3. 🏆 Advanced leaderboard
4. 🎮 Tournaments
5. 📱 Mobile app

---

## 🎊 Congratulations!

You now have a **REAL Web3 dApp** that:

✅ Connects to MetaMask  
✅ Interacts with real blockchain  
✅ Handles real transactions  
✅ Uses GenLayer smart contract  
✅ Has production-ready code  

**Start the dev server and play with real blockchain! 🚀**

```bash
npm run dev
```

---

## 📞 Support

- **GenLayer Docs:** https://docs.genlayer.com
- **GenLayer Discord:** https://discord.gg/8Jm4v89VAu
- **GenLayer Studio:** https://studio.genlayer.com
- **genlayer-js GitHub:** https://github.com/genlayerlabs/genlayer-js

---

**Happy Web3 Gaming! 🎯🚀**
