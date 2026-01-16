# v0.1.0
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Crypto Price Prediction dApp
    Users predict if crypto price will go UP or DOWN in a time window
    
    Using TreeMap for GenLayer storage compatibility
    """
    
    # State variables - using TreeMap (required by GenLayer)
    user_balances: TreeMap[str, u256]
    leaderboard: TreeMap[str, u256]
    
    # Active predictions tracking
    prediction_symbols: TreeMap[u256, str]      # prediction_id -> crypto symbol
    prediction_directions: TreeMap[u256, str]   # prediction_id -> UP/DOWN
    prediction_amounts: TreeMap[u256, u256]     # prediction_id -> bet amount
    prediction_entry_prices: TreeMap[u256, u256]  # prediction_id -> entry price in cents
    prediction_end_times: TreeMap[u256, u256]   # prediction_id -> end timestamp
    prediction_owners: TreeMap[u256, str]       # prediction_id -> user address
    prediction_statuses: TreeMap[u256, str]     # prediction_id -> ACTIVE/WON/LOST
    
    next_prediction_id: u256
    
    def __init__(self):
        """Initialize the game contract"""
        # TreeMaps are automatically initialized by GenLayer
        # Only initialize simple types
        self.next_prediction_id = 0
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """
        Fetch current crypto price from CoinGecko API using GenLayer's non-deterministic web fetching
        Returns: {"symbol": "BTC", "price_usd_cents": 4500000, "timestamp": 1234567890}
        Note: price_usd_cents is in cents (multiply by 100) to avoid float encoding issues
        Uses AI consensus for reliable price extraction
        """
        crypto_symbol_upper = crypto_symbol.upper()
        
        def fetch_and_extract_price():
            """Non-deterministic function to fetch and extract price"""
            # CryptoCompare API - more generous rate limits than CoinGecko
            url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol_upper}&tsyms=USD"
            
            # Use GenLayer's non-deterministic web rendering
            web_data = gl.nondet.web.render(url, mode="text")
            print(f"Fetched data for {crypto_symbol_upper}: {web_data}")
            
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
                    "price_usd_cents": price_cents
                }
            else:
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": 0,
                    "error": price_data.get("error", "Failed to extract price")
                }
        except Exception as e:
            print(f"Error in consensus price fetching: {e}")
            return {
                "symbol": crypto_symbol_upper,
                "price_usd_cents": 0,
                "error": str(e)
            }
    
    @gl.public.write
    def deposit(self, user_address: str, amount: u256) -> str:
        """
        Deposit funds to play the game
        Note: user_address must be passed as parameter (GenLayer doesn't have msg.sender)
        """
        if user_address not in self.user_balances:
            self.user_balances[user_address] = 0
        
        self.user_balances[user_address] += amount
        
        return f"Deposited {amount}. New balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_balance(self, user_address: str) -> u256:
        """
        Get user's balance
        """
        return self.user_balances.get(user_address, 0)
    
    @gl.public.write
    def place_prediction(
        self,
        user_address: str,
        crypto_symbol: str, 
        direction: str,  # "UP" or "DOWN"
        bet_amount: u256,
        duration_seconds: u256 = 60
    ) -> str:
        """
        Place a prediction on crypto price movement
        Returns prediction details with ID
        Note: user_address must be passed as parameter (GenLayer doesn't have msg.sender)
        """
        # Validate direction
        if direction.upper() not in ["UP", "DOWN"]:
            return "ERROR: Direction must be 'UP' or 'DOWN'"
        
        # Check balance
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. You have {user_balance}, need {bet_amount}"
        
        # Get current price
        price_data = self.get_current_price(crypto_symbol)
        if "error" in price_data:
            return "ERROR: Failed to fetch current price"
        
        # Deduct bet amount
        self.user_balances[user_address] -= bet_amount
        
        # Create prediction with simple dict storage
        prediction_id = self.next_prediction_id
        self.next_prediction_id += 1
        
        # Store prediction data in separate dicts
        self.prediction_symbols[prediction_id] = crypto_symbol.upper()
        self.prediction_directions[prediction_id] = direction.upper()
        self.prediction_amounts[prediction_id] = bet_amount
        self.prediction_entry_prices[prediction_id] = price_data["price_usd_cents"]
        # Store duration only - no timestamp available in GenLayer
        self.prediction_end_times[prediction_id] = duration_seconds
        self.prediction_owners[prediction_id] = user_address
        self.prediction_statuses[prediction_id] = "ACTIVE"
        
        price_usd = price_data["price_usd_cents"] / 100.0
        print(f"Prediction placed: ID={prediction_id}, {direction} on {crypto_symbol} at ${price_usd}")
        
        return f"Prediction #{prediction_id} placed: {direction} on {crypto_symbol} at ${price_usd:.2f} for {duration_seconds}s"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """
        Settle a prediction after time expires
        Determines winner and distributes payout
        Note: user_address must be passed as parameter (GenLayer doesn't have msg.sender)
        """
        # Check if prediction exists
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        # Check ownership
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        # Check status
        status = self.prediction_statuses[prediction_id]
        if status != "ACTIVE":
            return f"ERROR: Prediction already settled: {status}"
        
        # Check if time has expired
        end_time = self.prediction_end_times[prediction_id]
        # Note: Without timestamps, settlement is always allowed
        # In production, you'd track block numbers or use external time oracles
        
        # Get current price
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        if "error" in price_data:
            return "ERROR: Failed to fetch exit price"
        
        exit_price_cents = price_data["price_usd_cents"]
        entry_price_cents = self.prediction_entry_prices[prediction_id]
        
        # Determine result
        price_went_up = exit_price_cents > entry_price_cents
        direction = self.prediction_directions[prediction_id]
        user_predicted_up = direction == "UP"
        
        won = price_went_up == user_predicted_up
        
        # Calculate payout (simple 1.8x multiplier for winners)
        bet_amount = self.prediction_amounts[prediction_id]
        if won:
            payout = int(bet_amount * 1.8)
            self.user_balances[user_address] += payout
            self.prediction_statuses[prediction_id] = "WON"
            
            # Update leaderboard
            if user_address not in self.leaderboard:
                self.leaderboard[user_address] = 0
            self.leaderboard[user_address] += 1
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
        
        # Convert cents back to dollars for display
        entry_price_usd = entry_price_cents / 100.0
        exit_price_usd = exit_price_cents / 100.0
        
        result = "WON" if won else "LOST"
        print(f"Prediction settled: {result}, Entry: ${entry_price_usd}, Exit: ${exit_price_usd}, Payout: {payout}")
        
        return f"Settled: {result} - Entry: ${entry_price_usd:.2f}, Exit: ${exit_price_usd:.2f}, Payout: {payout}"
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> str:
        """
        Get details of a specific prediction
        """
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        symbol = self.prediction_symbols[prediction_id]
        direction = self.prediction_directions[prediction_id]
        amount = self.prediction_amounts[prediction_id]
        entry_price_cents = self.prediction_entry_prices[prediction_id]
        end_time = self.prediction_end_times[prediction_id]
        owner = self.prediction_owners[prediction_id]
        status = self.prediction_statuses[prediction_id]
        
        time_left = end_time  # Shows duration since we can't track real time
        entry_price_usd = entry_price_cents / 100.0
        
        return f"Prediction #{prediction_id}: {direction} on {symbol} | Bet: {amount} | Entry: ${entry_price_usd:.2f} | Status: {status} | Time left: {time_left}s | Owner: {owner[:10]}..."
    
    @gl.public.view
    def get_user_predictions(self, user_address: str) -> str:
        """
        Get all predictions for a user (returns count and list)
        """
        # Count predictions for this user
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
        """
        Get top players by wins
        """
        if not self.leaderboard:
            return "No winners yet"
        
        # Format leaderboard as string
        result = "Leaderboard:\n"
        sorted_leaders = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        for i, (user, wins) in enumerate(sorted_leaders[:10], 1):
            result += f"{i}. {user[:10]}... - {wins} wins\n"
        return result
    
    @gl.public.view
    def get_game_stats(self) -> str:
        """
        Get overall game statistics
        """
        total_predictions = len(self.prediction_owners)
        
        # Count unique players
        unique_players = set()
        for owner in self.prediction_owners.values():
            unique_players.add(owner)
        total_players = len(unique_players)
        
        total_in_pool = sum(self.user_balances.values())
        
        return f"Total predictions: {total_predictions}, Total players: {total_players}, Total in pool: {total_in_pool}"
