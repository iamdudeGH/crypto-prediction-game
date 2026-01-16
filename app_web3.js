// Crypto Prediction Game - Web3 Version with GenLayer SDK
// Full blockchain integration using genlayer-js

import {
    isMetaMaskInstalled,
    connectMetaMask,
    getAccounts,
    isOnGenLayerNetwork,
    switchToGenLayerNetwork,
    formatAddress,
    CONTRACT_ADDRESS,
} from './lib/genlayer/client.js';
import CryptoPredictionGame from './lib/contracts/CryptoPredictionGame.js';

// State
let state = {
    wallet: {
        address: null,
        isConnected: false,
        isOnCorrectNetwork: false,
    },
    contract: null,
    contractAddress: CONTRACT_ADDRESS,
    selectedCrypto: 'BTC',
    balance: 0,
    stats: { total: 0, wins: 0, losses: 0, winRate: 0 },
    activePredictions: [],
    activePredictionIds: [],
    updateTimer: null,
    lastPredictionId: -1, // Track last known prediction ID
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Web3 Crypto Prediction Game Loading...');
    
    // Check MetaMask
    if (!isMetaMaskInstalled()) {
        showBanner('Please install MetaMask to use this dApp');
        updateConnectionStatus('MetaMask Not Installed', 'disconnected');
        return;
    } else {
        // Hide banner by default if MetaMask is installed
        document.getElementById('connectionBanner').classList.add('hidden');
    }
    
    // Load saved contract address
    loadConfig();
    
    // Setup event listeners
    setupEventListeners();
    
    // Setup MetaMask listeners
    setupMetaMaskListeners();
    
    // Hide banner initially if contract is configured
    if (state.contractAddress) {
        document.getElementById('connectionBanner').classList.add('hidden');
    }
    
    // Try auto-connect
    await tryAutoConnect();
    
    console.log('✅ Web3 app initialized');
});

// Load configuration
function loadConfig() {
    // Use hardcoded contract address
    state.contractAddress = CONTRACT_ADDRESS;
    document.getElementById('contractAddress').value = CONTRACT_ADDRESS;
    
    // Hide contract address section (users don't need to see it)
    const contractRow = document.querySelector('.config-row');
    if (contractRow) {
        contractRow.style.display = 'none';
    }
}

// Save configuration
function saveConfig() {
    localStorage.setItem('contractAddress', state.contractAddress);
}

// Setup event listeners
function setupEventListeners() {
    // Save contract address
    document.getElementById('saveContract').addEventListener('click', () => {
        const address = document.getElementById('contractAddress').value.trim();
        if (address) {
            state.contractAddress = address;
            saveConfig();
            showToast('Contract address saved!', 'success');
            // Hide banner after saving
            document.getElementById('connectionBanner').classList.add('hidden');
            if (state.wallet.isConnected) {
                initializeContract();
            }
        }
    });
    
    // Connect wallet button
    document.getElementById('saveAddress').addEventListener('click', connectWallet);
    
    // Add GenLayer network button
    document.getElementById('addNetworkBtn').addEventListener('click', addGenLayerNetwork);
    
    // Crypto selection
    document.getElementById('cryptoSelect').addEventListener('change', (e) => {
        state.selectedCrypto = e.target.value;
        refreshPrice();
    });
    
    // Betting buttons
    document.getElementById('betUp').addEventListener('click', () => placePrediction('UP'));
    document.getElementById('betDown').addEventListener('click', () => placePrediction('DOWN'));
    
    // Refresh buttons
    document.getElementById('refreshPrice').addEventListener('click', refreshPrice);
    document.getElementById('refreshPredictions').addEventListener('click', refreshPredictions);
    document.getElementById('refreshLeaderboard').addEventListener('click', refreshLeaderboard);
    
    // Deposit button
    document.getElementById('depositBtn').addEventListener('click', deposit);
    
    // Banner dismiss
    document.getElementById('dismissBanner').addEventListener('click', () => {
        document.getElementById('connectionBanner').classList.add('hidden');
    });
}

// Setup MetaMask event listeners
function setupMetaMaskListeners() {
    if (!window.ethereum) return;
    
    // Account changed
    window.ethereum.on('accountsChanged', async (accounts) => {
        if (accounts.length === 0) {
            disconnectWallet();
        } else {
            state.wallet.address = accounts[0];
            await initializeContract();
            await updateAllData();
        }
    });
    
    // Chain changed
    window.ethereum.on('chainChanged', async () => {
        window.location.reload();
    });
}

