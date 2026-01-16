# 🚀 Live Deployment Guide

## 📋 Overview

Your dApp has 2 parts to deploy:
1. **Smart Contract** → Deploy to GenLayer (already done!)
2. **Frontend** → Deploy to web hosting (Vercel/Netlify/GitHub Pages)

---

## 🎯 Quick Deploy (Recommended: Vercel)

### **Step 1: Prepare Your Project**

1. **Make sure contract is deployed:**
   - You already have contract at: `0x53eE6AE11F33ff59417de622f3B6474CED3983Ec`
   - This is your production contract address ✅

2. **Update contract address in code (optional but recommended):**
   ```javascript
   // In app_web3.js, you can set a default contract address
   const DEFAULT_CONTRACT_ADDRESS = '0x53eE6AE11F33ff59417de622f3B6474CED3983Ec';
   ```

---

### **Step 2: Deploy to Vercel (Easiest & Free)**

#### **Option A: Using Vercel Website (No Code Changes Needed)**

1. **Go to:** https://vercel.com
2. **Sign up/Login** (can use GitHub account)
3. **Click "New Project"**
4. **Import your project:**
   - Click "Import Git Repository"
   - OR click "Deploy from existing code"
   - OR drag & drop your project folder

5. **Configure project:**
   - **Framework Preset:** Vite (if asked)
   - **Root Directory:** `.` (current directory)
   - **Build Command:** `npm run build` (or leave empty if using static files)
   - **Output Directory:** `dist` (or `.` if no build step)

6. **Click "Deploy"** 🚀

7. **Wait 1-2 minutes** for deployment

8. **Get your live URL:**
   - Example: `https://your-project-name.vercel.app`
   - Share this link with anyone! 🎉

---

#### **Option B: Using Vercel CLI (For Developers)**

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to your project
cd /path/to/your/crypto-prediction-game

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name? crypto-prediction-game
# - Directory? ./
# - Override settings? N

# Deploy to production
vercel --prod
```

**Done!** Your live URL will be shown in the terminal.

---

### **Step 3: Deploy to Netlify (Alternative)**

1. **Go to:** https://netlify.com
2. **Sign up/Login**
3. **Click "Add new site" → "Deploy manually"**
4. **Drag and drop your entire project folder**
5. **Wait for deployment**
6. **Get your live URL:** `https://your-site.netlify.app`

---

### **Step 4: Deploy to GitHub Pages (Free)**

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/crypto-prediction-game.git
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Go to your repo → Settings → Pages
   - Source: Deploy from branch
   - Branch: `main` → folder: `/ (root)`
   - Click Save

3. **Your live URL:**
   - `https://yourusername.github.io/crypto-prediction-game/`

---

## 🔧 Configuration for Production

### **Update Default Contract Address (Optional)**

Edit `app_web3.js` to set a default contract:

```javascript
// Around line 20-30, add:
const DEFAULT_CONTRACT_ADDRESS = '0x53eE6AE11F33ff59417de622f3B6474CED3983Ec';

// In the init function, use it as default:
async function init() {
    // ... existing code ...
    
    // Set default contract address
    const savedAddress = localStorage.getItem('contractAddress');
    if (!savedAddress) {
        localStorage.setItem('contractAddress', DEFAULT_CONTRACT_ADDRESS);
        state.contractAddress = DEFAULT_CONTRACT_ADDRESS;
        document.getElementById('contractAddress').value = DEFAULT_CONTRACT_ADDRESS;
    }
    
    // ... rest of code ...
}
```

This way users don't need to enter the contract address manually!

---

## 📝 Pre-Deployment Checklist

- [ ] Contract deployed to GenLayer
- [ ] Contract address saved
- [ ] Frontend tested locally (npm run dev)
- [ ] MetaMask works with the dApp
- [ ] Deposit/Bet/Settle all work
- [ ] Remove any test/debug code (optional)
- [ ] Update README.md with contract address

---

## 🌐 Deployment Comparison

| Platform | Free Tier | Custom Domain | Deploy Time | Difficulty |
|----------|-----------|---------------|-------------|------------|
| **Vercel** | ✅ Yes | ✅ Yes | ~1 min | ⭐ Easy |
| **Netlify** | ✅ Yes | ✅ Yes | ~1 min | ⭐ Easy |
| **GitHub Pages** | ✅ Yes | ✅ Yes | ~2 min | ⭐⭐ Medium |
| **Own Server** | ❌ No | ✅ Yes | ~30 min | ⭐⭐⭐ Hard |

**Recommendation:** Use Vercel for fastest deployment!

---

## 🎉 After Deployment

### **Test Your Live dApp:**

1. Open your live URL
2. Connect MetaMask
3. Make sure GenLayer network is added to MetaMask:
   - Network Name: GenLayer Studio
   - RPC URL: https://studio.genlayer.com/api
   - Chain ID: 61999 (0xf22f)
   - Currency: GEN

4. Enter contract address (if not default)
5. Deposit tokens
6. Place a bet
7. Settle a bet
8. Verify everything works! ✅

### **Share Your dApp:**

- Share the live URL with friends
- Post on social media
- Add to your portfolio
- Submit to GenLayer showcase (if they have one)

---

## 🐛 Troubleshooting

### **"Contract not found" error:**
- Make sure contract address is correct
- Check MetaMask is on GenLayer network
- Verify contract is deployed in GenLayer Studio

### **MetaMask not connecting:**
- Add GenLayer network to MetaMask
- Refresh page
- Try reconnecting wallet

### **Predictions not showing:**
- Check browser console for errors
- Verify you deployed the FIXED contract (`crypto_prediction_game_historical.py`)
- Make sure contract address is saved

### **Page not loading:**
- Check deployment logs on Vercel/Netlify
- Make sure all files are uploaded
- Check for any build errors

---

## 🚀 Quick Start (TL;DR)

**Fastest way to deploy right now:**

1. Go to https://vercel.com
2. Click "New Project"
3. Drag your project folder
4. Click "Deploy"
5. Done! 🎉

**Your dApp will be live in ~60 seconds!**

---

## 📞 Need Help?

- Vercel Docs: https://vercel.com/docs
- Netlify Docs: https://docs.netlify.com
- GitHub Pages: https://pages.github.com

---

**Ready to deploy?** Choose a platform above and follow the steps! 🚀

**Contract Address:** `0x53eE6AE11F33ff59417de622f3B6474CED3983Ec`
