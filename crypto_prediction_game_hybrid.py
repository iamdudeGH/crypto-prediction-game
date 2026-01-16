# v0.1.0 - Hybrid: Real API + Smart Caching
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Crypto Prediction Game with Smart Price Caching
    - Uses real API prices when available
    - Caches prices to avoid consensus delays during gameplay
    - Falls back to mock prices when API fails
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
    
    # Price cache (stores last known prices)
    cached_prices: TreeMap[str, u256]
    price_timestamps: TreeMap[str, u256]
    
    next_prediction_id: u256
    transaction_counter: u256
    price_counter: u256
    
    def __init__(self):
        """Initialize"""
        self.next_prediction_id = 0
        self.transaction_counter = 0
        self.price_counter = 0
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """
        Get current crypto price - tries real API first
        This is a VIEW function so it's fast and doesn't need consensus
        """
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

Convert to cents (multiply by 100).
"""
                
                result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "").strip()
                parsed = json.loads(result)
                
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
                price_cents = int(price_data["price_usd_cents"])
                
                return {
                    "symbol": crypto_symbol_upper,
                    "price_usd_cents": price_cents,
                    "source": "api"
                }
        except Exception as e:
            print(f"API fetch failed: {e}")
        
        # Fallback to mock
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
    def update_price_cache(self, crypto_symbol: str) -> str:
        """
        Manually update the price cache with real API data
        Call this periodically to refresh prices
        """
        self.transaction_counter += 1
        
        price_data = self.get_current_price(crypto_symbol)
        symbol = crypto_symbol.upper()
        
        self.cached_prices[symbol] = price_data["price_usd_cents"]
        self.price_timestamps[symbol] = self.transaction_counter
        
        price_usd = price_data["price_usd_cents"] / 100.0
        return f"Updated {symbol}: ${price_usd:.2f} (source: {price_data.get('source', 'unknown')})"
    
    def get_price_for_gameplay(self, crypto_symbol: str) -> dict:
        """
        Internal: Get price for gameplay (uses cache if available)
        Avoids consensus delays during active gameplay
        """
        symbol = crypto_symbol.upper()
        
        # Check if we have a cached price
        if symbol in self.cached_prices:
            cached_price = self.cached_prices[symbol]
            cached_at = self.price_timestamps.get(symbol, 0)
            age = self.transaction_counter - cached_at
            
            # Use cached price if it's recent (within 100 transactions)
            if age < 100:
                return {
                    "symbol": symbol,
                    "price_usd_cents": cached_price,
                    "source": f"cache (age: {age} tx)"
                }
        
        # No cache or too old, use current price
        return self.get_current_price(symbol)
    
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
        """Place prediction using cached price (fast!)"""
        self.transaction_counter += 1
        self.price_counter += 1
        
        if direction.upper() not in ["UP", "DOWN"]:
            return "ERROR: Direction must be UP or DOWN"
        
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. Have {user_balance}, need {bet_amount}"
        
        # Use cached price for fast gameplay
        price_data = self.get_price_for_gameplay(crypto_symbol)
        
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
        
        # Also update cache for next time
        self.cached_prices[crypto_symbol.upper()] = price_data["price_usd_cents"]
        self.price_timestamps[crypto_symbol.upper()] = self.transaction_counter
        
        price_usd = price_data["price_usd_cents"] / 100.0
        
        return f"Prediction #{prediction_id}: {direction.upper()} on {crypto_symbol.upper()} @ ${price_usd:.2f} | Bet: {bet_amount} | Expires: {duration_tx} tx | Source: {price_data.get('source', 'unknown')}"
    
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
            return f"ERROR: Too early. Need {duration_tx - tx_passed} more tx"
        
        # Use cached price for settlement (also fast)
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_price_for_gameplay(symbol)
        
        exit_price_cents = price_data["price_usd_cents"]
        entry_price_cents = self.prediction_entry_prices[prediction_id]
        
        price_went_up = exit_price_cents > entry_price_cents
        direction = self.prediction_directions[prediction_id]
        won = (price_went_up and direction == "UP") or (not price_went_up and direction == "DOWN")
        
        bet_amount = self.prediction_amounts[prediction_id]
        if won:
            payout = (bet_amount * 18) // 10
            self.user_balances[user_address] += payout
            self.prediction_statuses[prediction_id] = "WON"
            
            if user_address not in self.leaderboard:
                self.leaderboard[user_address] = 0
            self.leaderboard[user_address] += 1
            
            result = "WON"
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
            result = "LOST"
        
        entry_usd = entry_price_cents / 100.0
        exit_usd = exit_price_cents / 100.0
        
        return f"{result}: {symbol} ${entry_usd:.2f} -> ${exit_usd:.2f} | Payout: {payout} | Balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> str:
        """Get prediction details"""
        if prediction_id not in self.prediction_owners:
            return "ERROR: Not found"
        
        symbol = self.prediction_symbols[prediction_id]
        direction = self.prediction_directions[prediction_id]
        amount = self.prediction_amounts[prediction_id]
        entry_price = self.prediction_entry_prices[prediction_id] / 100.0
        status = self.prediction_statuses[prediction_id]
        
        if status == "ACTIVE":
            creation_tx = self.prediction_creation_tx[prediction_id]
            duration_tx = self.prediction_duration_tx[prediction_id]
            tx_remaining = max(0, duration_tx - (self.transaction_counter - creation_tx))
            time_status = "READY" if tx_remaining == 0 else f"{tx_remaining} tx left"
        else:
            time_status = status
        
        return f"#{prediction_id}: {direction} {symbol} @ ${entry_price:.2f} | {amount} tokens | {time_status}"
    
    @gl.public.view
    def get_user_predictions(self, user_address: str) -> str:
        """Get user summary"""
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
        
        if total == 0:
            return "No predictions"
        
        return f"Total: {total} | Active: {active} | Won: {won} | Lost: {lost}"
    
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
        return f"Predictions: {len(self.prediction_owners)} | Players: {len(set(self.prediction_owners.values()))} | TX: {self.transaction_counter}"
    
    @gl.public.write
    def advance_time(self) -> str:
        """Advance time"""
        self.transaction_counter += 1
        return f"Time advanced! TX: {self.transaction_counter}"
    
    @gl.public.view
    def get_current_transaction(self) -> u256:
        """Get TX counter"""
        return self.transaction_counter
    
    @gl.public.view
    def get_cached_price(self, crypto_symbol: str) -> str:
        """Check cached price"""
        symbol = crypto_symbol.upper()
        if symbol not in self.cached_prices:
            return f"{symbol}: Not cached yet"
        
        price_cents = self.cached_prices[symbol]
        cached_at = self.price_timestamps.get(symbol, 0)
        age = self.transaction_counter - cached_at
        price_usd = price_cents / 100.0
        
        return f"{symbol}: ${price_usd:.2f} (cached {age} tx ago)"
