import numpy as np
import torch
from typing import Dict, List

class MarketAnalyzer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.market_data = {}
    
    async def analyze(self, market_data: Dict) -> Dict:
        # Convert market data to tensors for GPU processing
        price_tensor = self._prepare_price_data(market_data)
        volume_tensor = self._prepare_volume_data(market_data)
        
        # Move tensors to GPU
        price_tensor = price_tensor.to(self.device)
        volume_tensor = volume_tensor.to(self.device)
        
        # Perform analysis
        analysis = {
            'price_momentum': self._calculate_momentum(price_tensor),
            'volume_surge': self._detect_volume_surge(volume_tensor),
            'rsi': self._calculate_rsi(price_tensor),
            'ma_signals': self._analyze_moving_averages(price_tensor)
        }
        
        return analysis
    
    def get_market_summary(self) -> Dict:
        return {
            'analyzed_pairs': len(self.market_data),
            'potential_signals': self._count_potential_signals()
        }
    
    def _prepare_price_data(self, market_data: Dict) -> torch.Tensor:
        # Convert price data to tensor
        prices = torch.tensor(market_data['prices'], dtype=torch.float32)
        return prices
    
    def _prepare_volume_data(self, market_data: Dict) -> torch.Tensor:
        # Convert volume data to tensor
        volumes = torch.tensor(market_data['volumes'], dtype=torch.float32)
        return volumes
    
    def _calculate_momentum(self, price_tensor: torch.Tensor) -> torch.Tensor:
        return torch.diff(price_tensor)
    
    def _detect_volume_surge(self, volume_tensor: torch.Tensor) -> torch.Tensor:
        avg_volume = torch.mean(volume_tensor)
        return volume_tensor > (avg_volume * 2)
    
    def _calculate_rsi(self, price_tensor: torch.Tensor, period: int = 14) -> torch.Tensor:
        diff = torch.diff(price_tensor)
        gains = torch.where(diff > 0, diff, torch.zeros_like(diff))
        losses = torch.where(diff < 0, -diff, torch.zeros_like(diff))
        
        avg_gain = torch.mean(gains[-period:])
        avg_loss = torch.mean(losses[-period:])
        
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _analyze_moving_averages(self, price_tensor: torch.Tensor) -> Dict:
        ma_20 = torch.mean(price_tensor[-20:])
        ma_50 = torch.mean(price_tensor[-50:])
        
        return {
            'golden_cross': ma_20 > ma_50,
            'death_cross': ma_20 < ma_50
        }
    
    def _count_potential_signals(self) -> int:
        # Count number of pairs with potential trading signals
        return sum(1 for data in self.market_data.values()
                  if data.get('potential_signal', False))