# MetaMask Network Connection Fix

## Problem
You're seeing this error when trying to connect MetaMask:
```
Failed to connect: Could not add network that points to same RPC endpoint as existing network for chain 0xf22f ('GenLayer Studio')
```

## Why This Happens
This error occurs because MetaMask already has a network configured with:
- **Chain ID:** `0xF22F` (61999 decimal)
- **RPC URL:** `https://studio.genlayer.com/api`

MetaMask prevents adding duplicate networks with the same RPC endpoint.

## Solution Options

### Option 1: Automatic Fix (Recommended)
The code has been updated to handle this automatically. Just try connecting again:

1. **Refresh the page** (to load the updated code)
2. Click **"Connect MetaMask"**
3. The app will now:
   - Try to switch to the existing GenLayer network
   - If that fails, show you a helpful error message

### Option 2: Manual Network Switch
If the automatic fix doesn't work, switch networks manually in MetaMask:

1. Open **MetaMask**
2. Click the **network dropdown** (top left, usually says "Ethereum Mainnet")
3. Look for **"GenLayer Studio"** or any network with chain ID **61999**
4. Select that network
5. Return to the dApp and try connecting again

### Option 3: Remove and Re-add Network
If you want to start fresh:

1. Open **MetaMask**
2. Go to **Settings** → **Networks**
3. Find the network with:
   - Chain ID: **61999** (or 0xF22F)
   - RPC URL: **https://studio.genlayer.com/api**
4. **Delete** that network
5. Return to the dApp and click **"Connect MetaMask"**
6. It will now add the network fresh

## GenLayer Network Details
For reference, here are the correct network settings:

- **Network Name:** GenLayer Studio
- **RPC URL:** https://studio.genlayer.com/api
- **Chain ID:** 61999 (hex: 0xF22F)
- **Currency Symbol:** GEN
- **Block Explorer:** (none)

## Troubleshooting

### Still Getting Errors?
1. **Check MetaMask version:** Make sure you're using the latest version
2. **Clear browser cache:** Sometimes helps with connection issues
3. **Try another browser:** Test in Chrome/Brave if using Firefox, or vice versa

### Network Shows Wrong Name?
That's okay! As long as the Chain ID is **61999** (0xF22F), it will work.

### Connection Successful But No Data?
Make sure you've:
1. ✅ Entered your **contract address** in the dApp
2. ✅ Clicked **"Save"** to save the contract address
3. ✅ The contract is actually deployed on GenLayer

## Next Steps After Connecting

1. **Enter Contract Address:** Paste your deployed contract address from `crypto_prediction_game_realtime.py`
2. **Click Save:** Save the contract address
3. **Deposit Tokens:** Click "Deposit Tokens" to add balance
4. **Start Playing:** Select a crypto, choose UP or DOWN, and place your bet!

## Need Help?
If you're still having issues:
- Check the browser console (F12) for detailed error messages
- Verify your contract is deployed: Check GenLayer Studio
- Make sure you're using the realtime contract address
