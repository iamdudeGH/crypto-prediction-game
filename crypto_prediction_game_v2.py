# v2.0.0 - Enhanced Multi-User Crypto Prediction Game (Simplified for GenLayer)
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Multi-User Crypto Price Prediction Game with Time-Based Settlement
    """
    
    # User balances
    user_balances: TreeMap[str, u256]
    
    # Leaderboard tracking
    leaderboard_wins: TreeMap[str, u256]
    leaderboard_profit: TreeMap[str, u256]
    
    # Prediction storage - using prediction_id as key
    prediction_symbols: TreeMap[u256, str]
    prediction_directions: TreeMap[u256, str]
    prediction_amounts: TreeMap[u256, u256]
    prediction_entry_prices: TreeMap[u256, u256]
    prediction_creation_tx: TreeMap[u256, u256]
    prediction_duration_tx: TreeMap[u256, u256]
    prediction_owners: TreeMap[u256, str]
    prediction_statuses: TreeMap[u256, str]
    
    # Global counters
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
        """Fetch crypto price - tries real API, falls back to mock"""
        crypto_symbol_upper = crypto_symbol.upper()
        
        # Try real API
        try:
            def fetch_and_extract_price():
                url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol_upper}&tsyms=USD"
                web_data = gl.nondet.web.render(url, mode="text")
                
                task = f"""
Extract USD price from: {web_data}

Return JSON only:
{{"price_usd_cents": <integer>, "success": true}}

