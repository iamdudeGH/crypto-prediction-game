# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionSimple(gl.Contract):
    """
    Simplified Crypto Price Prediction Game - Using CryptoCompare API (better rate limits)
    Single-user version that works with GenLayer's current API
    """
    
    # State variables
    balance: u256
    wins: u256
    losses: u256
    
    # Current active prediction
    active_prediction_id: u256
    active_symbol: str
    active_direction: str
    active_amount: u256
    active_entry_price: u256  # Price in cents to avoid float encoding issues
    active_end_time: u256
    active_status: str  # "NONE", "ACTIVE", "WON", "LOST"
    
    next_id: u256
    
    def __init__(self):
        """Initialize the game"""
        self.balance = 0
        self.wins = 0
        self.losses = 0
        self.active_prediction_id = 0
        self.active_symbol = ""
        self.active_direction = ""
        self.active_amount = 0
        self.active_entry_price = 0  # Integer (cents), not float
        self.active_end_time = 0
        self.active_status = "NONE"
        self.next_id = 0
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """
        Fetch current crypto price using CryptoCompare API (better rate limits than CoinGecko)
        Returns price in cents (integer) to avoid float encoding issues
        Uses AI consensus for reliable price extraction
        """
        crypto_symbol_upper = crypto_symbol.upper()
        
        def fetch_and_extract_price():
            """Non-deterministic function to fetch and extract price"""
            # CryptoCompare API - more generous rate limits
            url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol_upper}&tsyms=USD"
            
            # Use GenLayer's non-deterministic web rendering
            web_data = gl.nondet.web.render(url, mode="text")
            print(f"Fetched data: {web_data}")
            
            # Use AI to extract the price reliably
            task = f"""
From the following API response, extract the USD price for {crypto_symbol_upper}.

API Response:
{web_data}

Respond with ONLY a JSON object in this exact format:
{{
    "price_usd_cents": int,
    "success": bool,
    "error": str or null
}}

IMPORTANT: Convert the USD price to cents (multiply by 100 and convert to integer).
For example, if the price is $45000.50, return "price_usd_cents": 4500050.
If you see {{"USD": 45000.50}}, extract 45000.50 and convert to 4500050.
Extract the numeric price value. If the data is not available or invalid, set success to false.
Your response must be valid JSON only, no other text.
"""
            
            result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "").strip()
            print(f"AI extracted: {result}")
            
            parsed = json.loads(result)
            
            # Convert any floats to integers immediately before returning
            if "price_usd" in parsed and "price_usd_cents" not in parsed:
                # AI returned old field name, convert it now
                parsed["price_usd_cents"] = int(float(parsed["price_usd"]) * 100)
                del parsed["price_usd"]  # Remove the float field
            elif "price_usd_cents" in parsed:
                # Ensure it's an integer
                parsed["price_usd_cents"] = int(parsed["price_usd_cents"])
            
            return parsed
        
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
                # Handle both field names and convert to integer
                if "price_usd_cents" in price_data:
                    price_cents = int(price_data["price_usd_cents"])
                elif "price_usd" in price_data:
                    # Fallback: AI returned old field name, convert it
                    price_cents = int(float(price_data["price_usd"]) * 100)
                else:
                    raise ValueError("No price field found in AI response")
                
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": price_cents,
                    "success": True
                }
            else:
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": 0,
                    "success": False,
                    "error": price_data.get("error", "Failed to extract price")
                }
        except Exception as e:
            print(f"Error in consensus price fetching: {e}")
            return {
                "symbol": crypto_symbol_upper,
                "price_usd_cents": 0,
                "success": False,
                "error": str(e)
            }
    
    @gl.public.write
    def deposit(self, amount: u256) -> str:
        """Add tokens to your balance"""
        self.balance += amount
        return f"Deposited {amount}. New balance: {self.balance}"
    
    @gl.public.view
    def get_balance(self) -> u256:
        """Get current balance"""
        return self.balance
    
    @gl.public.view
    def get_stats(self) -> str:
        """Get your game statistics"""
        total = self.wins + self.losses
        win_rate = (self.wins / total * 100) if total > 0 else 0
        return f"Balance: {self.balance} | Wins: {self.wins} | Losses: {self.losses} | Win Rate: {win_rate:.1f}%"
    
    @gl.public.write
    def place_prediction(
        self,
        crypto_symbol: str,
        direction: str,
        bet_amount: u256,
        duration_seconds: u256 = 60
    ) -> str:
        """Place a prediction on crypto price"""
        
        # Check if there's already an active prediction
        if self.active_status == "ACTIVE":
            return "ERROR: You already have an active prediction. Settle it first!"
        
        # Validate direction
        if direction.upper() not in ["UP", "DOWN"]:
            return "ERROR: Direction must be 'UP' or 'DOWN'"
        
        # Check balance
        if self.balance < bet_amount:
            return f"ERROR: Insufficient balance. You have {self.balance}, need {bet_amount}"
        
        # Get current price
        price_data = self.get_current_price(crypto_symbol)
        if not price_data.get("success", False):
            return "ERROR: Failed to fetch current price"
        
        # Deduct bet
        self.balance -= bet_amount
        
        # Store prediction
        prediction_id = self.next_id
        self.next_id += 1
        
        self.active_prediction_id = prediction_id
        self.active_symbol = crypto_symbol.upper()
        self.active_direction = direction.upper()
        self.active_amount = bet_amount
        self.active_entry_price = price_data["price_usd_cents"]
        self.active_end_time = duration_seconds  # Simplified: just store duration
        self.active_status = "ACTIVE"
        
        price_usd = price_data["price_usd_cents"] / 100.0
        print(f"Prediction #{prediction_id}: {direction} on {crypto_symbol} at ${price_usd}")
        
        return f"✅ Prediction #{prediction_id} placed!\n{direction} on {crypto_symbol} @ ${price_usd:.2f}\nBet: {bet_amount} tokens | Duration: {duration_seconds}s"
    
    @gl.public.view
    def get_active_prediction(self) -> str:
        """Get details of your active prediction"""
        if self.active_status == "NONE":
            return "No active prediction"
        
        status_emoji = "🎯" if self.active_status == "ACTIVE" else ("🎉" if self.active_status == "WON" else "😔")
        direction_emoji = "⬆️" if self.active_direction == "UP" else "⬇️"
        entry_price_usd = self.active_entry_price / 100.0
        
        return f"{status_emoji} Prediction #{self.active_prediction_id}\n{direction_emoji} {self.active_direction} on {self.active_symbol}\nEntry: ${entry_price_usd:.2f}\nBet: {self.active_amount}\nStatus: {self.active_status}"
    
    @gl.public.write
    def settle_prediction(self) -> str:
        """Settle your active prediction"""
        
        if self.active_status != "ACTIVE":
            return f"ERROR: No active prediction to settle. Status: {self.active_status}"
        
        # Get current price
        price_data = self.get_current_price(self.active_symbol)
        if not price_data.get("success", False):
            return "ERROR: Failed to fetch exit price"
        
        exit_price_cents = price_data["price_usd_cents"]
        entry_price_cents = self.active_entry_price
        
        # Determine result
        price_went_up = exit_price_cents > entry_price_cents
        predicted_up = self.active_direction == "UP"
        won = price_went_up == predicted_up
        
        # Calculate payout
        if won:
            payout = int(self.active_amount * 1.8)
            self.balance += payout
            self.active_status = "WON"
            self.wins += 1
            result_msg = f"🎉 YOU WON!"
        else:
            payout = 0
            self.active_status = "LOST"
            self.losses += 1
            result_msg = f"😔 You Lost"
        
        # Convert cents to dollars for display
        entry_price_usd = entry_price_cents / 100.0
        exit_price_usd = exit_price_cents / 100.0
        
        price_change = ((exit_price_cents - entry_price_cents) / entry_price_cents * 100) if entry_price_cents > 0 else 0
        price_direction = "📈" if price_went_up else "📉"
        
        details = f"""
{result_msg}
{price_direction} {self.active_symbol}: ${entry_price_usd:.2f} → ${exit_price_usd:.2f} ({price_change:+.2f}%)
Your prediction: {self.active_direction}
Bet: {self.active_amount} tokens
Payout: {payout} tokens
New Balance: {self.balance}
        """.strip()
        
        print(f"Settled: {self.active_status} - Entry: ${entry_price_usd}, Exit: ${exit_price_usd}, Payout: {payout}")
        
        return details
    
    @gl.public.write
    def reset_prediction(self) -> str:
        """Clear the current prediction to start a new one"""
        self.active_status = "NONE"
        return "Ready for a new prediction!"
