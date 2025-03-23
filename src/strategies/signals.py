from typing import Dict, List

class SignalGenerator:
    def __init__(self):
        self.signals = []
    
    def generate_signals(self, analysis: Dict) -> List[Dict]:
        signals = []
        
        # Generate buy signals
        buy_signals = self._generate_buy_signals(analysis)
        signals.extend(buy_signals)
        
        # Generate sell signals
        sell_signals = self._generate_sell_signals(analysis)
        signals.extend(sell_signals)
        
        self.signals = signals
        return signals
    
    def _generate_buy_signals(self, analysis: Dict) -> List[Dict]:
        signals = []
        
        # Volume surge with price increase
        if analysis['volume_surge'].any() and analysis['price_momentum'][-1] > 0:
            signals.append({
                'action': 'buy',
                'reason': 'volume_surge_with_momentum',
                'strength': float(analysis['volume_surge'].max())
            })
        
        # RSI oversold condition
        if analysis['rsi'] < 30:
            signals.append({
                'action': 'buy',
                'reason': 'oversold',
                'strength': float(30 - analysis['rsi'])
            })
        
        # Golden cross
        if analysis['ma_signals']['golden_cross']:
            signals.append({
                'action': 'buy',
                'reason': 'golden_cross',
                'strength': 1.0
            })
        
        return signals
    
    def _generate_sell_signals(self, analysis: Dict) -> List[Dict]:
        signals = []
        
        # RSI overbought condition
        if analysis['rsi'] > 70:
            signals.append({
                'action': 'sell',
                'reason': 'overbought',
                'strength': float(analysis['rsi'] - 70)
            })
        
        # Death cross
        if analysis['ma_signals']['death_cross']:
            signals.append({
                'action': 'sell',
                'reason': 'death_cross',
                'strength': 1.0
            })
        
        return signals