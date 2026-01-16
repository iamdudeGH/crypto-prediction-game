# v0.1.0 - Real Timestamps Version
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    Crypto Prediction Game with REAL TIMESTAMPS
    Uses gl.message_raw["datetime"] for accurate time tracking
    """
    
    # State variables
    user_balances: TreeMap[str, u256]
    leaderboard: TreeMap[str, u256]
    
    # Predictions
    prediction_symbols: TreeMap[u256, str]
    prediction_directions: TreeMap[u256, str]
    prediction_amounts: TreeMap[u256, u256]
    prediction_entry_prices: TreeMap[u256, u256]
    prediction_creation_time: TreeMap[u256, str]  # ISO datetime string
    prediction_expiry_time: TreeMap[u256, str]    # ISO datetime string
    prediction_owners: TreeMap[u256, str]
    prediction_statuses: TreeMap[u256, str]
    
    next_prediction_id: u256
    
    def __init__(self):
        """Initialize"""
        self.next_prediction_id = 0
    
    def parse_datetime(self, datetime_str: str) -> dict:
        """
        Parse ISO datetime string to components
        Format: 2026-01-16T09:50:33.471071Z
        Returns: {year, month, day, hour, minute, second}
        """
        # Split date and time parts
        parts = datetime_str.replace("Z", "").split("T")
        date_part = parts[0]
        time_part = parts[1]
        
        # Parse date
        date_components = date_part.split("-")
        year = int(date_components[0])
        month = int(date_components[1])
        day = int(date_components[2])
        
        # Parse time
        time_components = time_part.split(":")
        hour = int(time_components[0])
        minute = int(time_components[1])
        second = int(float(time_components[2]))  # Ignore microseconds
        
        return {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second
        }
    
    def datetime_to_seconds(self, datetime_str: str) -> u256:
        """
        Convert ISO datetime to total seconds (more accurate)
        This calculates total seconds since epoch for comparison
        """
        dt = self.parse_datetime(datetime_str)
        
        # More accurate calculation
        # Account for actual days in each month
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Calculate total days
        total_days = 0
        
        # Add days for complete years since 2020
        total_days += (dt["year"] - 2020) * 365
        
        # Add days for complete months in current year
        for m in range(1, dt["month"]):
            total_days += days_in_month[m]
        
        # Add remaining days
        total_days += dt["day"]
        
        # Calculate total seconds
        seconds_today = dt["hour"] * 3600 + dt["minute"] * 60 + dt["second"]
        
        return total_days * 86400 + seconds_today
    
    def is_time_expired(self, expiry_time_str: str, current_time_str: str) -> bool:
        """Check if current time is past expiry time"""
        expiry_seconds = self.datetime_to_seconds(expiry_time_str)
        current_seconds = self.datetime_to_seconds(current_time_str)
        
        return current_seconds >= expiry_seconds
    
    def add_seconds_to_datetime(self, datetime_str: str, seconds_to_add: u256) -> str:
        """
        Add seconds to a datetime string (proper handling)
        Returns new datetime string
        """
        dt = self.parse_datetime(datetime_str)
        
        # Days in each month
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Add seconds
        total_seconds = dt["second"] + seconds_to_add
        
        added_minutes = total_seconds // 60
        new_second = total_seconds % 60
        
        # Add minutes
        total_minutes = dt["minute"] + added_minutes
        added_hours = total_minutes // 60
        new_minute = total_minutes % 60
        
        # Add hours
        total_hours = dt["hour"] + added_hours
        added_days = total_hours // 24
        new_hour = total_hours % 24
        
        # Add days with proper month/year overflow
        new_day = dt["day"] + added_days
        new_month = dt["month"]
        new_year = dt["year"]
        
        # Handle day overflow
        while new_day > days_in_month[new_month]:
            new_day -= days_in_month[new_month]
            new_month += 1
            
            # Handle month overflow
            if new_month > 12:
                new_month = 1
                new_year += 1
        
        # Format back to ISO string
        return f"{new_year}-{new_month:02d}-{new_day:02d}T{new_hour:02d}:{new_minute:02d}:{new_second:02d}Z"
    
    @gl.public.view
    def get_current_time(self) -> str:
        """Get current blockchain time"""
        try:
            return gl.message_raw["datetime"]
        except:
            return "ERROR: datetime not available"
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """Get crypto price with mock variation"""
        crypto_symbol_upper = crypto_symbol.upper()
        
        base_prices = {
            "BTC": 9500000,
            "ETH": 350000,
            "SOL": 15000,
            "DOGE": 35,
            "ADA": 95,
        }
        
        base = base_prices.get(crypto_symbol_upper, 100000)
        
        # Use current time for variation
        try:
            time_str = gl.message_raw["datetime"]
            time_seconds = self.datetime_to_seconds(time_str)
            variation = ((time_seconds * 7919) % 200) - 100
        except:
            variation = 0
        
        price = base + (base * variation // 1000)
        
        return {
            "symbol": crypto_symbol_upper,
            "price_usd_cents": price,
            "source": "mock"
        }
    
    @gl.public.write
    def deposit(self, user_address: str, amount: u256) -> str:
        """Deposit funds"""
        if user_address not in self.user_balances:
            self.user_balances[user_address] = 0
        
        self.user_balances[user_address] += amount
        
        current_time = gl.message_raw["datetime"]
        return f"Deposited {amount}. Balance: {self.user_balances[user_address]} | Time: {current_time}"
    
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
        """Place prediction with real timestamp expiry"""
        if direction.upper() not in ["UP", "DOWN"]:
            return "ERROR: Direction must be UP or DOWN"
        
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. Have {user_balance}, need {bet_amount}"
        
        price_data = self.get_current_price(crypto_symbol)
        
        self.user_balances[user_address] -= bet_amount
        
        prediction_id = self.next_prediction_id
        self.next_prediction_id += 1
        
        # Get current time and calculate expiry
        current_time = gl.message_raw["datetime"]
        expiry_time = self.add_seconds_to_datetime(current_time, duration_seconds)
        
        self.prediction_symbols[prediction_id] = crypto_symbol.upper()
        self.prediction_directions[prediction_id] = direction.upper()
        self.prediction_amounts[prediction_id] = bet_amount
        self.prediction_entry_prices[prediction_id] = price_data["price_usd_cents"]
        self.prediction_creation_time[prediction_id] = current_time
        self.prediction_expiry_time[prediction_id] = expiry_time
        self.prediction_owners[prediction_id] = user_address
        self.prediction_statuses[prediction_id] = "ACTIVE"
        
        price_usd = price_data["price_usd_cents"] / 100.0
        
        return f"Prediction #{prediction_id}: {direction.upper()} on {crypto_symbol.upper()} @ ${price_usd:.2f} | Created: {current_time} | Expires: {expiry_time}"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """Settle prediction using real timestamp"""
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        if self.prediction_statuses[prediction_id] != "ACTIVE":
            return f"ERROR: Already settled"
        
        # Check if time has expired
        current_time = gl.message_raw["datetime"]
        expiry_time = self.prediction_expiry_time[prediction_id]
        
        if not self.is_time_expired(expiry_time, current_time):
            return f"ERROR: Too early! Current: {current_time} | Expires: {expiry_time}"
        
        # Get exit price
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        
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
        
        return f"{result}: {symbol} ${entry_usd:.2f} -> ${exit_usd:.2f} | Payout: {payout} | Balance: {self.user_balances[user_address]} | Settled at: {current_time}"
    
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
        creation_time = self.prediction_creation_time[prediction_id]
        expiry_time = self.prediction_expiry_time[prediction_id]
        
        if status == "ACTIVE":
            try:
                current_time = gl.message_raw["datetime"]
                is_ready = self.is_time_expired(expiry_time, current_time)
                time_status = "READY TO SETTLE" if is_ready else f"Expires: {expiry_time}"
            except:
                time_status = f"Expires: {expiry_time}"
        else:
            time_status = f"Status: {status}"
        
        return f"#{prediction_id}: {direction} {symbol} @ ${entry_price:.2f} | {amount} tokens | Created: {creation_time} | {time_status}"
    
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
    def get_user_active_predictions(self, user_address: str) -> str:
        """Get list of active prediction IDs with details - for frontend display"""
        active_list = []
        
        try:
            current_time = gl.message_raw["datetime"]
        except:
            current_time = "unknown"
        
        for pred_id in self.prediction_owners:
            if self.prediction_owners[pred_id] == user_address:
                status = self.prediction_statuses[pred_id]
                if status == "ACTIVE":
                    symbol = self.prediction_symbols[pred_id]
                    direction = self.prediction_directions[pred_id]
                    amount = self.prediction_amounts[pred_id]
                    entry_price = self.prediction_entry_prices[pred_id] / 100.0
                    expiry = self.prediction_expiry_time[pred_id]
                    
                    # Check if ready
                    is_ready = self.is_time_expired(expiry, current_time) if current_time != "unknown" else False
                    ready_str = "READY" if is_ready else "WAITING"
                    
                    active_list.append(f"{pred_id}|{symbol}|{direction}|{amount}|{entry_price}|{expiry}|{ready_str}")
        
        if len(active_list) == 0:
            return "NONE"
        
        return ";;".join(active_list)
    
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
        total = len(self.prediction_owners)
        players = len(set(self.prediction_owners.values()))
        
        try:
            current_time = gl.message_raw["datetime"]
            return f"Predictions: {total} | Players: {players} | Current Time: {current_time}"
        except:
            return f"Predictions: {total} | Players: {players}"