// Try auto-connect
async function tryAutoConnect() {
    try {
        const accounts = await getAccounts();
        if (accounts.length > 0) {
            state.wallet.address = accounts[0];
            state.wallet.isConnected = true;
            
            console.log('🔗 Auto-connecting with address:', state.wallet.address);
            
            // Check network
            const onCorrectNetwork = await isOnGenLayerNetwork();
            state.wallet.isOnCorrectNetwork = onCorrectNetwork;
            
            console.log('✅ Network check result:', onCorrectNetwork);
            
            if (!onCorrectNetwork) {
                showBanner('Please switch to GenLayer network (Chain ID: 61999 / 0xf22f)');
                updateConnectionStatus('Wrong Network', 'disconnected');
                console.error('❌ Wrong network detected. Please switch to GenLayer in MetaMask.');
                return;
            }
            
            // Initialize contract
            await initializeContract();
            
            updateConnectionStatus(`Connected: ${formatAddress(state.wallet.address)}`, 'connected');
            
            // Load data
            await updateAllData();
            
            // Start auto-refresh
            startAutoRefresh();
        }
    } catch (error) {
        console.error('Auto-connect failed:', error);
    }
}

// Add GenLayer network to MetaMask
async function addGenLayerNetwork() {
    if (!isMetaMaskInstalled()) {
        showToast('Please install MetaMask first!', 'error');
        return;
    }
    
    try {
        showToast('Adding GenLayer network to MetaMask...', 'info');
        
        const ethereum = window.ethereum;
        
        // Try to add the network
        await ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [{
                chainId: '0xf22f', // 61999 in hex
                chainName: 'GenLayer Studio',
                nativeCurrency: {
                    name: 'GEN',
                    symbol: 'GEN',
                    decimals: 18
                },
                rpcUrls: ['https://studio.genlayer.com/api'],
                blockExplorerUrls: []
            }]
        });
        
        showToast('✅ GenLayer network added successfully!', 'success');
        
        // Auto-switch to the network
        setTimeout(async () => {
            try {
                await ethereum.request({
                    method: 'wallet_switchEthereumChain',
                    params: [{ chainId: '0xf22f' }]
                });
                showToast('✅ Switched to GenLayer network!', 'success');
            } catch (switchError) {
                console.log('User declined to switch networks');
            }
        }, 500);
        
    } catch (error) {
        console.error('Error adding network:', error);
        
        // Better error messages
        if (error.code === 4902) {
            showToast('Network already exists. Trying to switch...', 'info');
            try {
                await window.ethereum.request({
                    method: 'wallet_switchEthereumChain',
                    params: [{ chainId: '0xf22f' }]
                });
                showToast('✅ Switched to GenLayer network!', 'success');
            } catch (switchError) {
                showToast('Please manually switch to GenLayer network in MetaMask', 'error');
            }
        } else if (error.code === 4001) {
            showToast('You declined the request. Click the button again when ready!', 'info');
        } else if (error.code === -32602) {
            showToast('Network already exists with same RPC. Please switch to Chain ID 61999 in MetaMask.', 'error');
            // Show help modal
            setTimeout(() => {
                document.getElementById('networkHelpModal').classList.remove('hidden');
            }, 2000);
        } else {
            showToast('Click here for manual setup instructions', 'error');
            // Show help modal
            setTimeout(() => {
                document.getElementById('networkHelpModal').classList.remove('hidden');
            }, 2000);
        }
    }
}

