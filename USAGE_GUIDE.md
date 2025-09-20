# 🚀 Binance Context Server - Usage Guide

Learn how to use the `binance-context-server` package installed from PyPI!

## 📦 Installation

```bash
pip install binance-context-server
```

## 🎯 3 Different Usage Methods

### 1️⃣ **As Python Module** (Recommended)

```python
from binance_context_server import BinanceClientWrapper
import asyncio

async def main():
    # Create client
    client = BinanceClientWrapper()
    
    # Get Bitcoin price
    btc_price = await client.get_symbol_price(symbol="BTCUSDT")
    print(f"BTC: ${float(btc_price['price']):,.2f}")
    
    # Get market statistics
    stats = await client.get_ticker_24hr(symbol="ETHUSDT")
    if stats:
        eth = stats[0]
        print(f"ETH: ${float(eth.lastPrice):,.2f}")
        print(f"24h change: %{float(eth.priceChangePercent):.2f}")

# Run
asyncio.run(main())
```

### 2️⃣ **As MCP Server**

```python
from binance_context_server import main
import asyncio

# Start MCP server
asyncio.run(main())
```

### 3️⃣ **Command Line Usage**

```bash
# On Windows (full path required)
"C:\Users\USERNAME\AppData\Roaming\Python\Python313\Scripts\binance-context-server.exe"

# On Linux/Mac
binance-context-server
```

---

## 🔧 Available API Methods

### 📊 **Market Data**
- `get_symbol_price(symbol)` - Single symbol price
- `get_ticker_24hr(symbol=None)` - 24-hour statistics
- `get_order_book(symbol, limit=100)` - Order book data
- `get_klines(symbol, interval, limit)` - Candlestick data
- `get_avg_price(symbol)` - Average price

### 📈 **Trading Data**
- `get_recent_trades(symbol, limit=100)` - Recent trades
- `get_historical_trades(symbol, limit=100)` - Historical trades
- `get_price_change_statistics(symbols)` - Price change statistics

### 💰 **Account Data** (Requires API Key)
- `get_account_balance()` - Account balance

### 🔍 **Info & Search**
- `get_exchange_info(symbol=None)` - Exchange information
- `get_symbol_info(symbol)` - Symbol details
- `get_server_time()` - Server time

---

## 💡 **Practical Usage Examples**

### Example 1: Simple Price Tracking

```python
import asyncio
from binance_context_server import BinanceClientWrapper

async def track_prices():
    client = BinanceClientWrapper()
    
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT"]
    
    for symbol in symbols:
        price_data = await client.get_symbol_price(symbol=symbol)
        price = float(price_data['price'])
        print(f"{symbol}: ${price:,.2f}")

asyncio.run(track_prices())
```

### Example 2: Market Analysis

```python
import asyncio
from binance_context_server import BinanceClientWrapper

async def analyze_market():
    client = BinanceClientWrapper()
    
    # Get top 10 coins by volume
    tickers = await client.get_ticker_24hr()
    usdt_pairs = [t for t in tickers if t.symbol.endswith('USDT')]
    usdt_pairs.sort(key=lambda x: float(x.volume), reverse=True)
    
    print("📊 Top 10 USDT Pairs by Volume:")
    for i, ticker in enumerate(usdt_pairs[:10], 1):
        change = float(ticker.priceChangePercent)
        emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
        print(f"{i:2d}. {emoji} {ticker.symbol:12s} ${float(ticker.lastPrice):>10,.2f} (%{change:+.2f})")

asyncio.run(analyze_market())
```

### Example 3: Order Book Analysis

```python
import asyncio
from binance_context_server import BinanceClientWrapper

async def analyze_orderbook():
    client = BinanceClientWrapper()
    
    order_book = await client.get_order_book(symbol="BTCUSDT", limit=10)
    
    print("📈 BTC/USDT Order Book Analysis:")
    print("\n🟢 Bids (Buy Orders):")
    total_bid_volume = 0
    for i, bid in enumerate(order_book.bids[:5], 1):
        price, qty = float(bid[0]), float(bid[1])
        total_bid_volume += qty
        print(f"  {i}. ${price:,.2f} - {qty:.6f} BTC")
    
    print("\n🔴 Asks (Sell Orders):")
    total_ask_volume = 0
    for i, ask in enumerate(order_book.asks[:5], 1):
        price, qty = float(ask[0]), float(ask[1])
        total_ask_volume += qty
        print(f"  {i}. ${price:,.2f} - {qty:.6f} BTC")
    
    print(f"\n📊 Total Bid Volume: {total_bid_volume:.6f} BTC")
    print(f"📊 Total Ask Volume: {total_ask_volume:.6f} BTC")

asyncio.run(analyze_orderbook())
```

### Example 4: Real-time Trade Tracking

