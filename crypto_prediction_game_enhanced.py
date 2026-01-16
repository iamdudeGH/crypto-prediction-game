# v1.0.0 - Enhanced Multi-User Crypto Prediction Game
# { "Depends": "py-genlayer:latest" }

from genlayer import *
import json

class CryptoPredictionGame(gl.Contract):
    """
    🎯 Enhanced Crypto Price Prediction Game
    
    Features:
    - Multi-user support
    - Time-based settlements (transaction counter)
    - Real API integration with fallback
    - Multiple simultaneous predictions per user
    - Leaderboard and comprehensive stats
    - Auto-expiry checking
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
    prediction_statuses: TreeMap[u256, str]  # ACTIVE, WON, LOST, EXPIRED
    
    # Global counters
    next_prediction_id: u256
    transaction_counter: u256
    price_counter: u256  # For mock prices when API fails
    
    # Constants
    PAYOUT_MULTIPLIER: u256 = 18  # 1.8x (stored as 18 to multiply by 10)
    MIN_BET: u256 = 10
    MAX_BET: u256 = 10000
    
    def __init__(self):
        """Initialize the game contract"""
        self.next_prediction_id = 0
        self.transaction_counter = 0
        self.price_counter = 0
        # Note: TreeMaps are not initialized - they're auto-initialized by GenLayer
    
    # ============================================================
    # PRICE FETCHING (Real API + Fallback)
    # ============================================================
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """
        Fetch real crypto price from CryptoCompare API
        Falls back to mock prices if API fails
        """
        crypto_symbol_upper = crypto_symbol.upper()
        
        # Try real API first
        try:
            return self.fetch_real_price(crypto_symbol_upper)
        except Exception as e:
            # Fallback to mock prices
            return self.get_mock_price(crypto_symbol_upper)
    
    def fetch_real_price(self, crypto_symbol: str) -> dict:
        """Fetch real price from CryptoCompare API"""
        def fetch_and_extract_price():
            url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol}&tsyms=USD"
            web_data = gl.nondet.web.render(url, mode="text")
            
            task = f"""
Extract USD price from this API response: {web_data}

Return ONLY valid JSON in this exact format:
{{"price_usd_cents": <integer>, "success": true}}