// Connect wallet
async function connectWallet() {
    try {
        showToast('Connecting to MetaMask...', 'info');
        
        // Request accounts
        const accounts = await connectMetaMask();
        
        if (accounts.length === 0) {
            throw new Error('No accounts found');
        }
        
        state.wallet.address = accounts[0];
        state.wallet.isConnected = true;
        
        console.log('🔗 Connected to address:', state.wallet.address);
        
        // Check network
        const onCorrectNetwork = await isOnGenLayerNetwork();
        state.wallet.isOnCorrectNetwork = onCorrectNetwork;
        
        console.log('✅ Network check result:', onCorrectNetwork);
        
        if (!onCorrectNetwork) {
            showToast('Switching to GenLayer network...', 'info');
            try {
                await switchToGenLayerNetwork();
                // Verify switch was successful
                const recheckNetwork = await isOnGenLayerNetwork();
                state.wallet.isOnCorrectNetwork = recheckNetwork;
                
                if (!recheckNetwork) {
                    throw new Error('Failed to switch network. Please switch manually to Chain ID 61999 (0xf22f)');
                }
            } catch (switchError) {
                console.error('Network switch failed:', switchError);
                throw new Error('Please manually switch to GenLayer network (Chain ID: 61999 / 0xf22f) in MetaMask');
            }
        }
        
        // Initialize contract
        await initializeContract();
        
        showToast('Wallet connected!', 'success');
        updateConnectionStatus(`Connected: ${formatAddress(state.wallet.address)}`, 'connected');
        
        // Update user address input
        document.getElementById('userAddress').value = state.wallet.address;
        
        // Load data
        await updateAllData();
        
        // Start auto-refresh
        startAutoRefresh();
        
    } catch (error) {
        console.error('Connection error:', error);
        showToast('Failed to connect: ' + error.message, 'error');
    }
}

// Disconnect wallet
function disconnectWallet() {
    state.wallet.address = null;
    state.wallet.isConnected = false;
    state.wallet.isOnCorrectNetwork = false;
    state.contract = null;
    
    if (state.updateTimer) {
        clearInterval(state.updateTimer);
        state.updateTimer = null;
    }
    
    updateConnectionStatus('Disconnected', 'disconnected');
    showToast('Wallet disconnected', 'info');
}

// Initialize contract
async function initializeContract() {
    if (!state.contractAddress) {
        showToast('Please enter contract address', 'error');
        return;
    }
    
    if (!state.wallet.address) {
        showToast('Please connect wallet first', 'error');
        return;
    }
    
    try {
        state.contract = new CryptoPredictionGame(
            state.contractAddress,
            state.wallet.address
        );
        
        // Hide the configuration banner
        document.getElementById('connectionBanner').classList.add('hidden');
        
        console.log('✅ Contract initialized successfully');
    } catch (error) {
        console.error('Contract initialization error:', error);
        showToast('Failed to initialize contract', 'error');
    }
}

