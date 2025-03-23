import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    
    return {
        'api': {
            'access_key': os.getenv('UPBIT_ACCESS_KEY'),
            'secret_key': os.getenv('UPBIT_SECRET_KEY')
        },
        'trading': {
            'max_coins': 3,
            'max_investment_per_coin': 0.2,  # 20% of total assets
            'daily_loss_limit': 0.02,  # 2% daily loss limit
            'target_profit': 0.01,  # 1% target profit
            'stop_loss': 0.005,  # 0.5% stop loss
            'excluded_coins': ['USDT', 'USDC', 'BTC', 'ETH', 'XRP']
        },
        'analysis': {
            'volume_threshold': 2.0,  # 200% volume increase
            'price_threshold': 0.05,  # 5% price increase
            'rsi_oversold': 30,
            'rsi_overbought': 70
        }
    }