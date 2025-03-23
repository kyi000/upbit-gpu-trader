import ccxt
import asyncio
from typing import Dict, List

class UpbitClient:
    def __init__(self, config: Dict):
        self.exchange = ccxt.upbit({
            'apiKey': config['api']['access_key'],
            'secret': config['api']['secret_key'],
            'enableRateLimit': True
        })
        self.config = config
        self.portfolio = {}
    
    async def execute_trade(self, signal: Dict):
        try:
            if signal['action'] == 'buy':
                await self._place_buy_order(signal)
            elif signal['action'] == 'sell':
                await self._place_sell_order(signal)
        except Exception as e:
            logging.error(f"Trade execution error: {e}")
    
    async def update_portfolio(self):
        try:
            balances = self.exchange.fetch_balance()
            self.portfolio = {
                currency: float(balance['total'])
                for currency, balance in balances['total'].items()
                if float(balance['total']) > 0
            }
        except Exception as e:
            logging.error(f"Portfolio update error: {e}")
    
    def get_portfolio_summary(self) -> Dict:
        return {
            'total_value': sum(self.portfolio.values()),
            'positions': self.portfolio
        }
    
    async def _place_buy_order(self, signal: Dict):
        self.exchange.create_market_buy_order(
            symbol=signal['symbol'],
            amount=signal['amount']
        )
    
    async def _place_sell_order(self, signal: Dict):
        self.exchange.create_market_sell_order(
            symbol=signal['symbol'],
            amount=signal['amount']
        )