// Update all data
async function updateAllData() {
    if (!state.contract) return;
    
    try {
        await Promise.all([
            refreshBalance(),
            refreshPrice(),
            refreshPredictions(),
            refreshStats(),
            refreshLeaderboard()
        ]);
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

// Refresh balance
async function refreshBalance() {
    if (!state.contract || !state.wallet.address) return;
    
    try {
        const balance = await state.contract.getBalance(state.wallet.address);
        
        // Handle BigInt
        const balanceNum = typeof balance === 'bigint' ? Number(balance) : Number(balance);
        state.balance = balanceNum;
        
        document.getElementById('userBalance').textContent = balanceNum;
    } catch (error) {
        console.error('Error fetching balance:', error);
    }
}

// Refresh price with animation
async function refreshPrice() {
    if (!state.contract) return;
    
    try {
        const priceData = await state.contract.getCurrentPrice(state.selectedCrypto);
        
        // Handle different return formats
        let price, source, symbol;
        
        // Check if it's a Map (GenLayer returns dicts as Maps)
        if (priceData instanceof Map) {
            const priceCents = priceData.get('price_usd_cents');
            source = priceData.get('source');
            symbol = priceData.get('symbol');
            
            // Convert BigInt to Number (divide by 100 for cents to dollars)
            price = Number(priceCents) / 100;
            
            // Add animation to price element
            const priceElement = document.getElementById('currentPrice');
            priceElement.style.animation = 'none';
            setTimeout(() => {
                priceElement.style.animation = 'priceUpdate 0.5s ease-out';
            }, 10);
        } else if (typeof priceData === 'object' && priceData !== null) {
            // If it's a plain object with price_usd_cents property
            if (priceData.price_usd_cents !== undefined) {
                price = Number(priceData.price_usd_cents) / 100;
                source = priceData.source || 'unknown';
                symbol = priceData.symbol;
            } else {
                console.error('❌ priceData object missing price_usd_cents:', priceData);
                document.getElementById('currentPrice').textContent = 'Invalid data format';
                return;
            }
        } else if (typeof priceData === 'string') {
            // If it's a string, try to parse it as JSON
            try {
                const parsed = JSON.parse(priceData);
                price = Number(parsed.price_usd_cents) / 100;
                source = parsed.source || 'unknown';
                symbol = parsed.symbol;
            } catch (parseError) {
                console.error('❌ Failed to parse price data string:', priceData);
                document.getElementById('currentPrice').textContent = 'Parse error';
                return;
            }
        } else {
            console.error('❌ Unexpected priceData type:', typeof priceData, priceData);
            document.getElementById('currentPrice').textContent = 'Unknown format';
            return;
        }
        
        if (isNaN(price)) {
            console.error('❌ Price is NaN. priceData was:', priceData);
            document.getElementById('currentPrice').textContent = 'Invalid price';
            return;
        }
        
        document.getElementById('cryptoSymbol').textContent = symbol || state.selectedCrypto;
        document.getElementById('currentPrice').textContent = `$${price.toFixed(2)}`;
        document.getElementById('lastUpdate').textContent = `Updated: ${new Date().toLocaleTimeString()} | Source: ${source}`;
    } catch (error) {
        console.error('❌ Error fetching price:', error);
        document.getElementById('currentPrice').textContent = 'Error: ' + error.message;
    }
}

// Place prediction
async function placePrediction(direction) {
    if (!state.contract) {
        showToast('Please initialize contract first', 'error');
        return;
    }
    
    if (!state.wallet.isConnected) {
        showToast('Please connect wallet first', 'error');
        return;
    }
    
    const betAmount = parseInt(document.getElementById('betAmount').value);
    const duration = parseInt(document.getElementById('duration').value);
    
    if (!betAmount || betAmount < 10) {
        showToast('Minimum bet is 10 tokens', 'error');
        return;
    }
    
    try {
        showToast('Placing prediction...', 'info');
        
        console.log('🎲 Calling placePrediction with:', {
            address: state.wallet.address,
            crypto: state.selectedCrypto,
            direction: direction,
            amount: betAmount,
            duration: duration
        });
        
        const result = await state.contract.placePrediction(
            state.wallet.address,
            state.selectedCrypto,
            direction,
            betAmount,
            duration
        );
        
        console.log('📝 Prediction result:', result);
        console.log('📝 Result data:', result?.data);
        console.log('📝 Result consensus_data:', result?.consensus_data);
        
        // Extract prediction ID from result if possible
        // Result format: "Prediction #0: UP on BTC @ $95000.00 | ..."
        const idMatch = result?.toString().match(/Prediction #(\d+)/);
        if (idMatch) {
            const predictionId = parseInt(idMatch[1]);
            state.lastPredictionId = Math.max(state.lastPredictionId, predictionId);
            console.log('📝 Prediction ID:', predictionId, '| Will auto-settle in', duration, 'seconds');
            
            showToast(`Prediction #${predictionId} placed! ${direction} on ${state.selectedCrypto} | Auto-settle in ${duration}s`, 'success');
        } else {
            showToast(`Prediction placed! ${direction} on ${state.selectedCrypto}`, 'success');
        }
        
        // Refresh data
        await updateAllData();
        
    } catch (error) {
        console.error('Error placing prediction:', error);
        showToast('Failed to place prediction: ' + error.message, 'error');
    }
}

// Settle prediction with win/loss animation
async function settlePrediction(predictionId) {
    if (!state.contract) return;
    
    try {
        showToast('Settling prediction...', 'info');
        
        console.log('🎯 Settling prediction #' + predictionId);
        const result = await state.contract.settlePrediction(state.wallet.address, predictionId);
        
        console.log('🎯 Settlement result object:', result);
        console.log('🎯 Settlement result.data:', result?.data);
        console.log('🎯 Settlement result.data.calldata:', result?.data?.calldata);
        console.log('🎯 Settlement consensus_data:', result?.consensus_data);
        console.log('🎯 Settlement leader_receipt:', result?.consensus_data?.leader_receipt);
        console.log('🎯 Settlement leader_receipt[0]:', result?.consensus_data?.leader_receipt?.[0]);
        console.log('🎯 Settlement leader_receipt[1]:', result?.consensus_data?.leader_receipt?.[1]);
        
        // Try to extract the actual message from the result
        let resultStr = '';
        if (result?.consensus_data?.leader_receipt?.[0]) {
            const receipt = result.consensus_data.leader_receipt[0];
            console.log('🎯 Leader receipt (index 0):', receipt);
            console.log('🎯 Leader genvm_result:', receipt?.genvm_result);
            console.log('🎯 Leader genvm_result.data:', receipt?.genvm_result?.data);
            
            // Extract from genvm_result
            if (receipt?.genvm_result?.data) {
                resultStr = String(receipt.genvm_result.data);
            } else if (receipt?.genvm_result?.result) {
                resultStr = String(receipt.genvm_result.result);
            } else if (receipt?.result) {
                resultStr = String(receipt.result);
            } else {
                resultStr = String(receipt);
            }
        } else if (result?.data?.calldata?.result) {
            resultStr = String(result.data.calldata.result);
        } else {
            resultStr = String(result);
        }
        
        console.log('🎯 Extracted settlement message:', resultStr);
        
        // Check if won or lost
        const isWin = resultStr.includes('WON') || resultStr.includes('won');
        const isLoss = resultStr.includes('LOST') || resultStr.includes('lost');
        
        if (isWin) {
            showToast('🎉 YOU WON! Congrats!', 'success');
            triggerConfetti();
        } else if (isLoss) {
            showToast('😔 You lost. Better luck next time!', 'error');
        } else {
            showToast('Prediction settled!', 'success');
        }
        
        // Refresh data
        await updateAllData();
        
    } catch (error) {
        console.error('Error settling prediction:', error);
        showToast('Failed to settle: ' + error.message, 'error');
    }
}

// Trigger confetti effect for wins
function triggerConfetti() {
    const colors = ['#667eea', '#764ba2', '#38ef7d', '#11998e', '#ffd700', '#ff6a00'];
    const confettiCount = 80;
    
    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.width = Math.random() * 10 + 5 + 'px';
            confetti.style.height = Math.random() * 10 + 5 + 'px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.left = Math.random() * window.innerWidth + 'px';
            confetti.style.top = '-20px';
            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '9999';
            confetti.style.opacity = '1';
            
            document.body.appendChild(confetti);
            
            const duration = 2000 + Math.random() * 1500;
            const xMovement = (Math.random() - 0.5) * 400;
            const rotation = Math.random() * 720;
            
            confetti.animate([
                { 
                    transform: 'translateY(0) translateX(0) rotate(0deg)',
                    opacity: 1
                },
                { 
                    transform: `translateY(${window.innerHeight + 50}px) translateX(${xMovement}px) rotate(${rotation}deg)`,
                    opacity: 0
                }
            ], {
                duration: duration,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            });
            
            setTimeout(() => {
                confetti.remove();
            }, duration);
        }, i * 20);
    }
}