```python
import asyncio
import time
from binance_context_server import BinanceClientWrapper

async def track_recent_trades():
    client = BinanceClientWrapper()
    
    print("🔄 BTC/USDT Recent Trades (Updated every 5 seconds):")
    print("=" * 60)
    
    while True:
        try:
            trades = await client.get_recent_trades(symbol="BTCUSDT", limit=5)
            
            print(f"\n⏰ {time.strftime('%H:%M:%S')} - Last 5 Trades:")
            for trade in trades:
                price = float(trade['price'])
                qty = float(trade['qty'])
                is_buyer = trade['isBuyerMaker']
                side = "🟢 BUY" if not is_buyer else "🔴 SELL"
                print(f"  {side} {qty:.6f} BTC @ ${price:,.2f}")
            
            await asyncio.sleep(5)  # Wait 5 seconds
            
        except KeyboardInterrupt:
            print("\n👋 Tracking stopped.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(5)

asyncio.run(track_recent_trades())
```

### Example 5: Technical Analysis with Klines

```python
import asyncio
from binance_context_server import BinanceClientWrapper

async def technical_analysis():
    client = BinanceClientWrapper()
    
    # Get 1-hour klines for BTC/USDT
    klines = await client.get_klines(symbol="BTCUSDT", interval="1h", limit=24)
    
    print("📊 BTC/USDT 24-Hour Technical Analysis:")
    print("=" * 50)
    
    if klines:
        # Calculate basic statistics
        prices = [float(k[4]) for k in klines]  # Close prices
        volumes = [float(k[5]) for k in klines]  # Volumes
        
        highest = max(prices)
        lowest = min(prices)
        avg_price = sum(prices) / len(prices)
        avg_volume = sum(volumes) / len(volumes)
        
        print(f"📈 Highest Price: ${highest:,.2f}")
        print(f"📉 Lowest Price: ${lowest:,.2f}")
        print(f"📊 Average Price: ${avg_price:,.2f}")
        print(f"📦 Average Volume: {avg_volume:,.2f} BTC")
        
        # Price change
        first_price = prices[0]
        last_price = prices[-1]
        change_percent = ((last_price - first_price) / first_price) * 100
        emoji = "🟢" if change_percent > 0 else "🔴" if change_percent < 0 else "⚪"
        
        print(f"\n{emoji} 24h Price Change: {change_percent:+.2f}%")

asyncio.run(technical_analysis())
```

---

## ⚙️ **Configuration**

### Using with API Key (Optional)

```python
from binance_context_server import BinanceClientWrapper

# Create client with API key
client = BinanceClientWrapper(
    api_key="your_api_key_here",
    api_secret="your_api_secret_here",
    testnet=False  # True for testnet
)

# Get account balance (requires API key)
balance = await client.get_account_balance()
```

### Environment Variables

```bash
# Create .env file
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=false
LOG_LEVEL=INFO
```

---

## 🚨 **Important Notes**

### ✅ **Working Features**
- All public market data (prices, statistics, order book)
- Recent trades and historical trades
- Exchange information and symbol details
- Server time

### 🔐 **API Key Required Features**
- Account balance (`get_account_balance`)
- Private trading data

### 📊 **Rate Limits**
- Binance API rate limits apply
- You may be temporarily blocked if you send too many requests
- Usually sufficient limits for public data

---

## 🐛 **Troubleshooting**

### Common Errors:

1. **"ModuleNotFoundError"**
   ```bash
   pip install binance-context-server
   ```

2. **"BinanceAPIException"**
   - Check your internet connection
   - Ensure symbol name is correct (e.g., "BTCUSDT")

3. **"PATH error" (Windows)**
   - Use full path or use as Python module

---

## 🎉 **Successful Test**

If everything works correctly, you should see this output:

```
🚀 Binance Context Server Usage Examples
==================================================
INFO:binance_context_server.binance_client:Binance client initialized for public data only

1️⃣ Bitcoin price:
   BTC/USDT: $115,781.08

2️⃣ Ethereum 24h statistics:
   ETH/USDT: $4,470.63
   24h change: %-1.52
   24h volume: 265,696 ETH

✅ All examples executed successfully!
```

---

## 📁 **Example Scripts**

This repository includes comprehensive example scripts:

- **`example_usage.py`** - Basic usage examples showing fundamental API calls
- **`advanced_examples.py`** - Advanced features including:
  - Portfolio tracking
  - Market scanning for significant movers
  - Technical analysis with indicators
  - Order book depth analysis
  - Real-time price monitoring

Run the examples:
```bash
python example_usage.py
python advanced_examples.py
```

---

## 📚 **More Information**

- [GitHub Repository](https://github.com/hocestnonsatis/binance-context-server)
- [PyPI Package](https://pypi.org/project/binance-context-server/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)

---

**🎯 Summary:** Package successfully installed from PyPI and working! You can import and use it as a Python module. 🚀