Convert the price to cents (multiply by 100 and make it an integer).
Example: if USD is 95642.50, return 9564250
"""
            
            result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "").strip()
            parsed = json.loads(result)
            
            # Ensure integer cents
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
                "symbol": crypto_symbol,
                "price_usd_cents": int(price_data["price_usd_cents"]),
                "source": "api"
            }
        else:
            raise Exception("API returned failure")
    
    def get_mock_price(self, crypto_symbol: str) -> dict:
        """Generate mock price with variation (fallback)"""
        # Base prices in cents
        base_prices = {
            "BTC": 9500000,   # $95,000
            "ETH": 350000,    # $3,500
            "SOL": 15000,     # $150
            "DOGE": 35,       # $0.35
            "ADA": 95,        # $0.95
        }
        
        base = base_prices.get(crypto_symbol, 100000)
        
        # Create variation using price_counter
        variation = ((self.price_counter * 7919) % 200) - 100  # -100 to +100
        price = base + (base * variation // 1000)  # ±10% variation
        
        return {
            "symbol": crypto_symbol,
            "price_usd_cents": price,
            "source": "mock"
        }
    
    # ============================================================
    # USER BALANCE MANAGEMENT
    # ============================================================
    
    @gl.public.write
    def deposit(self, user_address: str, amount: u256) -> str:
        """Deposit funds to user balance"""
        self.transaction_counter += 1
        
        if amount < 100:
            return "ERROR: Minimum deposit is 100 tokens"
        
        if user_address not in self.user_balances:
            self.user_balances[user_address] = 0
        
        self.user_balances[user_address] += amount
        return f"✅ Deposited {amount} tokens. New balance: {self.user_balances[user_address]}"
    
    @gl.public.view
    def get_balance(self, user_address: str) -> u256:
        """Get user balance"""
        return self.user_balances.get(user_address, 0)
    
    @gl.public.view
    def get_user_stats(self, user_address: str) -> dict:
        """Get comprehensive user statistics"""
        balance = self.user_balances.get(user_address, 0)
        wins = self.leaderboard_wins.get(user_address, 0)
        profit = self.leaderboard_profit.get(user_address, 0)
        
        # Count predictions
        total = active = won = lost = expired = 0
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
                elif status == "EXPIRED":
                    expired += 1
        
        win_rate = (won * 100 // total) if total > 0 else 0
        
        return {
            "balance": balance,
            "total_predictions": total,
            "active": active,
            "won": won,
            "lost": lost,
            "expired": expired,
            "win_rate_percent": win_rate,
            "total_profit": profit
        }
    
    # ============================================================
    # PREDICTION MANAGEMENT
    # ============================================================
    
    @gl.public.write
    def place_prediction(
        self,
        user_address: str,
        crypto_symbol: str, 
        direction: str,
        bet_amount: u256,
        duration_seconds: u256 = 60
    ) -> str:
        """
        Place a new prediction
        
        Args:
            user_address: User's wallet address
            crypto_symbol: BTC, ETH, SOL, DOGE, ADA
            direction: UP or DOWN
            bet_amount: Amount to bet (min 10)
            duration_seconds: Time until settlement (default 60s)
        """
        self.transaction_counter += 1
        self.price_counter += 1
        
        # Validation
        direction_upper = direction.upper()
        if direction_upper not in ["UP", "DOWN"]:
            return "ERROR: Direction must be UP or DOWN"
        
        if bet_amount < self.MIN_BET:
            return f"ERROR: Minimum bet is {self.MIN_BET} tokens"
        
        if bet_amount > self.MAX_BET:
            return f"ERROR: Maximum bet is {self.MAX_BET} tokens"
        
        user_balance = self.user_balances.get(user_address, 0)
        if user_balance < bet_amount:
            return f"ERROR: Insufficient balance. Have {user_balance}, need {bet_amount}"
        
        # Get current price
        price_data = self.get_current_price(crypto_symbol)
        if "error" in price_data or price_data["price_usd_cents"] == 0:
            return "ERROR: Failed to fetch price. Try again."
        
        # Deduct bet from balance
        self.user_balances[user_address] -= bet_amount
        
        # Create prediction
        prediction_id = self.next_prediction_id
        self.next_prediction_id += 1
        
        # Convert duration to transaction blocks (assume 1 tx per 10 seconds)
        duration_tx = max(1, duration_seconds // 10)
        
        # Store prediction
        self.prediction_symbols[prediction_id] = crypto_symbol.upper()
        self.prediction_directions[prediction_id] = direction_upper
        self.prediction_amounts[prediction_id] = bet_amount
        self.prediction_entry_prices[prediction_id] = price_data["price_usd_cents"]
        self.prediction_creation_tx[prediction_id] = self.transaction_counter
        self.prediction_duration_tx[prediction_id] = duration_tx
        self.prediction_owners[prediction_id] = user_address
        self.prediction_statuses[prediction_id] = "ACTIVE"
        
        price_usd = price_data["price_usd_cents"] / 100
        potential_win = (bet_amount * self.PAYOUT_MULTIPLIER) // 10
        
        return f"✅ Prediction #{prediction_id} placed!\n{direction_upper} on {crypto_symbol.upper()} @ ${price_usd:.2f}\nBet: {bet_amount} tokens | Potential win: {potential_win}\nExpires in ~{duration_seconds}s ({duration_tx} transactions)\nSource: {price_data.get('source', 'unknown')}"
    
    @gl.public.write
    def settle_prediction(self, user_address: str, prediction_id: u256) -> str:
        """
        Settle an active prediction
        Checks if enough time has passed and determines winner
        """
        self.transaction_counter += 1
        self.price_counter += 1
        
        # Validation
        if prediction_id not in self.prediction_owners:
            return "ERROR: Prediction not found"
        
        if self.prediction_owners[prediction_id] != user_address:
            return "ERROR: Not your prediction"
        
        status = self.prediction_statuses[prediction_id]
        if status != "ACTIVE":
            return f"ERROR: Already settled (Status: {status})"
        
        # Check if enough time has passed
        creation_tx = self.prediction_creation_tx[prediction_id]
        duration_tx = self.prediction_duration_tx[prediction_id]
        tx_passed = self.transaction_counter - creation_tx
        
        if tx_passed < duration_tx:
            tx_remaining = duration_tx - tx_passed
            return f"⏳ Too early! Need {tx_remaining} more transactions.\nTip: Call advance_time() or make other transactions to simulate time passing."
        
        # Get exit price
        symbol = self.prediction_symbols[prediction_id]
        price_data = self.get_current_price(symbol)
        
        if "error" in price_data or price_data["price_usd_cents"] == 0:
            return "ERROR: Failed to fetch exit price. Try again."
        
        exit_price = price_data["price_usd_cents"]
        entry_price = self.prediction_entry_prices[prediction_id]
        
        # Determine winner
        price_went_up = exit_price > entry_price
        direction = self.prediction_directions[prediction_id]
        won = (price_went_up and direction == "UP") or (not price_went_up and direction == "DOWN")
        
        bet = self.prediction_amounts[prediction_id]
        
        # Calculate result
        if won:
            payout = (bet * self.PAYOUT_MULTIPLIER) // 10
            self.user_balances[user_address] += payout
            self.prediction_statuses[prediction_id] = "WON"
            
            # Update leaderboard
            if user_address not in self.leaderboard_wins:
                self.leaderboard_wins[user_address] = 0
                self.leaderboard_profit[user_address] = 0
            
            self.leaderboard_wins[user_address] += 1
            profit = payout - bet
            self.leaderboard_profit[user_address] += profit
            
            result_emoji = "🎉"
            result_text = "YOU WON!"
        else:
            payout = 0
            self.prediction_statuses[prediction_id] = "LOST"
            
            # Track losses
            if user_address not in self.leaderboard_profit:
                self.leaderboard_profit[user_address] = 0
            self.leaderboard_profit[user_address] -= bet
            
            result_emoji = "😔"
            result_text = "You Lost"
        
        # Format response
        entry_usd = entry_price / 100
        exit_usd = exit_price / 100
        change_percent = ((exit_price - entry_price) * 100 / entry_price) if entry_price > 0 else 0
        
        return f"""{result_emoji} {result_text}
