# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Crypto Price Prediction dApp - FIXED VERSION
    No float issues - all conversions happen before consensus
    """
    
    # State variables - using TreeMap
    user_balances: TreeMap[str, u256]
    leaderboard: TreeMap[str, u256]
    
    # Active predictions tracking
    prediction_symbols: TreeMap[u256, str]
    prediction_directions: TreeMap[u256, str]
    prediction_amounts: TreeMap[u256, u256]
    prediction_entry_prices: TreeMap[u256, u256]
    prediction_end_times: TreeMap[u256, u256]
    prediction_owners: TreeMap[u256, str]
    prediction_statuses: TreeMap[u256, str]
    
    next_prediction_id: u256
    
    def __init__(self):
        """Initialize the game contract"""
        self.next_prediction_id = 0
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """
        Fetch crypto price using CryptoCompare API
        Returns ONLY integers to avoid encoding issues
        """
        crypto_symbol_upper = crypto_symbol.upper()
        
        def fetch_and_extract_price() -> dict:
            """Non-deterministic function - returns integers only"""
            url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol_upper}&tsyms=USD"
            
            web_data = gl.nondet.web.render(url, mode="text")
            print(f"Raw API data: {web_data}")
            
            task = f"""
Extract the USD price from this API response and convert to cents (integer).

API Response: {web_data}

Return ONLY this JSON (no markdown, no extra text):
{{"price_cents": <integer>, "success": true}}

Example: If USD price is 95642.50, return {{"price_cents": 9564250, "success": true}}
If the response is {{"USD": 95642.50}}, extract 95642.50 and multiply by 100.

CRITICAL: price_cents must be an INTEGER, not a float.
"""
            
            result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "").strip()
            print(f"AI response: {result}")
            
            parsed = json.loads(result)
            
            # Force conversion to integer
            price_cents = int(float(parsed.get("price_cents", 0)))
            
            return {
                "price_cents": price_cents,
                "success": parsed.get("success", False)
            }
        
        try:
            # Use prompt_comparative for semantic comparison (more flexible for prices)
            def get_price_json():
                data = fetch_and_extract_price()
                return json.dumps(data)
            
            price_json = gl.eq_principle.prompt_comparative(
                get_price_json,
                "The price_usd_cents values should be within 1% of each other"
            )
            price_data = json.loads(price_json)
            
            if price_data.get("success", False):
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": price_data["price_cents"]
                }
            else:
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": 0,
                    "error": "Failed to fetch price"
                }
        except Exception as e:
            print(f"Error: {e}")
            return {
                "symbol": crypto_symbol_upper,
                "price_usd_cents": 0,
                "error": str(e)
            }
    
    @gl.public.write
    def deposit(self, user_address: str, amount: u256) -> str:
        """Deposit funds"""
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
        
        self.prediction_symbols[prediction_id] = crypto_symbol.upper()
        self.prediction_directions[prediction_id] = direction.upper()
        self.prediction_amounts[prediction_id] = bet_amount
        self.prediction_entry_prices[prediction_id] = price_data["price_usd_cents"]
        self.prediction_end_times[prediction_id] = duration_seconds
        self.prediction_owners[prediction_id] = user_address
        self.prediction_statuses[prediction_id] = "ACTIVE"
        
        price_dollars = price_data["price_usd_cents"] / 100
        
        return f"Prediction #{prediction_id}: {direction} on {crypto_symbol} at ${price_dollars:.2f}"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """Settle prediction"""
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        if self.prediction_statuses[prediction_id] != "ACTIVE":
            return f"ERROR: Already settled"
        
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        if "error" in price_data:
            return "ERROR: Failed to fetch exit price"
        
        exit_price = price_data["price_usd_cents"]
        entry_price = self.prediction_entry_prices[prediction_id]
        
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
            
            result_msg = "WON"
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
            result_msg = "LOST"
        
        entry_usd = entry_price / 100
        exit_usd = exit_price / 100
        
        return f"{result_msg} - Entry: ${entry_usd:.2f}, Exit: ${exit_usd:.2f}, Payout: {payout}"
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> str:
        """Get prediction details"""
        if prediction_id not in self.prediction_owners:
            return "ERROR: Not found"
        
        symbol = self.prediction_symbols[prediction_id]
        direction = self.prediction_directions[prediction_id]
        amount = self.prediction_amounts[prediction_id]
        price = self.prediction_entry_prices[prediction_id] / 100
        status = self.prediction_statuses[prediction_id]
        
        return f"#{prediction_id}: {direction} on {symbol} | ${price:.2f} | {amount} tokens | {status}"
    
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
