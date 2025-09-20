#!/usr/bin/env python3
"""
Binance Context Server - Advanced Usage Examples
This script demonstrates advanced features and real-world usage scenarios.
"""

import asyncio
import time
from datetime import datetime, timedelta
from binance_context_server import BinanceClientWrapper


async def portfolio_tracker():
    """Track a portfolio of cryptocurrencies"""
    client = BinanceClientWrapper()
    
    # Define your portfolio (symbol, quantity)
    portfolio = {
        "BTCUSDT": 0.1,  # 0.1 BTC
        "ETHUSDT": 1.0,  # 1.0 ETH
        "BNBUSDT": 10.0, # 10.0 BNB
        "ADAUSDT": 1000.0, # 1000 ADA
    }
    
    print("💼 Portfolio Tracker")
    print("=" * 50)
    
    total_value = 0
    
    for symbol, quantity in portfolio.items():
        try:
            price_data = await client.get_symbol_price(symbol=symbol)
            price = float(price_data['price'])
            value = price * quantity
            
            print(f"{symbol:10s}: {quantity:>8.2f} × ${price:>10,.2f} = ${value:>12,.2f}")
            total_value += value
            
        except Exception as e:
            print(f"{symbol:10s}: Error - {e}")
    
    print("-" * 50)
    print(f"{'TOTAL VALUE':10s}: {'':>8} {'':>10} ${total_value:>12,.2f}")


async def market_scanner():
    """Scan for cryptocurrencies with significant price movements"""
    client = BinanceClientWrapper()
    
    print("\n🔍 Market Scanner - Significant Movers")
    print("=" * 60)
    
    # Get all tickers
    tickers = await client.get_ticker_24hr()
    usdt_pairs = [t for t in tickers if t.symbol.endswith('USDT')]
    
    # Filter for significant moves (>5% change)
    significant_movers = []
    for ticker in usdt_pairs:
        change = float(ticker.priceChangePercent)
        if abs(change) >= 5.0:  # 5% or more change
            significant_movers.append(ticker)
    
    # Sort by absolute change
    significant_movers.sort(key=lambda x: abs(float(x.priceChangePercent)), reverse=True)
    
    print(f"Found {len(significant_movers)} cryptocurrencies with >5% price change:")
    print()
    
    for i, ticker in enumerate(significant_movers[:15], 1):  # Top 15
        change = float(ticker.priceChangePercent)
        price = float(ticker.lastPrice)
        volume = float(ticker.volume)
        
        emoji = "🚀" if change > 10 else "📈" if change > 5 else "📉" if change < -5 else "📊"
        if change < -10:
            emoji = "💥"
        
        print(f"{i:2d}. {emoji} {ticker.symbol:12s} ${price:>10,.4f} {change:+6.2f}% (Vol: {volume:,.0f})")


async def technical_analysis():
    """Perform basic technical analysis on BTC/USDT"""
    client = BinanceClientWrapper()
    
    print("\n📊 Technical Analysis - BTC/USDT")
    print("=" * 50)
    
    # Get 1-hour klines for the last 24 hours
    klines = await client.get_klines(symbol="BTCUSDT", interval="1h", limit=24)
    
    if not klines:
        print("❌ No kline data available")
        return
    
    # Extract OHLCV data
    opens = [float(k[1]) for k in klines]
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]
    closes = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]
    
    # Calculate basic indicators
    current_price = closes[-1]
    highest_24h = max(highs)
    lowest_24h = min(lows)
    
    # Simple Moving Average (24-hour)
    sma_24h = sum(closes) / len(closes)
    
    # Volume analysis
    avg_volume = sum(volumes) / len(volumes)
    current_volume = volumes[-1]
    volume_ratio = current_volume / avg_volume
    
    # Price position in 24h range
    price_position = (current_price - lowest_24h) / (highest_24h - lowest_24h) * 100
    
    # Display analysis
    print(f"Current Price: ${current_price:,.2f}")
    print(f"24h High:      ${highest_24h:,.2f}")
    print(f"24h Low:       ${lowest_24h:,.2f}")
    print(f"SMA (24h):     ${sma_24h:,.2f}")
    print()
    
    print("📈 Technical Indicators:")
    
    # Price vs SMA
    if current_price > sma_24h:
        print(f"✅ Price above SMA: +{((current_price - sma_24h) / sma_24h * 100):.2f}%")
    else:
        print(f"❌ Price below SMA: {((current_price - sma_24h) / sma_24h * 100):.2f}%")
    
    # Price position
    if price_position > 80:
        print(f"🔴 Near resistance: {price_position:.1f}% of 24h range")
    elif price_position < 20:
        print(f"🟢 Near support: {price_position:.1f}% of 24h range")
    else:
        print(f"⚪ Mid-range: {price_position:.1f}% of 24h range")
    
    # Volume analysis
    if volume_ratio > 1.5:
        print(f"📊 High volume: {volume_ratio:.1f}x average")
    elif volume_ratio < 0.5:
        print(f"📊 Low volume: {volume_ratio:.1f}x average")
    else:
        print(f"📊 Normal volume: {volume_ratio:.1f}x average")


