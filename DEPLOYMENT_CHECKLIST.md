# 🚀 Deployment Checklist

## ✅ All Contracts Updated

All Python contract files now have the correct header format:

```python
# v1.0.0
# { "Depends": "py-genlayer:test" }
```

### Updated Files:
- ✅ `crypto_prediction_simple.py`
- ✅ `crypto_prediction_game.py`
- ✅ `my_first_contract.py`
- ✅ `wizard_of_coin.py` (was already correct)

---

## 🔍 If You Still See "absent_runner_comment" Error

### Possible Causes:

1. **Browser Cache**
   - Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
   - Clear browser cache
   - Try incognito/private mode

2. **Copying Old Version**
   - Make sure you're copying from the **latest saved file**
   - Re-open the file in your editor
   - Copy directly from workspace files

3. **GenLayer Studio Issue**
   - Refresh the GenLayer Studio page
   - Log out and log back in
   - Try a different browser

4. **Testing Wrong File**
   - Make sure you're deploying the correct contract
   - Double-check the file name

---

## ✅ Correct Header Format

**Both lines are required:**

```python
# v1.0.0                              ← Version comment
# { "Depends": "py-genlayer:test" }  ← Runner comment
                                       ← Blank line
from genlayer import *                 ← Imports
```

**Common Mistakes:**
- ❌ Missing version line
- ❌ Extra spaces in JSON: `{ "Depends" : "py-genlayer:test" }`
- ❌ Wrong quotes: `{ 'Depends': 'py-genlayer:test' }`
- ❌ Missing blank line after comments

---

## 🧪 How to Test

### Step 1: Copy the Latest File

Open one of these files in your workspace:
- `crypto_prediction_simple.py` (recommended for testing)
- `crypto_prediction_game.py`
- `my_first_contract.py`

### Step 2: Verify Headers

The first 3 lines should be:
```python
# v1.0.0
# { "Depends": "py-genlayer:test" }

```

### Step 3: Deploy in GenLayer Studio

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Paste the entire file
3. Click "Deploy"
4. Should work without "absent_runner_comment" error!

---

## 📝 Quick Test Commands

After successful deployment:

### For `crypto_prediction_simple.py`:
```python
contract.deposit(1000)
contract.get_balance()
contract.get_current_price("BTC")
contract.place_prediction("BTC", "UP", 100, 60)
contract.get_active_prediction()
```

### For `my_first_contract.py`:
```python
contract.get_name()
contract.greet()
contract.set_name("YourName")
```

---

## 🆘 Still Not Working?

If the error persists after trying all the above:

1. **Copy the working example** - Use `wizard_of_coin.py` as a test
2. **Check GenLayer Studio status** - Maybe there's a platform issue
3. **Share the exact error** - The full error message might have more clues
4. **Try a minimal contract** - Test with `my_first_contract.py` first

---

## ✅ Success Indicators

You'll know it works when:
- ✅ No "absent_runner_comment" error
- ✅ Contract compiles successfully
- ✅ You can call contract methods
- ✅ Methods return expected results

---

## 💡 Pro Tips

- Always copy the **entire file** including headers
- Check that no extra characters were added when copying
- Use a plain text editor (not Word or rich text)
- Make sure file encoding is UTF-8

---

**All your contract files are now correctly formatted and ready to deploy!** 🚀