// Refresh predictions
async function refreshPredictions() {
    if (!state.contract || !state.wallet.address) return;
    
    try {
        const summary = await state.contract.getUserPredictions(state.wallet.address);
        const activePredictions = await state.contract.getUserActivePredictions(state.wallet.address);
        
        console.log('📊 Summary:', summary);
        console.log('📋 Active Predictions:', activePredictions);
        
        const container = document.getElementById('activePredictions');
        
        if (summary.includes('No predictions')) {
            container.innerHTML = '<p class="empty-state">No predictions. Place a bet to start!</p>';
            return;
        }
        
        // Parse summary: "Total: X | Active: Y | Won: Z | Lost: W"
        const activeMatch = summary.match(/Active:\s*(\d+)/);
        const activeCount = activeMatch ? parseInt(activeMatch[1]) : 0;
        
        let html = `
            <div class="prediction-summary">
                <div style="background: #f0f4ff; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <p style="margin: 0; font-size: 14px; color: #333;">${summary}</p>
                </div>
        `;
        
        // Show active predictions with settle buttons
        if (activeCount > 0 && activePredictions !== 'NONE' && activePredictions) {
            // Handle different data formats
            let predictionsArray = [];
            
            if (typeof activePredictions === 'string') {
                predictionsArray = activePredictions.split(';;');
            } else if (Array.isArray(activePredictions)) {
                predictionsArray = activePredictions;
            } else {
                console.error('❌ Unexpected activePredictions format:', typeof activePredictions, activePredictions);
            }
            
            console.log('🔍 Parsed predictions array:', predictionsArray);
            
            if (predictionsArray.length > 0) {
                html += `<div style="background: #fff; border: 2px solid #667eea; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                    <h4 style="margin: 0 0 15px 0; color: #667eea;">⏰ Active Predictions (${predictionsArray.length})</h4>`;
                
                // Fetch current prices for all symbols in parallel
                const symbolsSet = new Set();
                predictionsArray.forEach(pred => {
                    if (pred && pred.trim()) {
                        const parts = pred.split('|');
                        if (parts[1]) symbolsSet.add(parts[1]);
                    }
                });
                
                const pricePromises = {};
                for (const symbol of symbolsSet) {
                    pricePromises[symbol] = state.contract.getCurrentPrice(symbol).catch(err => {
                        console.error(`Error fetching price for ${symbol}:`, err);
                        return null;
                    });
                }
                
                const prices = {};
                for (const symbol in pricePromises) {
                    const priceData = await pricePromises[symbol];
                    if (priceData) {
                        if (priceData instanceof Map) {
                            prices[symbol] = Number(priceData.get('price_usd_cents')) / 100;
                        } else if (priceData.price_usd_cents) {
                            prices[symbol] = Number(priceData.price_usd_cents) / 100;
                        }
                    }
                }
                
                console.log('💰 Current prices:', prices);
                
                for (const pred of predictionsArray) {
                    if (!pred || pred.trim() === '') continue;
                    
                    const parts = pred.split('|');
                    console.log('🔍 Prediction parts:', parts);
                    
                    const [id, symbol, direction, amount, entryPrice, expiry, ready] = parts;
                    const isReady = ready === 'READY';
                    const expiryTime = expiry ? new Date(expiry).toLocaleString() : 'Unknown';
                    
                    const entryPriceNum = parseFloat(entryPrice);
                    const currentPrice = prices[symbol];
                    const betAmount = parseInt(amount);
                    const potentialPayout = Math.floor(betAmount * 1.8);
                    
                    // Calculate if winning or losing
                    let winLoseStatus = '';
                    let winLoseColor = '#666';
                    let priceChange = '';
                    let priceChangeColor = '#666';
                    
                    if (currentPrice && isReady) {
                        const priceChangeAmount = currentPrice - entryPriceNum;
                        const priceChangePercent = ((priceChangeAmount / entryPriceNum) * 100).toFixed(2);
                        const priceWentUp = currentPrice > entryPriceNum;
                        
                        if (priceWentUp) {
                            priceChange = `📈 $${entryPriceNum.toFixed(2)} → $${currentPrice.toFixed(2)} (+${priceChangePercent}%)`;
                            priceChangeColor = '#28a745';
                        } else if (currentPrice < entryPriceNum) {
                            priceChange = `📉 $${entryPriceNum.toFixed(2)} → $${currentPrice.toFixed(2)} (${priceChangePercent}%)`;
                            priceChangeColor = '#dc3545';
                        } else {
                            priceChange = `➡️ $${entryPriceNum.toFixed(2)} → $${currentPrice.toFixed(2)} (No change)`;
                            priceChangeColor = '#ffc107';
                        }
                        
                        const isWinning = (priceWentUp && direction === 'UP') || (!priceWentUp && currentPrice < entryPriceNum && direction === 'DOWN');
                        
                        if (isWinning) {
                            winLoseStatus = `🎉 WINNING! You'll get ${potentialPayout} tokens`;
                            winLoseColor = '#28a745';
                        } else {
                            winLoseStatus = `😔 LOSING... You'll lose ${betAmount} tokens`;
                            winLoseColor = '#dc3545';
                        }
                    } else if (currentPrice && !isReady) {
                        const priceChangeAmount = currentPrice - entryPriceNum;
                        const priceChangePercent = ((priceChangeAmount / entryPriceNum) * 100).toFixed(2);
                        
                        if (currentPrice > entryPriceNum) {
                            priceChange = `📈 Currently $${currentPrice.toFixed(2)} (+${priceChangePercent}%)`;
                            priceChangeColor = '#28a745';
                        } else if (currentPrice < entryPriceNum) {
                            priceChange = `📉 Currently $${currentPrice.toFixed(2)} (${priceChangePercent}%)`;
                            priceChangeColor = '#dc3545';
                        } else {
                            priceChange = `➡️ Currently $${currentPrice.toFixed(2)} (No change)`;
                            priceChangeColor = '#666';
                        }
                    }
                    
                    html += `
                        <div style="background: ${isReady ? '#fff3cd' : '#f8f9fa'}; border: 2px solid ${isReady ? '#ffc107' : '#dee2e6'}; border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                                <div style="flex: 1; min-width: 200px;">
                                    <div style="font-weight: 600; font-size: 16px; color: #333;">
                                        #${id}: ${direction === 'UP' ? '⬆️' : '⬇️'} ${direction} on ${symbol}
                                    </div>
                                    <div style="font-size: 13px; color: #666; margin-top: 5px;">
                                        Entry: $${entryPriceNum.toFixed(2)} | Bet: ${betAmount} tokens
                                    </div>
                                    ${priceChange ? `
                                        <div style="font-size: 13px; color: ${priceChangeColor}; margin-top: 5px; font-weight: 600;">
                                            ${priceChange}
                                        </div>
                                    ` : ''}
                                    ${winLoseStatus ? `
                                        <div style="font-size: 14px; color: ${winLoseColor}; margin-top: 5px; font-weight: 700; padding: 5px 10px; background: ${winLoseColor}22; border-radius: 5px; display: inline-block;">
                                            ${winLoseStatus}
                                        </div>
                                    ` : ''}
                                    <div style="font-size: 12px; color: #999; margin-top: 5px;">
                                        ${isReady ? '✅ Ready to settle!' : `⏳ Expires: ${expiryTime}`}
                                    </div>
                                </div>
                                <button onclick="window.settlePrediction(${id})" 
                                        ${!isReady ? 'disabled' : ''}
                                        style="padding: 10px 20px; background: ${isReady ? '#ffc107' : '#6c757d'}; color: ${isReady ? '#000' : '#fff'}; border: none; border-radius: 5px; font-weight: 600; cursor: ${isReady ? 'pointer' : 'not-allowed'}; white-space: nowrap; opacity: ${isReady ? '1' : '0.6'};">
                                    ${isReady ? '🎯 Settle Now' : '⏳ Not Ready'}
                                </button>
                            </div>
                        </div>
                    `;
                }
                
                html += `</div>`;
            }
        } else if (activeCount > 0) {
            // We have active predictions but couldn't parse them
            html += `
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <p style="margin: 0; font-size: 14px; color: #856404;">
                        ⚠️ You have ${activeCount} active prediction(s), but we couldn't load the details. 
                        Try refreshing or check the browser console for errors.
                    </p>
                </div>
            `;
        }
        
        html += `
                <button class="refresh-btn" onclick="window.refreshPredictions()" style="margin-top: 10px;">
                    🔄 Refresh Status
                </button>
            </div>
        `;
        
        container.innerHTML = html;
    } catch (error) {
        console.error('❌ Error fetching predictions:', error);
        const container = document.getElementById('activePredictions');
        container.innerHTML = `
            <div style="background: #f8d7da; padding: 15px; border-radius: 8px;">
                <p style="margin: 0; color: #721c24;">
                    ❌ Error loading predictions: ${error.message}
                </p>
                <button class="refresh-btn" onclick="window.refreshPredictions()" style="margin-top: 10px;">
                    🔄 Try Again
                </button>
            </div>
        `;
    }
}