Prediction #{prediction_id}: {direction} on {symbol}
Entry: ${entry_usd:.2f} → Exit: ${exit_usd:.2f} ({change_percent:+.2f}%)
Bet: {bet} | Payout: {payout} | Profit: {payout - bet:+d}
New Balance: {self.user_balances[user_address]}"""
    
    @gl.public.write
    def settle_all_ready(self, user_address: str) -> str:
        """Auto-settle all ready predictions for a user"""
        self.transaction_counter += 1
        
        settled_count = 0
        results = []
        
        for pred_id in self.prediction_owners:
            if self.prediction_owners[pred_id] != user_address:
                continue
            
            if self.prediction_statuses[pred_id] != "ACTIVE":
                continue
            
            creation_tx = self.prediction_creation_tx[pred_id]
            duration_tx = self.prediction_duration_tx[pred_id]
            tx_passed = self.transaction_counter - creation_tx
            
            if tx_passed >= duration_tx:
                result = self.settle_prediction(user_address, pred_id)
                settled_count += 1
                results.append(f"#{pred_id}: {result[:30]}...")
        
        if settled_count == 0:
            return "No predictions ready to settle"
        
        return f"✅ Settled {settled_count} predictions:\n" + "\n".join(results)
    
    @gl.public.view
    def get_prediction_details(self, prediction_id: u256) -> dict:
        """Get detailed information about a prediction"""
        if prediction_id not in self.prediction_owners:
            return {"error": "Prediction not found"}
        
        symbol = self.prediction_symbols[prediction_id]
        direction = self.prediction_directions[prediction_id]
        amount = self.prediction_amounts[prediction_id]
        entry_price = self.prediction_entry_prices[prediction_id]
        status = self.prediction_statuses[prediction_id]
        owner = self.prediction_owners[prediction_id]
        
        result = {
            "id": prediction_id,
            "symbol": symbol,
            "direction": direction,
            "amount": amount,
            "entry_price_cents": entry_price,
            "entry_price_usd": entry_price / 100,
            "status": status,
            "owner": owner
        }
        
        if status == "ACTIVE":
            creation_tx = self.prediction_creation_tx[prediction_id]
            duration_tx = self.prediction_duration_tx[prediction_id]
            tx_passed = self.transaction_counter - creation_tx
            tx_remaining = max(0, duration_tx - tx_passed)
            
            result["creation_tx"] = creation_tx
            result["duration_tx"] = duration_tx
            result["tx_passed"] = tx_passed
            result["tx_remaining"] = tx_remaining
            result["ready_to_settle"] = tx_remaining == 0
        
        return result
    
    @gl.public.view
    def get_active_predictions(self, user_address: str) -> str:
        """Get all active predictions for a user"""
        active = []
        
        for pred_id in self.prediction_owners:
            if self.prediction_owners[pred_id] != user_address:
                continue
            
            if self.prediction_statuses[pred_id] != "ACTIVE":
                continue
            
            details = self.get_prediction_details(pred_id)
            if "error" not in details:
                ready = "✅ READY" if details.get("ready_to_settle", False) else f"⏳ {details.get('tx_remaining', 0)} tx left"
                active.append(f"#{pred_id}: {details['direction']} on {details['symbol']} | ${details['entry_price_usd']:.2f} | {details['amount']} tokens | {ready}")
        
        if not active:
            return "No active predictions"
        
        return "\n".join(active)
    
    # ============================================================
    # LEADERBOARD & STATS
    # ============================================================
    
    @gl.public.view
    def get_leaderboard(self, sort_by: str = "wins") -> str:
        """
        Get leaderboard sorted by wins or profit
        Args:
            sort_by: "wins" or "profit"
        """
        if sort_by == "profit":
            if not self.leaderboard_profit:
                return "🏆 No players yet"
            
            sorted_leaders = sorted(
                self.leaderboard_profit.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            result = "🏆 Top Players by Profit:\n"
            for i, (user, profit) in enumerate(sorted_leaders[:10], 1):
                result += f"{i}. {user[:10]}... - {profit:+d} tokens\n"
        else:
            if not self.leaderboard_wins:
                return "🏆 No winners yet"
            
            sorted_leaders = sorted(
                self.leaderboard_wins.items(),
                key=lambda x: x[1],
                reverse=True
            )
            result = "🏆 Top Players by Wins:\n"
            for i, (user, wins) in enumerate(sorted_leaders[:10], 1):
                profit = self.leaderboard_profit.get(user, 0)
                result += f"{i}. {user[:10]}... - {wins} wins ({profit:+d} profit)\n"
        
        return result
    
    @gl.public.view
    def get_game_stats(self) -> dict:
        """Get comprehensive game statistics"""
        total_predictions = len(self.prediction_owners)
        unique_players = len(set(self.prediction_owners.values()))
        total_in_pool = sum(self.user_balances.values())
        
        # Count by status
        active = won = lost = expired = 0
        for pred_id in self.prediction_statuses:
            status = self.prediction_statuses[pred_id]
            if status == "ACTIVE":
                active += 1
            elif status == "WON":
                won += 1
            elif status == "LOST":
                lost += 1
            elif status == "EXPIRED":
                expired += 1
        
        return {
            "total_predictions": total_predictions,
            "active_predictions": active,
            "won": won,
            "lost": lost,
            "expired": expired,
            "unique_players": unique_players,
            "total_pool": total_in_pool,
            "transaction_counter": self.transaction_counter
        }
    
    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================
    
    @gl.public.write
    def advance_time(self) -> str:
        """
        Utility function to advance the transaction counter
        Simulates time passing in the blockchain
        """
        self.transaction_counter += 1
        return f"⏰ Time advanced! Transaction #{self.transaction_counter}"
    
    @gl.public.view
    def get_current_transaction(self) -> u256:
        """Get current transaction counter"""
        return self.transaction_counter
