# 🧪 Testing Session - January 16, 2026

## ✅ Current Status

### Dev Server
- **Status:** ✅ Running
- **URL:** http://localhost:3002
- **Port:** 3002 (3000 and 3001 were in use)

### Contract Status
- **File:** `crypto_prediction_game_realtime.py`
- **Status:** ⚠️ Needs to be deployed to GenLayer
- **Contract Address:** Not yet deployed

### Fixed Issues
- ✅ Vite config updated to use `index.html` (was `index_web3.html`)

---

## 📋 Testing Steps Required

### Step 1: Deploy Contract to GenLayer ⚠️
You need to deploy the contract first before testing the dApp.

**Options:**
1. **Deploy via GenLayer Studio** (https://studio.genlayer.com)
   - Open GenLayer Studio
   - Create new contract
   - Paste `crypto_prediction_game_realtime.py`
   - Deploy and save the contract address

2. **Use existing deployment** (if you already deployed it)
   - Find your contract address in GenLayer Studio
   - Copy it for the next step

### Step 2: Configure Contract Address
1. Open http://localhost:3002
2. Paste your contract address in "Contract Address" field
3. Click "Save"

### Step 3: Connect MetaMask
1. Click "Connect MetaMask" button
2. Approve the connection
3. Make sure MetaMask is configured for GenLayer network:
   - **Network Name:** GenLayer Studio
   - **RPC URL:** https://studio.genlayer.com/api
   - **Chain ID:** 61999 (0xf22f)
   - **Currency Symbol:** GEN

### Step 4: Test Core Features
- [ ] Deposit tokens (test with 1000 tokens)
- [ ] Check balance updates
- [ ] Refresh crypto price (test with BTC)
- [ ] Place UP prediction
- [ ] Place DOWN prediction
- [ ] Wait for expiry and settle
- [ ] Verify win/loss works correctly
- [ ] Check confetti animation on win 🎉

### Step 5: Test UI Features
- [ ] Verify all animations work smoothly
- [ ] Check price updates with refresh button
- [ ] Verify active predictions display correctly
- [ ] Check statistics update properly
- [ ] Test leaderboard refreshes
- [ ] Verify toast notifications appear

---

## 🎯 What to Test

### 1. Wallet Connection
- MetaMask connects without errors
- Wallet address displays correctly
- Balance shows after connection

### 2. Price Fetching
- Select different cryptos (BTC, ETH, SOL, DOGE, ADA)
- Click "Refresh Price"
- Verify price displays correctly (not NaN)
- Check "Last updated" timestamp

### 3. Deposit/Withdraw
- Deposit tokens (try 1000)
- Balance updates immediately
- Toast notification appears

### 4. Placing Predictions
- Enter bet amount (minimum 10 tokens)
- Select duration (30s, 60s, 2m, 5m)
- Click UP or DOWN button
- Verify prediction card appears in "Active Predictions"
- Check entry price is correct

### 5. Settling Predictions
- Wait for expiry time
- "Settle Now" button should appear
- Click settle button
- Verify win/loss message
- Check confetti animation on win 🎉
- Balance should update

### 6. Statistics
- Total predictions counter increments
- Wins counter increases on win
- Losses counter increases on loss
- Win rate percentage calculates correctly

### 7. Leaderboard
- Top players display
- Scores show correctly
- Rankings update after wins

---

## 🐛 Known Issues to Watch For

Based on PROJECT_SUMMARY, these were previously fixed:
- ✅ Chain ID mismatch (now 0xf22f)
- ✅ Price showing NaN (Map/BigInt handling fixed)
- ✅ Balance not updating (BigInt conversion fixed)
- ✅ Predictions settling too early (time calculation fixed)
- ✅ Auto-settle removed (manual settle with buttons)

---

## 📝 Test Results

### Manual Testing Checklist

| Feature | Status | Notes |
|---------|--------|-------|
| Dev server running | ✅ | Port 3002 |
| Contract deployed | ⏳ | Waiting for deployment |
| MetaMask connection | ⏳ | Pending |
| Deposit tokens | ⏳ | Pending |
| Price refresh | ⏳ | Pending |
| Place UP prediction | ⏳ | Pending |
| Place DOWN prediction | ⏳ | Pending |
| Settle prediction | ⏳ | Pending |
| Win confetti | ⏳ | Pending |
| Statistics update | ⏳ | Pending |
| Leaderboard | ⏳ | Pending |

---

## 🚀 Next Actions

**Right Now:**
1. **Deploy the contract** to GenLayer Studio
   - File: `crypto_prediction_game_realtime.py`
   - Save the contract address

2. **Open the dApp:** http://localhost:3002

3. **Configure and test** following the steps above

**After Testing:**
- Report any bugs found
- Verify all features work as expected
- Move to GenLayer branding phase

---

## 📞 Quick Reference

- **Contract File:** `crypto_prediction_game_realtime.py`
- **Frontend:** http://localhost:3002
- **GenLayer Studio:** https://studio.genlayer.com
- **GenLayer Docs:** https://docs.genlayer.com
- **Chain ID:** 0xf22f (61999)
- **RPC URL:** https://studio.genlayer.com/api

---

**Status:** ⚠️ Ready to test once contract is deployed!
