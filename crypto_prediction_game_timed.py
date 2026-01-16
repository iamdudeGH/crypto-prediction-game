# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Crypto Price Prediction dApp with Time-Based Settlement
    Uses transaction counter to simulate block-based timing
    """
    
    # State variables
    user_balances: TreeMap[str, u256]
    leaderboard: TreeMap[str, u256]
    
    # Active predictions tracking
    prediction_symbols: TreeMap[u256, str]
    prediction_directions: TreeMap[u256, str]
    prediction_amounts: TreeMap[u256, u256]
    prediction_entry_prices: TreeMap[u256, u256]
    prediction_creation_tx: TreeMap[u256, u256]  # Transaction number when created
    prediction_duration_tx: TreeMap[u256, u256]  # How many transactions until expiry
    prediction_owners: TreeMap[u256, str]
    prediction_statuses: TreeMap[u256, str]
    
    next_prediction_id: u256
    transaction_counter: u256  # Increments on every write transaction
    
    def __init__(self):
        """Initialize the game contract"""
        self.next_prediction_id = 0
        self.transaction_counter = 0
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """Fetch crypto price using CryptoCompare API"""
        crypto_symbol_upper = crypto_symbol.upper()
        
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
        
        try:
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
                    "price_usd_cents": int(price_data["price_usd_cents"])
                }
            else:
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": 0,
                    "error": "Failed to fetch"
                }
        except Exception as e:
            return {
                "symbol": crypto_symbol_upper,
                "price_usd_cents": 0,
                "error": str(e)
            }
    
    @gl.public.write
    def deposit(self, user_address: str, amount: u256) -> str:
        """Deposit funds"""
        self.transaction_counter += 1
        
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
        """Place a prediction with time limit"""
        self.transaction_counter += 1
        
        if direction.upper() not in ["UP", "DOWN"]:
            return "ERROR: Direction must be UP or DOWN"
        
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. Have {user_balance}, need {bet_amount}"
        
        price_data = self.get_current_price(crypto_symbol)
        if "error" in price_data:
            return "ERROR: Failed to fetch price"
        
        self.user_balances[user_address] -= bet_amount
        
        prediction_id = self.next_prediction_id
        self.next_prediction_id += 1
        
        # Convert duration to "transaction blocks" (assume 1 tx per 10 seconds)
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
        
        return f"✅ Prediction #{prediction_id}: {direction} on {crypto_symbol} @ ${price_usd:.2f} | Bet: {bet_amount} | Expires after {duration_tx} more transactions (~{duration_seconds}s)"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """Settle prediction - checks if enough transactions have passed"""
        self.transaction_counter += 1
        
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        if self.prediction_statuses[prediction_id] != "ACTIVE":
            return f"ERROR: Already settled"
        
        # Check if enough transactions have passed
        creation_tx = self.prediction_creation_tx[prediction_id]
        duration_tx = self.prediction_duration_tx[prediction_id]
        tx_passed = self.transaction_counter - creation_tx
        
        if tx_passed < duration_tx:
            tx_remaining = duration_tx - tx_passed
            return f"⏳ Too early! Need {tx_remaining} more transactions. Try calling deposit() or other methods to advance time, then settle again."
        
        # Get exit price
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        if "error" in price_data:
            return "ERROR: Failed to fetch exit price"
        
        exit_price = price_data["price_usd_cents"]
        entry_price = self.prediction_entry_prices[prediction_id]
        
        # Determine winner
        price_went_up = exit_price > entry_price
        direction = self.prediction_directions[prediction_id]
        won = price_went_up == (direction == "UP")
        
        bet = self.prediction_amounts[prediction_id]
        
        if won:
            payout = int(bet * 1.8)
            self.user_balances[user_address] += payout
            self.prediction_statuses[prediction_id] = "WON"
            
            if user_address not in self.leaderboard:
                self.leaderboard[user_address] = 0
            self.leaderboard[user_address] += 1
            
            result = "🎉 YOU WON!"
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
            result = "😔 You Lost"
        
        entry_usd = entry_price / 100
        exit_usd = exit_price / 100
        change = ((exit_price - entry_price) / entry_price * 100) if entry_price > 0 else 0
        
        return f"{result}\nEntry: ${entry_usd:.2f} → Exit: ${exit_usd:.2f} ({change:+.1f}%)\nPayout: {payout} tokens | Balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> str:
        """Get prediction details with time remaining"""
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
            
            time_status = f"⏳ {tx_remaining} transactions left" if tx_remaining > 0 else "✅ Ready to settle!"
        else:
            time_status = f"Status: {status}"
        
        return f"Prediction #{prediction_id}: {direction} on {symbol} | ${entry_price:.2f} | {amount} tokens | {time_status} | Owner: {owner[:10]}..."
    
    @gl.public.view
    def get_user_predictions(self, user_address: str) -> str:
        """Get user predictions summary"""
        count = active = won = lost = 0
        
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
        
        return f"Total: {count} (Active: {active}, Won: {won}, Lost: {lost})"
    
    @gl.public.view
    def get_leaderboard(self) -> str:
        """Get leaderboard"""
        if not self.leaderboard:
            return "No winners yet"
        
        result = "🏆 Leaderboard:\n"
        sorted_leaders = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        for i, (user, wins) in enumerate(sorted_leaders[:10], 1):
            result += f"{i}. {user[:10]}... - {wins} wins\n"
        return result
    
    @gl.public.view
    def get_game_stats(self) -> str:
        """Get game stats"""
        total_predictions = len(self.prediction_owners)
        unique_players = len(set(self.prediction_owners.values()))
        total_in_pool = sum(self.user_balances.values())
        
        return f"📊 Stats: {total_predictions} predictions | {unique_players} players | {total_in_pool} tokens in pool | Transaction #{self.transaction_counter}"
    
    @gl.public.write
    def advance_time(self) -> str:
        """Dummy transaction to advance the transaction counter (simulate time passing)"""
        self.transaction_counter += 1
        return f"⏰ Time advanced! Transaction counter now: {self.transaction_counter}"
