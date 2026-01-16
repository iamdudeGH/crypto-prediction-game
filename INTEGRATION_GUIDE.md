# 🔌 GenLayer Integration Guide

## Current Status

✅ **Smart Contract Fixed** - `crypto_prediction_game.py` now works without `gl.msg.sender`
⚠️ **Frontend Integration** - Needs GenLayer SDK or proper Web3 connection

## The Problem

The error you're seeing:
```
Unexpected error in eth_call: 'to'
KeyError: 'to'
```

This happens because:
1. The frontend tries to call the contract using standard Web3 methods
2. But the contract address is not configured (`CONFIG.contractAddress = null`)
3. So the `eth_call` request is missing the `to` field

## Solutions

### Option 1: Use Simplified Single-User Contract (RECOMMENDED FOR TESTING)

The **easiest way** to test your dApp is to use the simplified version that doesn't require passing user addresses:

**Switch to `crypto_prediction_simple.py`:**
- ✅ No user_address parameters needed
- ✅ Single-user experience
- ✅ Works perfectly with current frontend
- ✅ Great for learning and testing

**How to use:**
1. Deploy `crypto_prediction_simple.py` in GenLayer Studio
2. Test it directly in the studio (no frontend needed)
3. Methods to try:
   ```python
   # Deposit tokens
   contract.deposit(1000)
   
   # Check balance
   contract.get_balance()
   
   # Place prediction
   contract.place_prediction("BTC", "UP", 100, 60)
   
   # Check active prediction
   contract.get_active_prediction()
   
   # Settle after time passes
   contract.settle_prediction()
   
   # Reset for new prediction
   contract.reset_prediction()
   ```

### Option 2: Connect Frontend to Multi-User Contract

For the full multi-user `crypto_prediction_game.py`:

#### Step 1: Deploy Your Contract

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Copy `crypto_prediction_game.py` into the editor
3. Click "Deploy"
4. **Copy the contract address** you receive

#### Step 2: Update Frontend Configuration

Two options:

**A) Use the new GenLayer-ready file:**
```html
<!-- In index.html, change line 114: -->
<script src="app_genlayer.js"></script>

<!-- Then update app_genlayer.js line 9: -->
contractAddress: '0xYOUR_ACTUAL_CONTRACT_ADDRESS_HERE',
```

**B) Or keep using demo mode:**
- The current `app.js` runs in demo mode (simulated data)
- Good for testing UI without blockchain
- No contract calls are made

#### Step 3: Handle User Addresses in Frontend

Since GenLayer doesn't auto-inject `msg.sender`, you need to pass it:

```javascript
// When calling contract methods, include user address:

// Deposit
await contract.call('deposit', [userAddress, amount]);

// Place prediction  
await contract.call('place_prediction', [
    userAddress,
    'BTC',
    'UP', 
    100,
    60
]);

// Get balance
await contract.call('get_balance', [userAddress]);
```

### Option 3: Use GenLayer Studio Only (NO FRONTEND)

The **simplest approach** for now:

1. Deploy contract in GenLayer Studio
2. Test everything directly in the studio console
3. Skip frontend integration until GenLayer releases their official JS SDK

**Benefits:**
- ✅ No Web3 complexity
- ✅ Direct contract testing
- ✅ See exactly what works
- ✅ Perfect for development

## Current File Status

| File | Status | Purpose |
|------|--------|---------|
| `crypto_prediction_game.py` | ✅ Fixed | Multi-user game (needs user_address params) |
| `crypto_prediction_simple.py` | ✅ Ready | Single-user game (no user_address needed) |
| `app.js` | ⚠️ Demo Mode | Original frontend (simulated data only) |
| `app_genlayer.js` | ✅ New | GenLayer-ready (needs contract address) |
| `index.html` | ✅ Ready | Works with either JS file |

## Recommended Next Steps

### For Quick Testing:
1. ✅ Use `crypto_prediction_simple.py`
2. ✅ Test in GenLayer Studio console
3. ✅ Skip frontend for now

### For Full dApp:
1. Deploy `crypto_prediction_game.py`
2. Update `app_genlayer.js` with contract address
3. Wait for GenLayer's official JS SDK for easier integration

## Example: Testing in GenLayer Studio

```python
# Deploy crypto_prediction_simple.py, then:

# 1. Deposit some tokens
result = contract.deposit(1000)
print(result)  # "Deposited 1000. New balance: 1000"

# 2. Check balance
balance = contract.get_balance()
print(balance)  # 1000

# 3. Place a prediction
result = contract.place_prediction("BTC", "UP", 100, 60)
print(result)  # Shows prediction details

# 4. Check current prediction
status = contract.get_active_prediction()
print(status)  # Shows prediction status

# 5. Wait 60 seconds, then settle
result = contract.settle_prediction()
print(result)  # Shows if you won or lost

# 6. Check stats
stats = contract.get_stats()
print(stats)  # Shows win/loss record
```

## Need Help?

- 📚 [GenLayer Docs](https://docs.genlayer.com)
- 💬 [GenLayer Discord](https://discord.gg/genlayer)
- 🎓 [Vibecoding Tutorials](https://vibecoding.com)

## Summary

**The `'to'` error is fixed by:**
1. Either using the contract directly in GenLayer Studio (recommended)
2. Or updating the frontend with your deployed contract address

**The `gl.msg.sender` error is fixed by:**
- ✅ Already fixed! Contract now uses `user_address` parameters
