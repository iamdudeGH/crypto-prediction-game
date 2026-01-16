# 🚀 Quick Deployment Guide - Historical Price Fix

## ✅ Pre-Deployment Checklist

- [x] New contract created: `crypto_prediction_game_historical.py`
- [x] Contract interface compatible: `lib/contracts/CryptoPredictionGame.js`
- [x] Frontend compatible: No changes needed
- [x] Documentation complete
- [x] Issue understood and fixed

---

## 📋 Deployment Steps

### **Option 1: Using GenLayer Studio (Recommended)**

1. **Open GenLayer Studio:**
   ```
   https://studio.genlayer.com
   ```

2. **Deploy Contract:**
   - Click "Create New Contract"
   - Copy entire content from `crypto_prediction_game_historical.py`
   - Paste into the editor
   - Click "Deploy" button
   - Wait for deployment confirmation

3. **Copy Contract Address:**
   - After successful deployment, copy the contract address
   - Example: `0x1234567890abcdef...`

4. **Update Your dApp:**
   - Your dApp is running at: http://localhost:3002
   - In the UI, find "Contract Address" field
   - Paste the new contract address
   - Click "Save" button
   - Refresh the page (F5)

5. **Connect & Test:**
   - Click "Connect Wallet"
   - Approve MetaMask connection
   - Deposit some tokens (e.g., 1000)
   - Ready to test!

---

### **Option 2: Using GenLayer CLI**

```bash
# Make sure you're in the project directory
cd /path/to/your/project

# Select network
genlayer network

# Deploy the contract
genlayer deploy

# Follow prompts to deploy crypto_prediction_game_historical.py
# Copy the returned contract address
```

Then update frontend as in Option 1, step 4.

---

## 🧪 Testing the Fix

### **Test Case: 30-Second Prediction**

**Goal:** Verify settlement uses expiry-time price, not current price

**Steps:**

1. **Place Prediction:**
   ```
   - Crypto: BTC
   - Direction: UP (or DOWN, doesn't matter)
   - Amount: 100 tokens
   - Duration: 30 seconds
   ```
   - ✅ Note the entry price shown

2. **Wait for Expiry:**
   ```
   - Wait exactly 30 seconds
   - Prediction card shows "READY"
   - Note the current BTC price at this moment
   ```

3. **Keep Waiting (Critical Test):**
   ```
   - Wait another 30-60 seconds
   - DO NOT click Settle yet
   - Watch the BTC price change on the main card
   - The current price should be different now
   ```

4. **Settle the Prediction:**
   ```
   - Now click "Settle Now" button
   - Read the settlement message carefully
   ```

5. **Verify the Fix:**
   ```
   ✅ Settlement message shows: "Entry → Exit (at expiry)"
   ✅ Exit price matches the price from step 2 (30s mark)
   ✅ Exit price DOES NOT match current price from step 3
   ✅ Win/loss calculated based on 30-second price
   ```

**Expected Behavior:**
- If BTC went UP at 30 seconds → WIN (even if down now)
- If BTC went DOWN at 30 seconds → LOSE (even if up now)
- Settlement time doesn't affect outcome ✅

---

## 📊 Quick Visual Test

### **Before Fix (Old Contract):**
```
Place: $95,000
After 30s: $95,500 (UP - should WIN)
After 60s: $94,800 (DOWN from entry)
Settle at 60s: ❌ LOSE (uses $94,800)
```
**Problem:** Should have won at 30s, but lost due to late settlement

### **After Fix (New Contract):**
```
Place: $95,000
After 30s: $95,500 (UP - should WIN)
After 60s: $94,800 (DOWN from entry)
Settle at 60s: ✅ WIN (uses $95,500 from 30s)
```
**Fixed:** Settlement uses expiry-time price regardless of when you click!

---

## 🎯 Success Indicators

You know it's working correctly when:

1. ✅ You can settle anytime after expiry
2. ✅ Late settlement doesn't change outcome
3. ✅ Settlement message shows "(at expiry)"
4. ✅ Price used matches expiry time, not current time
5. ✅ No errors in browser console
6. ✅ Balance updates correctly after settlement

---

## 🐛 Troubleshooting

### **Issue: "Prediction not found"**
- **Cause:** Old contract address still set
- **Fix:** Update contract address in UI, click Save, refresh

### **Issue: "Too early!"**
- **Cause:** Haven't waited for expiry yet
- **Fix:** Wait for countdown to reach 0, then "READY" appears

### **Issue: MetaMask connection issues**
- **Cause:** Wrong network or cached data
- **Fix:** Switch to GenLayer network in MetaMask, refresh page

### **Issue: Balance shows 0**
- **Cause:** New contract = fresh start
- **Fix:** Deposit tokens again (balances don't carry over)

### **Issue: Prices look weird**
- **Cause:** Mock prices with variation
- **Fix:** This is normal! Prices vary ±10% from base

---

## 📝 Post-Deployment Notes

### **Remember:**
- ✅ Old contract predictions cannot be migrated
- ✅ Users need to re-deposit on new contract
- ✅ Leaderboard starts fresh
- ✅ All frontend code works without changes

### **Optional:**
- Update PROJECT_SUMMARY.md with new contract address
- Announce upgrade to users (if you have any)
- Test with multiple timeframes (30s, 60s, 2m, 5m)

---

## 📞 Need Help?

### **Check These Files:**
- `SETTLEMENT_FIX_SUMMARY.md` - Detailed explanation
- `HISTORICAL_PRICE_UPGRADE.md` - Complete technical guide
- `crypto_prediction_game_historical.py` - New contract code

### **Common Questions:**

**Q: Do I need to redeploy the frontend?**
A: No! Just update the contract address in the UI.

**Q: Will my old predictions work?**
A: No, they're on the old contract. Finish them first or start fresh.

**Q: Are real prices used?**
A: No, deterministic mock prices. Same timestamp = same price always.

**Q: Can users exploit the new system?**
A: No! Settlement time doesn't affect outcome anymore.

**Q: Is it slower now?**
A: No, actually faster! No external API calls needed.

---

## 🎉 You're Ready!

**Next Actions:**
1. ✅ Deploy `crypto_prediction_game_historical.py`
2. ✅ Update contract address in UI
3. ✅ Test with 30-second predictions
4. ✅ Verify settlement timing works
5. ✅ Enjoy fair gameplay!

**The fix is complete and ready to deploy! 🚀**

---

**Version:** 0.2.0  
**Status:** ✅ Ready to Deploy  
**Contract:** `crypto_prediction_game_historical.py`  
**Compatibility:** All existing frontend code works
