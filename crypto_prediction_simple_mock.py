# v0.1.0
# { "Depends": "py-genlayer:test" }

from genlayer import *
import json

class CryptoPredictionSimpleMock(gl.Contract):
    """
    Simplified Crypto Price Prediction Game - MOCK VERSION
    Uses simulated prices for testing until web API is confirmed
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
    active_entry_price: u256  # Price in cents
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
        self.active_entry_price = 0
        self.active_end_time = 0
        self.active_status = "NONE"
        self.next_id = 0
    
    @gl.public.view
    def get_current_price(self, crypto_symbol: str) -> dict:
        """
        Get current crypto price - MOCK VERSION
        Returns simulated prices with small random variation
        """
        # Base mock prices in cents
        base_prices = {
            "BTC": 4500000,  # $45,000.00
            "ETH": 250000,   # $2,500.00
            "SOL": 10000,    # $100.00
            "DOGE": 10,      # $0.10
            "ADA": 50        # $0.50
        }
        
        symbol_upper = crypto_symbol.upper()
        base_price = base_prices.get(symbol_upper, 4500000)
        
        # Add small variation (+/- 2%) using block timestamp for pseudo-randomness
        variation = (gl.block.timestamp % 100) - 50  # -50 to +49
        price_cents = base_price + int(base_price * variation / 2500)
        
        return {
            "symbol": symbol_upper,
            "price_usd_cents": price_cents,
            "success": True
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
        self.active_end_time = duration_seconds
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