Convert price to cents (multiply by 100). If USD is 95642.50, return 9564250.
"""
                
                result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "").strip()
                parsed = json.loads(result)
                
                # Ensure integer
                if "price_usd" in parsed and "price_usd_cents" not in parsed:
                    parsed["price_usd_cents"] = int(float(parsed["price_usd"]) * 100)
                    del parsed["price_usd"]
                elif "price_usd_cents" in parsed:
                    parsed["price_usd_cents"] = int(parsed["price_usd_cents"])
                
                return parsed
            
            def get_price_json():
                return json.dumps(fetch_and_extract_price())
            
            price_json = gl.eq_principle.prompt_comparative(
                get_price_json,
                "Price values should be within 1% of each other"
            )
            price_data = json.loads(price_json)
            
            if price_data.get("success", False):
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": int(price_data["price_usd_cents"]),
                    "source": "api"
                }
        except:
            pass
        
        # Fallback to mock prices
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
        
        if amount < 100:
            return "ERROR: Minimum deposit is 100 tokens"
        
        if user_address not in self.user_balances:
            self.user_balances[user_address] = 0
        
        self.user_balances[user_address] += amount
        return f"Deposited {amount}. Balance: {self.user_balances[user_address]}"
    
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
        
        if bet_amount < 10:
            return "ERROR: Minimum bet is 10 tokens"
        
        if bet_amount > 10000:
            return "ERROR: Maximum bet is 10000 tokens"
        
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. Have {user_balance}, need {bet_amount}"
        
        price_data = self.get_current_price(crypto_symbol)
        if price_data["price_usd_cents"] == 0:
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
        
        price_usd = price_data["price_usd_cents"] / 100
        potential_win = (bet_amount * 18) // 10
        
        return f"Prediction #{prediction_id}: {direction.upper()} on {crypto_symbol.upper()} @ ${price_usd:.2f} | Bet: {bet_amount} | Win: {potential_win} | Duration: ~{duration_seconds}s ({duration_tx} tx)"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """Settle prediction"""
        self.transaction_counter += 1
        self.price_counter += 1
        
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        if self.prediction_statuses[prediction_id] != "ACTIVE":
            return f"ERROR: Already settled"
        
        creation_tx = self.prediction_creation_tx[prediction_id]
        duration_tx = self.prediction_duration_tx[prediction_id]
        tx_passed = self.transaction_counter - creation_tx
        
        if tx_passed < duration_tx:
            tx_remaining = duration_tx - tx_passed
            return f"Too early! Need {tx_remaining} more transactions. Call advance_time() or make other transactions."
        
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        
        if price_data["price_usd_cents"] == 0:
            return "ERROR: Failed to fetch exit price"
        
        exit_price = price_data["price_usd_cents"]
        entry_price = self.prediction_entry_prices[prediction_id]
        
        price_went_up = exit_price > entry_price
        direction = self.prediction_directions[prediction_id]
        won = (price_went_up and direction == "UP") or (not price_went_up and direction == "DOWN")
        
        bet = self.prediction_amounts[prediction_id]
        
        if won:
            payout = (bet * 18) // 10
            self.user_balances[user_address] += payout
            self.prediction_statuses[prediction_id] = "WON"
            
            if user_address not in self.leaderboard_wins:
                self.leaderboard_wins[user_address] = 0
                self.leaderboard_profit[user_address] = 0
            
            self.leaderboard_wins[user_address] += 1
            self.leaderboard_profit[user_address] += (payout - bet)
            
            result = "YOU WON!"
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
            
            if user_address not in self.leaderboard_profit:
                self.leaderboard_profit[user_address] = 0
            self.leaderboard_profit[user_address] -= bet
            
            result = "You Lost"
        
        entry_usd = entry_price / 100
        exit_usd = exit_price / 100
        change = ((exit_price - entry_price) * 100 / entry_price) if entry_price > 0 else 0
        
        return f"{result} | {symbol}: ${entry_usd:.2f} -> ${exit_usd:.2f} ({change:+.1f}%) | Bet: {bet} | Payout: {payout} | Balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> str:
        """Get prediction details"""
        if prediction_id not in self.prediction_owners:
            return "ERROR: Not found"
        
        symbol = self.prediction_symbols[prediction_id]
        direction = self.prediction_directions[prediction_id]
        amount = self.prediction_amounts[prediction_id]
        entry_price = self.prediction_entry_prices[prediction_id] / 100
        status = self.prediction_statuses[prediction_id]
        owner = self.prediction_owners[prediction_id]
        
        if status == "ACTIVE":
            creation_tx = self.prediction_creation_tx[prediction_id]
            duration_tx = self.prediction_duration_tx[prediction_id]
            tx_passed = self.transaction_counter - creation_tx
            tx_remaining = max(0, duration_tx - tx_passed)
            
            time_status = f"Ready to settle!" if tx_remaining == 0 else f"{tx_remaining} tx left"
        else:
            time_status = f"Status: {status}"
        
        return f"#{prediction_id}: {direction} on {symbol} | ${entry_price:.2f} | {amount} tokens | {time_status} | Owner: {owner[:10]}..."
    
    @gl.public.view
    def get_active_predictions(self, user_address: str) -> str:
        """Get active predictions"""
        active = []
        
        for pred_id in self.prediction_owners:
            if self.prediction_owners[pred_id] != user_address:
                continue
            
            if self.prediction_statuses[pred_id] != "ACTIVE":
                continue
            
            symbol = self.prediction_symbols[pred_id]
            direction = self.prediction_directions[pred_id]
            amount = self.prediction_amounts[pred_id]
            entry_price = self.prediction_entry_prices[pred_id] / 100
            
            creation_tx = self.prediction_creation_tx[pred_id]
            duration_tx = self.prediction_duration_tx[pred_id]
            tx_passed = self.transaction_counter - creation_tx
            tx_remaining = max(0, duration_tx - tx_passed)
            
            ready = "READY" if tx_remaining == 0 else f"{tx_remaining} tx left"
            active.append(f"#{pred_id}: {direction} on {symbol} | ${entry_price:.2f} | {amount} | {ready}")
        
        if not active:
            return "No active predictions"
        
        return "\n".join(active)
    
    @gl.public.view
    def get_user_stats(self, user_address: str) -> str:
        """Get user statistics"""
        balance = self.user_balances.get(user_address, 0)
        wins = self.leaderboard_wins.get(user_address, 0)
        profit = self.leaderboard_profit.get(user_address, 0)
        
        total = active = won = lost = 0
        for pred_id in self.prediction_owners:
            if self.prediction_owners[pred_id] == user_address:
                total += 1
                status = self.prediction_statuses[pred_id]
                if status == "ACTIVE":
                    active += 1
                elif status == "WON":
                    won += 1
                elif status == "LOST":
                    lost += 1
        
        win_rate = (won * 100 // total) if total > 0 else 0
        
        return f"Balance: {balance} | Predictions: {total} (Active: {active}, Won: {won}, Lost: {lost}) | Win Rate: {win_rate}% | Profit: {profit:+d}"
    
    @gl.public.view
    def get_leaderboard(self, sort_by: str = "wins") -> str:
        """Get leaderboard"""
        if sort_by == "profit":
            if not self.leaderboard_profit:
                return "No players yet"
            
            sorted_leaders = sorted(self.leaderboard_profit.items(), key=lambda x: x[1], reverse=True)
            result = "Top Players by Profit:\n"
            for i, (user, profit) in enumerate(sorted_leaders[:10], 1):
                result += f"{i}. {user[:10]}... - {profit:+d} tokens\n"
        else:
            if not self.leaderboard_wins:
                return "No winners yet"
            
            sorted_leaders = sorted(self.leaderboard_wins.items(), key=lambda x: x[1], reverse=True)
            result = "Top Players by Wins:\n"
            for i, (user, wins) in enumerate(sorted_leaders[:10], 1):
                profit = self.leaderboard_profit.get(user, 0)
                result += f"{i}. {user[:10]}... - {wins} wins ({profit:+d} profit)\n"
        
        return result
    
    @gl.public.view
    def get_game_stats(self) -> str:
        """Get game stats"""
        total_predictions = len(self.prediction_owners)
        unique_players = len(set(self.prediction_owners.values()))
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
        
        return f"Total: {total_predictions} predictions | {unique_players} players | {total_in_pool} tokens | Active: {active} | Won: {won} | Lost: {lost} | TX: {self.transaction_counter}"
    
    @gl.public.write
    def advance_time(self) -> str:
        """Advance transaction counter (simulate time passing)"""
        self.transaction_counter += 1
        return f"Time advanced! TX #{self.transaction_counter}"
    
    @gl.public.view
    def get_current_transaction(self) -> u256:
        """Get current transaction counter"""
        return self.transaction_counter
