# v0.1.0 - Simple with Time Tracking
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Crypto Price Prediction dApp with Time-Based Settlement
    Uses mock prices for fast consensus
    """
    
    # State variables
    user_balances: TreeMap[str, u256]
    leaderboard: TreeMap[str, u256]
    
    # Predictions
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
        """Get mock crypto price with variation"""
        crypto_symbol_upper = crypto_symbol.upper()
        
        base_prices = {
            "BTC": 9500000,
            "ETH": 350000,
            "SOL": 15000,
            "DOGE": 35,
            "ADA": 95,
        }
        
        base = base_prices.get(crypto_symbol_upper, 100000)
        variation = ((self.price_counter * 7919) % 200) - 100
        price = base + (base * variation // 1000)
        
        return {
            "symbol": crypto_symbol_upper,
            "price_usd_cents": price,
            "source": "mock"
        }
    
    @gl.public.write
    def deposit(self, user_address: str, amount: u256) -> str:
        """Deposit funds"""
        self.transaction_counter += 1
        
        if user_address not in self.user_balances:
            self.user_balances[user_address] = 0
        
        self.user_balances[user_address] += amount
        
        return f"Deposited {amount}. New balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_balance(self, user_address: str) -> u256:
        """Get balance"""
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
        """Place a prediction"""
        self.transaction_counter += 1
        self.price_counter += 1
        
        if direction.upper() not in ["UP", "DOWN"]:
            return "ERROR: Direction must be UP or DOWN"
        
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. You have {user_balance}, need {bet_amount}"
        
        price_data = self.get_current_price(crypto_symbol)
        if "error" in price_data:
            return "ERROR: Failed to fetch price"
        
        self.user_balances[user_address] -= bet_amount
        
        prediction_id = self.next_prediction_id
        self.next_prediction_id += 1
        
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
        
        return f"Prediction #{prediction_id} placed: {direction} on {crypto_symbol} at ${price_usd:.2f} for {duration_seconds}s ({duration_tx} tx)"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """Settle a prediction"""
        self.transaction_counter += 1
        self.price_counter += 1
        
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        status = self.prediction_statuses[prediction_id]
        if status != "ACTIVE":
            return f"ERROR: Already settled: {status}"
        
        creation_tx = self.prediction_creation_tx[prediction_id]
        duration_tx = self.prediction_duration_tx[prediction_id]
        tx_passed = self.transaction_counter - creation_tx
        
        if tx_passed < duration_tx:
            tx_remaining = duration_tx - tx_passed
            return f"ERROR: Too early. Need {tx_remaining} more transactions"
        
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        if "error" in price_data:
            return "ERROR: Failed to fetch exit price"
        
        exit_price_cents = price_data["price_usd_cents"]
        entry_price_cents = self.prediction_entry_prices[prediction_id]
        
        price_went_up = exit_price_cents > entry_price_cents
        direction = self.prediction_directions[prediction_id]
        user_predicted_up = direction == "UP"
        
        won = price_went_up == user_predicted_up
        
        bet_amount = self.prediction_amounts[prediction_id]
        if won:
            payout = int(bet_amount * 18 // 10)
            self.user_balances[user_address] += payout
            self.prediction_statuses[prediction_id] = "WON"
            
            if user_address not in self.leaderboard:
                self.leaderboard[user_address] = 0
            self.leaderboard[user_address] += 1
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
        
        entry_price_usd = entry_price_cents / 100.0
        exit_price_usd = exit_price_cents / 100.0
        
        result = "WON" if won else "LOST"
        
        return f"Settled: {result} - Entry: ${entry_price_usd:.2f}, Exit: ${exit_price_usd:.2f}, Payout: {payout}"
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> str:
        """Get prediction details"""
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
            
            time_status = "Ready to settle!" if tx_remaining == 0 else f"{tx_remaining} tx remaining"
        else:
            time_status = f"Status: {status}"
        
        return f"Prediction #{prediction_id}: {direction} on {symbol} | Bet: {amount} | Entry: ${entry_price_usd:.2f} | {time_status} | Owner: {owner[:10]}..."
    
    @gl.public.view
    def get_user_predictions(self, user_address: str) -> str:
        """Get user predictions summary"""
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
        
        return f"Total: {count} predictions (Active: {active}, Won: {won}, Lost: {lost})"
    
    @gl.public.view
    def get_leaderboard(self) -> str:
        """Get leaderboard"""
        if not self.leaderboard:
            return "No winners yet"
        
        result = "Leaderboard:\n"
        sorted_leaders = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        for i, (user, wins) in enumerate(sorted_leaders[:10], 1):
            result += f"{i}. {user[:10]}... - {wins} wins\n"
        return result
    
    @gl.public.view
    def get_game_stats(self) -> str:
        """Get game stats"""
        total_predictions = len(self.prediction_owners)
        
        unique_players = set()
        for owner in self.prediction_owners.values():
            unique_players.add(owner)
        total_players = len(unique_players)
        
        total_in_pool = sum(self.user_balances.values())
        
        return f"Total predictions: {total_predictions}, Total players: {total_players}, Total in pool: {total_in_pool}, Transaction counter: {self.transaction_counter}"
    
    @gl.public.write
    def advance_time(self) -> str:
        """Advance time by 1 transaction"""
        self.transaction_counter += 1
        return f"Time advanced! Transaction counter: {self.transaction_counter}"
    
    @gl.public.view
    def get_current_transaction(self) -> u256:
        """Get transaction counter"""
        return self.transaction_counter
