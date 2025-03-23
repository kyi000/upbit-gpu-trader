import asyncio
import logging
from rich.console import Console
from config.settings import load_config
from core.upbit_client import UpbitClient
from core.websocket import UpbitWebSocket
from strategies.analyzer import MarketAnalyzer
from strategies.signals import SignalGenerator
from strategies.risk_manager import RiskManager

console = Console()

async def main():
    # Load configuration
    config = load_config()
    
    # Initialize components
    upbit = UpbitClient(config)
    websocket = UpbitWebSocket()
    analyzer = MarketAnalyzer()
    signal_gen = SignalGenerator()
    risk_manager = RiskManager(config)
    
    try:
        # Start market data stream
        await websocket.connect()
        
        # Main trading loop
        while True:
            # Process market data
            market_data = await websocket.get_market_data()
            analysis = await analyzer.analyze(market_data)
            signals = signal_gen.generate_signals(analysis)
            
            # Execute trades based on signals and risk management
            for signal in signals:
                if risk_manager.validate_trade(signal):
                    await upbit.execute_trade(signal)
            
            # Update portfolio status
            await upbit.update_portfolio()
            
            # Display status
            console.clear()
            console.print("[bold green]Upbit GPU Trader[/bold green]")
            console.print(upbit.get_portfolio_summary())
            console.print(analyzer.get_market_summary())
            
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        console.print("[yellow]Shutting down...[/yellow]")
    finally:
        await websocket.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())