async def order_book_analysis():
    """Analyze order book depth and spread"""
    client = BinanceClientWrapper()
    
    print("\n📖 Order Book Analysis - BTC/USDT")
    print("=" * 50)
    
    order_book = await client.get_order_book(symbol="BTCUSDT", limit=20)
    
    # Calculate spread
    best_bid = float(order_book.bids[0][0])
    best_ask = float(order_book.asks[0][0])
    spread = best_ask - best_bid
    spread_percent = (spread / best_bid) * 100
    
    print(f"Best Bid: ${best_bid:,.2f}")
    print(f"Best Ask: ${best_ask:,.2f}")
    print(f"Spread:   ${spread:.2f} ({spread_percent:.4f}%)")
    
    # Analyze depth
    bid_depth = sum(float(bid[1]) for bid in order_book.bids)
    ask_depth = sum(float(ask[1]) for ask in order_book.asks)
    
    print(f"\n📊 Market Depth:")
    print(f"Bid Depth: {bid_depth:.6f} BTC")
    print(f"Ask Depth: {ask_depth:.6f} BTC")
    
    if bid_depth > ask_depth * 1.2:
        print("🟢 More buying pressure")
    elif ask_depth > bid_depth * 1.2:
        print("🔴 More selling pressure")
    else:
        print("⚪ Balanced order book")


async def real_time_monitor():
    """Monitor real-time price changes"""
    client = BinanceClientWrapper()
    
    print("\n⏱️  Real-time Price Monitor")
    print("=" * 50)
    print("Monitoring BTC/USDT, ETH/USDT, BNB/USDT")
    print("Press Ctrl+C to stop")
    print()
    
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    previous_prices = {}
    
    try:
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            
            for symbol in symbols:
                try:
                    price_data = await client.get_symbol_price(symbol=symbol)
                    current_price = float(price_data['price'])
                    
                    if symbol in previous_prices:
                        prev_price = previous_prices[symbol]
                        change = current_price - prev_price
                        change_percent = (change / prev_price) * 100
                        
                        if change > 0:
                            indicator = "🟢"
                        elif change < 0:
                            indicator = "🔴"
                        else:
                            indicator = "⚪"
                        
                        print(f"{current_time} {indicator} {symbol}: ${current_price:,.2f} ({change_percent:+.3f}%)")
                    else:
                        print(f"{current_time} ⚪ {symbol}: ${current_price:,.2f} (initial)")
                    
                    previous_prices[symbol] = current_price
                    
                except Exception as e:
                    print(f"{current_time} ❌ {symbol}: Error - {e}")
            
            print("-" * 50)
            await asyncio.sleep(10)  # Update every 10 seconds
            
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped.")


async def main():
    """Run all examples"""
    print("🚀 Binance Context Server - Advanced Examples")
    print("=" * 60)
    
    try:
        # Run examples
        await portfolio_tracker()
        await market_scanner()
        await technical_analysis()
        await order_book_analysis()
        
        # Ask user if they want real-time monitoring
        print("\n❓ Do you want to start real-time monitoring? (y/n): ", end="")
        # For demo purposes, we'll skip the input and show a brief example
        print("n (skipping for demo)")
        
        # Uncomment the line below to enable real-time monitoring
        # await real_time_monitor()
        
        print("\n✅ All advanced examples completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
