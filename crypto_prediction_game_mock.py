# v0.1.0 - Mock Prices Only (Fast & Reliable)
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Crypto Price Prediction dApp with Time-Based Settlement
    Uses MOCK prices for fast, reliable testing (no API calls)
    """
    
    # State variables - using TreeMap
    user_balances: TreeMap[str, u256]
    leaderboard: TreeMap[str, u256]
    
    # Active predictions tracking
    prediction_symbols: TreeMap[u256, str]
    prediction_directions: TreeMap[u256, str]
    prediction_amounts: TreeMap[u256, u256]
    prediction_entry_prices: TreeMap[u256, u256]
    prediction_creation_tx: TreeMap[u256, u256]
    prediction_duration_tx: TreeMap[u256, u256]
    prediction_owners: TreeMap[u256, str]
    prediction_statuses: TreeMap[u256, str]
    
    next_prediction_id: u256
    transaction_counter: u256
    price_counter: u256
    
    def __init__(self):
        """Initialize the game contract"""
        self.next_prediction_id = 0
        self.transaction_counter = 0
        self.price_counter = 0
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """
        Get mock crypto price with realistic variation
        No API calls = fast and reliable consensus
        """
        crypto_symbol_upper = crypto_symbol.upper()
        
        # Base prices in cents
        base_prices = {
            "BTC": 9500000,   # $95,000
            "ETH": 350000,    # $3,500
            "SOL": 15000,     # $150
            "DOGE": 35,       # $0.35
            "ADA": 95,        # $0.95
            "MATIC": 85,      # $0.85
            "AVAX": 3500,     # $35.00
            "DOT": 650,       # $6.50
            "LINK": 1500,     # $15.00
            "UNI": 900,       # $9.00
        }
        
        base = base_prices.get(crypto_symbol_upper, 100000)
        
        # Create realistic variation using price_counter
        # This gives ±10% variation that changes with each call
        variation = ((self.price_counter * 7919) % 200) - 100  # -100 to +100
        price = base + (base * variation // 1000)
        
        return {
            "symbol": crypto_symbol_upper,
            "price_usd_cents": price,
            "source": "mock"
        }
    
    @gl.public.write
    def deposit(self, user_address: str, amount: u256) -> str:
        """Deposit funds to play the game"""
        self.transaction_counter += 1
        
        if user_address not in self.user_balances:
            self.user_balances[user_address] = 0
        
        self.user_balances[user_address] += amount
        
        return f"Deposited {amount}. New balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_balance(self, user_address: str) -> u256:
        """Get user's balance"""
        return self.user_balances.get(user_address, 0)
    
    @gl.public.write
    def place_prediction(
        self,
        user_address: str,
        crypto_symbol: str, 
        direction: str,
        bet_amount: u256,
        duration_seconds: u256 = 60
    ) -> str:
        """Place a prediction on crypto price movement with time limit"""
        self.transaction_counter += 1
        self.price_counter += 1
        
        if direction.upper() not in ["UP", "DOWN"]:
            return "ERROR: Direction must be 'UP' or 'DOWN'"
        
        if bet_amount < 10:
            return "ERROR: Minimum bet is 10 tokens"
        
        if bet_amount > 10000:
            return "ERROR: Maximum bet is 10000 tokens"
        
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. You have {user_balance}, need {bet_amount}"
        
        price_data = self.get_current_price(crypto_symbol)
        if price_data["price_usd_cents"] == 0:
            return "ERROR: Failed to fetch current price"
        
        self.user_balances[user_address] -= bet_amount
        
        prediction_id = self.next_prediction_id
        self.next_prediction_id += 1
        
        # Convert duration to transaction blocks (1 tx = ~10 seconds)
        duration_tx = max(1, duration_seconds // 10)
        
        self.prediction_symbols[prediction_id] = crypto_symbol.upper()
        self.prediction_directions[prediction_id] = direction.upper()
        self.prediction_amounts[prediction_id] = bet_amount
        self.prediction_entry_prices[prediction_id] = price_data["price_usd_cents"]
        self.prediction_creation_tx[prediction_id] = self.transaction_counter
        self.prediction_duration_tx[prediction_id] = duration_tx
        self.prediction_owners[prediction_id] = user_address
        self.prediction_statuses[prediction_id] = "ACTIVE"
        
        price_usd = price_data["price_usd_cents"] / 100.0
        potential_win = (bet_amount * 18) // 10
        
        return f"Prediction #{prediction_id} placed! {direction.upper()} on {crypto_symbol.upper()} @ ${price_usd:.2f} | Bet: {bet_amount} | Potential Win: {potential_win} | Expires in {duration_tx} tx (~{duration_seconds}s) | Balance: {self.user_balances[user_address]}"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """Settle a prediction after time expires"""
        self.transaction_counter += 1
        self.price_counter += 1
        
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        status = self.prediction_statuses[prediction_id]
        if status != "ACTIVE":
            return f"ERROR: Already settled as {status}"
        
        # Check if enough time has passed
        creation_tx = self.prediction_creation_tx[prediction_id]
        duration_tx = self.prediction_duration_tx[prediction_id]
        tx_passed = self.transaction_counter - creation_tx
        
        if tx_passed < duration_tx:
            tx_remaining = duration_tx - tx_passed
            return f"Too early! Need {tx_remaining} more transactions. Call advance_time() {tx_remaining} times or make other transactions."
        
        # Get exit price
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        
        exit_price_cents = price_data["price_usd_cents"]
        entry_price_cents = self.prediction_entry_prices[prediction_id]
        
        # Determine result
        price_went_up = exit_price_cents > entry_price_cents
        direction = self.prediction_directions[prediction_id]
        won = (price_went_up and direction == "UP") or (not price_went_up and direction == "DOWN")
        
        # Calculate payout (1.8x multiplier)
        bet_amount = self.prediction_amounts[prediction_id]
        if won:
            payout = (bet_amount * 18) // 10
            self.user_balances[user_address] += payout
            self.prediction_statuses[prediction_id] = "WON"
            
            # Update leaderboard
            if user_address not in self.leaderboard:
                self.leaderboard[user_address] = 0
            self.leaderboard[user_address] += 1
            
            result_text = "YOU WON!"
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
            result_text = "You Lost"
        
        entry_price_usd = entry_price_cents / 100.0
        exit_price_usd = exit_price_cents / 100.0
        price_change = exit_price_cents - entry_price_cents
        price_change_pct = (price_change * 100 / entry_price_cents) if entry_price_cents > 0 else 0
        profit = payout - bet_amount
        
        return f"{result_text} | {symbol}: ${entry_price_usd:.2f} -> ${exit_price_usd:.2f} ({price_change_pct:.2f}%) | Bet: {bet_amount} | Payout: {payout} | Profit: {profit} | Balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> str:
        """Get details of a specific prediction"""
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        symbol = self.prediction_symbols[prediction_id]
        direction = self.prediction_directions[prediction_id]
        amount = self.prediction_amounts[prediction_id]
        entry_price_cents = self.prediction_entry_prices[prediction_id]
        owner = self.prediction_owners[prediction_id]
        status = self.prediction_statuses[prediction_id]
        
        entry_price_usd = entry_price_cents / 100.0
        
        if status == "ACTIVE":
            creation_tx = self.prediction_creation_tx[prediction_id]
            duration_tx = self.prediction_duration_tx[prediction_id]
            tx_passed = self.transaction_counter - creation_tx
            tx_remaining = max(0, duration_tx - tx_passed)
            
            if tx_remaining == 0:
                time_status = "READY TO SETTLE!"
            else:
                time_status = f"{tx_remaining} tx remaining"
        else:
            time_status = f"Status: {status}"
        
        return f"Prediction #{prediction_id}: {direction} on {symbol} | Entry: ${entry_price_usd:.2f} | Bet: {amount} tokens | {time_status} | Owner: {owner[:10]}..."
    
    @gl.public.view
    def get_active_predictions(self, user_address: str) -> str:
        """Get all active predictions for a user"""
        active = []
        
        for pred_id in self.prediction_owners:
            if self.prediction_owners[pred_id] != user_address:
                continue
            
            if self.prediction_statuses[pred_id] != "ACTIVE":
                continue
            
            symbol = self.prediction_symbols[pred_id]
            direction = self.prediction_directions[pred_id]
            amount = self.prediction_amounts[pred_id]
            
            creation_tx = self.prediction_creation_tx[pred_id]
            duration_tx = self.prediction_duration_tx[pred_id]
            tx_passed = self.transaction_counter - creation_tx
            tx_remaining = max(0, duration_tx - tx_passed)
            
            status = "READY" if tx_remaining == 0 else f"{tx_remaining} tx"
            active.append(f"#{pred_id}: {direction} on {symbol} | {amount} tokens | {status}")
        
        if not active:
            return "No active predictions"
        
        return "\n".join(active)
    
    @gl.public.view
    def get_user_predictions(self, user_address: str) -> str:
        """Get all predictions for a user"""
        count = 0
        active = 0
        won = 0
        lost = 0
        
        for pred_id in self.prediction_owners:
            if self.prediction_owners[pred_id] == user_address:
                count += 1
                status = self.prediction_statuses[pred_id]
                if status == "ACTIVE":
                    active += 1
                elif status == "WON":
                    won += 1
                elif status == "LOST":
                    lost += 1
        
        if count == 0:
            return "No predictions found"
        
        win_rate = (won * 100 // count) if count > 0 else 0
        return f"Total: {count} predictions | Active: {active} | Won: {won} | Lost: {lost} | Win Rate: {win_rate}%"
    
    @gl.public.view
    def get_leaderboard(self) -> str:
        """Get top players by wins"""
        if not self.leaderboard:
            return "No winners yet"
        
        result = "Leaderboard:\n"
        sorted_leaders = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        for i, (user, wins) in enumerate(sorted_leaders[:10], 1):
            result += f"{i}. {user[:10]}... - {wins} wins\n"
        return result
    
    @gl.public.view
    def get_game_stats(self) -> str:
        """Get overall game statistics"""
        total_predictions = len(self.prediction_owners)
        
        unique_players = set()
        for owner in self.prediction_owners.values():
            unique_players.add(owner)
        total_players = len(unique_players)
        
        total_in_pool = sum(self.user_balances.values())
        
        active = won = lost = 0
        for pred_id in self.prediction_statuses:
            status = self.prediction_statuses[pred_id]
            if status == "ACTIVE":
                active += 1
            elif status == "WON":
                won += 1
            elif status == "LOST":
                lost += 1
        
        return f"Game Stats: {total_predictions} predictions | {total_players} players | {total_in_pool} tokens in pool | Active: {active} | Won: {won} | Lost: {lost} | TX: {self.transaction_counter}"
    
    @gl.public.write
    def advance_time(self) -> str:
        """Advance transaction counter by 1 (simulate time passing)"""
        self.transaction_counter += 1
        return f"Time advanced! Current TX: {self.transaction_counter}"
    
    @gl.public.view
    def get_current_transaction(self) -> u256:
        """Get current transaction counter"""
        return self.transaction_counter
