#!/usr/bin/env python3
"""
Binance Context Server - Usage Examples
This script demonstrates how to use the binance-context-server package installed from PyPI.
"""

import asyncio
from binance_context_server import BinanceClientWrapper


async def main():
    """Main usage examples"""
    print("🚀 Binance Context Server Usage Examples")
    print("=" * 50)
    
    # Create Binance client
    client = BinanceClientWrapper()
    
    try:
        # 1. Simple price query
        print("\n1️⃣ Bitcoin price:")
        btc_price = await client.get_symbol_price(symbol="BTCUSDT")
        print(f"   BTC/USDT: ${float(btc_price['price']):,.2f}")
        
        # 2. Ethereum market statistics
        print("\n2️⃣ Ethereum 24h statistics:")
        eth_stats = await client.get_ticker_24hr(symbol="ETHUSDT")
        if eth_stats:
            stats = eth_stats[0]
            print(f"   ETH/USDT: ${float(stats.lastPrice):,.2f}")
            print(f"   24h change: %{float(stats.priceChangePercent):.2f}")
            print(f"   24h volume: {float(stats.volume):,.0f} ETH")
        
        # 3. Top 5 cryptocurrencies
        print("\n3️⃣ Top 5 cryptocurrencies by volume:")
        top_cryptos = await client.get_ticker_24hr()
        # Filter USDT pairs and sort by volume
        usdt_pairs = [crypto for crypto in top_cryptos if crypto.symbol.endswith('USDT')]
        usdt_pairs.sort(key=lambda x: float(x.volume), reverse=True)
        for i, crypto in enumerate(usdt_pairs[:5], 1):
            symbol = crypto.symbol
            volume = float(crypto.volume)
            price = float(crypto.lastPrice)
            print(f"   {i}. {symbol}: ${price:,.2f} (Volume: {volume:,.0f})")
        
        # 4. Order book example
        print("\n4️⃣ BTC/USDT Order Book (first 3 levels):")
        order_book = await client.get_order_book(symbol="BTCUSDT", limit=3)
        print("   Bids (Buy Orders):")
        for bid in order_book.bids[:3]:
            price, qty = float(bid[0]), float(bid[1])
            print(f"     ${price:,.2f} - {qty:.6f} BTC")
        print("   Asks (Sell Orders):")
        for ask in order_book.asks[:3]:
            price, qty = float(ask[0]), float(ask[1])
            print(f"     ${price:,.2f} - {qty:.6f} BTC")
        
        # 5. Recent trades
        print("\n5️⃣ BTC/USDT Last 3 trades:")
        recent_trades = await client.get_recent_trades(symbol="BTCUSDT", limit=3)
        for trade in recent_trades:
            price = float(trade['price'])
            qty = float(trade['qty'])
            is_buyer = trade['isBuyerMaker']
            side = "SELL" if is_buyer else "BUY"
            print(f"   {side}: {qty:.6f} BTC @ ${price:,.2f}")
        
        print("\n✅ All examples executed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Check your internet connection")


if __name__ == "__main__":
    # Use asyncio.run for Python 3.7+
    asyncio.run(main())