// Refresh stats
async function refreshStats() {
    if (!state.contract || !state.wallet.address) return;
    
    try {
        const summary = await state.contract.getUserPredictions(state.wallet.address);
        
        // Parse: "Total: X | Active: Y | Won: Z | Lost: W"
        const parseValue = (str, key) => {
            const match = str.match(new RegExp(key + ':\\s*(\\d+)'));
            return match ? parseInt(match[1]) : 0;
        };
        
        const total = parseValue(summary, 'Total');
        const wins = parseValue(summary, 'Won');
        const losses = parseValue(summary, 'Lost');
        const winRate = total > 0 ? Math.floor((wins / total) * 100) : 0;
        
        document.getElementById('statTotal').textContent = total;
        document.getElementById('statWins').textContent = wins;
        document.getElementById('statLosses').textContent = losses;
        document.getElementById('statWinRate').textContent = winRate + '%';
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

// Refresh leaderboard
async function refreshLeaderboard() {
    if (!state.contract) return;
    
    try {
        const leaderboardText = await state.contract.getLeaderboard();
        const container = document.getElementById('leaderboard');
        
        if (leaderboardText.includes('No winners')) {
            container.innerHTML = '<p class="empty-state">No winners yet. Be the first!</p>';
        } else {
            // Parse and display leaderboard
            const lines = leaderboardText.split('\n').filter(l => l.trim());
            let html = '<div class="leaderboard-items">';
            
            lines.forEach(line => {
                if (line.includes('.')) {
                    const isYou = state.wallet.address && line.includes(state.wallet.address.substring(0, 10));
                    html += `<div class="leaderboard-item ${isYou ? 'highlight' : ''}">${line}</div>`;
                }
            });
            
            html += '</div>';
            container.innerHTML = html;
        }
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
    }
}

// Deposit
async function deposit() {
    if (!state.contract) {
        showToast('Please initialize contract first', 'error');
        return;
    }
    
    const amount = parseInt(document.getElementById('depositAmount').value);
    
    if (!amount || amount < 100) {
        showToast('Minimum deposit is 100 tokens', 'error');
        return;
    }
    
    try {
        showToast('Depositing tokens...', 'info');
        
        await state.contract.deposit(state.wallet.address, amount);
        
        showToast(`Deposited ${amount} tokens!`, 'success');
        
        await refreshBalance();
        
    } catch (error) {
        console.error('Error depositing:', error);
        showToast('Failed to deposit: ' + error.message, 'error');
    }
}

// Start auto-refresh
function startAutoRefresh() {
    if (state.updateTimer) {
        clearInterval(state.updateTimer);
    }
    
    state.updateTimer = setInterval(async () => {
        if (state.wallet.isConnected && state.contract) {
            await updateAllData();
        }
    }, 10000); // Every 10 seconds
}

// Update connection status
function updateConnectionStatus(text, status) {
    const badge = document.getElementById('contractStatus');
    badge.textContent = text;
    badge.className = 'status-badge status-' + status;
}

// Show banner
function showBanner(message) {
    document.getElementById('bannerMessage').textContent = message;
    document.getElementById('connectionBanner').classList.remove('hidden');
}

// Show toast
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    
    // Clear any existing timeout
    if (toast.timeoutId) {
        clearTimeout(toast.timeoutId);
    }
    
    toast.textContent = message;
    toast.className = 'toast toast-' + type + ' show';
    
    // Auto-dismiss after 3 seconds
    toast.timeoutId = setTimeout(() => {
        toast.classList.remove('show');
        toast.timeoutId = null;
    }, 3000);
}

// Make functions available globally for onclick
window.settlePrediction = settlePrediction;
window.refreshPredictions = refreshPredictions;

// Debug function to check contract state
window.debugContract = async function() {
    if (!state.contract || !state.wallet.address) {
        console.log('❌ Contract not initialized or wallet not connected');
        return;
    }
    
    console.log('=== CONTRACT DEBUG INFO ===');
    console.log('Contract Address:', state.contractAddress);
    console.log('Wallet Address:', state.wallet.address);
    console.log('Balance:', state.balance);
    
    try {
        // Try to get prediction details for ID 0
        console.log('\n--- Testing getPredictionDetails(0) ---');
        const details = await state.contract.getPredictionDetails(0);
        console.log('Prediction 0:', details);
        
        // Try to get user predictions
        console.log('\n--- Testing getUserPredictions ---');
        const summary = await state.contract.getUserPredictions(state.wallet.address);
        console.log('Summary:', summary);
        
        // Try to get active predictions
        console.log('\n--- Testing getUserActivePredictions ---');
        const active = await state.contract.getUserActivePredictions(state.wallet.address);
        console.log('Active Predictions:', active);
        
        // Try to get game stats
        console.log('\n--- Testing getGameStats ---');
        const stats = await state.contract.getGameStats();
        console.log('Game Stats:', stats);
        
        console.log('\n=== END DEBUG INFO ===');
    } catch (error) {
        console.error('❌ Error during debug:', error);
    }
};

console.log('✅ Web3 dApp loaded!');
console.log('📝 Using genlayer-js SDK for blockchain interaction');
console.log('🔗 Connect MetaMask to start playing!');
console.log('🔧 Debug: Run debugContract() in console to check contract state');
