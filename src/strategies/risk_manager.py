from typing import Dict
import logging

class RiskManager:
    def __init__(self, config: Dict):
        self.config = config
        self.daily_pnl = 0.0
        self.positions = {}
    
    def validate_trade(self, signal: Dict) -> bool:
        # Check daily loss limit
        if self.daily_pnl <= -self.config['trading']['daily_loss_limit']:
            logging.warning("Daily loss limit reached")
            return False
        
        # Check maximum number of positions
        if len(self.positions) >= self.config['trading']['max_coins']:
            logging.info("Maximum number of positions reached")
            return False
        
        # Validate position size
        if not self._validate_position_size(signal):
            return False
        
        return True
    
    def update_position(self, trade: Dict):
        symbol = trade['symbol']
        
        if trade['action'] == 'buy':
            self.positions[symbol] = {
                'amount': trade['amount'],
                'price': trade['price']
            }
        elif trade['action'] == 'sell':
            if symbol in self.positions:
                del self.positions[symbol]
    
    def _validate_position_size(self, signal: Dict) -> bool:
        max_position_size = self.config['trading']['max_investment_per_coin']
        
        # Calculate position size as percentage of total assets
        position_size = signal.get('amount', 0) * signal.get('price', 0)
        total_assets = sum(pos['amount'] * pos['price'] for pos in self.positions.values())
        
        if position_size / (total_assets + position_size) > max_position_size:
            logging.info(f"Position size exceeds maximum allowed ({max_position_size*100}%)")
            return False
        
        return True