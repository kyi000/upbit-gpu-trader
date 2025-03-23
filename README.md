# Upbit GPU Trader

High-performance cryptocurrency trading bot for Upbit exchange with GPU acceleration.

## Features

- Real-time market data monitoring via WebSocket
- GPU-accelerated technical analysis using PyTorch
- Advanced trading strategies with risk management
- Real-time portfolio tracking and management
- Beautiful console interface with detailed trading information

## Requirements

- Python 3.10+
- NVIDIA GPU (RTX 3090 recommended)
- CUDA Toolkit 11.8+
- Ubuntu 24.04 (WSL2)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kyi000/upbit-gpu-trader.git
cd upbit-gpu-trader
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file with your Upbit API credentials:
```bash
UPBIT_ACCESS_KEY=your_access_key
UPBIT_SECRET_KEY=your_secret_key
```

## Usage

```bash
python src/main.py
```

## Trading Strategy

- Monitors all available coins (excluding USDT, USDC, BTC, ETH, XRP)
- Updates volatile coins list every hour
- Detects sudden price and volume increases
- Implements risk management with stop-loss and take-profit
- Targets 1% daily profit

## Risk Management

- Maximum 20% investment per coin
- Maximum 3 simultaneous positions
- Dynamic stop-loss based on volatility
- Automatic position closure on system issues

## License

MIT License