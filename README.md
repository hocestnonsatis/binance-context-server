# Binance Context Server

MCP (Model Context Protocol) server for accessing Binance cryptocurrency data. Provides real-time price data, technical analysis, and market statistics.

## Features

- 📊 **Real-time price data** - Current prices for all cryptocurrency trading pairs
- 📈 **Technical analysis** - Technical indicators like RSI, SMA
- 📋 **Market statistics** - 24-hour changes, volume, high/low prices
- 🔍 **Search and filtering** - Cryptocurrency search and category filtering
- ⚡ **Fast access** - Direct connection to Binance API

## Installation

### 1. Install from PyPI (Recommended)
```bash
pip install binance-context-server
```

### 2. Install from Source
```bash
git clone https://github.com/hocestnonsatis/binance-context-server.git
cd binance-context-server
pip install -e .
```


## Configuration

### 1. Environment Variables (Optional)
```bash
cp env.example .env
```

Edit the `.env` file:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=false
LOG_LEVEL=INFO
```

**Note:** API keys are only required for account operations. Not needed for public data.

## Usage

### Running the Server
```bash
python -m binance_context_server.server
```

### Using with MCP Clients
This server supports the MCP protocol and can be used with any MCP-compatible client.

### Basic Examples

**Using with Python:**
```python
from binance_context_server import BinanceClientWrapper
import asyncio

async def main():
    client = BinanceClientWrapper()
    
    # Bitcoin price
    btc_price = await client.get_symbol_price(symbol="BTCUSDT")
    print(f"BTC: ${float(btc_price['price']):,.2f}")
    
    # Market statistics
    stats = await client.get_ticker_24hr(symbol="ETHUSDT")
    if stats:
        eth = stats[0]
        print(f"ETH: ${float(eth.lastPrice):,.2f}")

asyncio.run(main())
```

**MCP Tool calls:**
```python
# Price data
await tools.call_tool("get_crypto_price", {"symbol": "BTCUSDT"})
await tools.call_tool("get_market_stats", {"symbol": "ETHUSDT"})

# Technical analysis
await tools.call_tool("get_klines_with_indicators", {
    "symbol": "BTCUSDT", 
    "interval": "1h", 
    "limit": 100
})

# Search
await tools.call_tool("search_symbols", {"query": "bitcoin"})
```

## IDE Configuration

### MCP Settings for Cursor/VS Code

Add the following configuration to your `settings.json` file:

```json
{
  "mcpServers": {
    "binance-context-server": {
      "command": "python",
      "args": ["-m", "binance_context_server.server"],
      "env": {
        "BINANCE_API_KEY": "your_api_key_here",
        "BINANCE_API_SECRET": "your_api_secret_here"
      }
    }
  }
}
```


## Available Tools

- `get_crypto_price` - Cryptocurrency price
- `get_market_stats` - 24-hour market statistics  
- `get_top_cryptocurrencies` - Most traded cryptocurrencies
- `get_order_book` - Buy/sell prices
- `get_candlestick_data` - Candlestick chart data
- `get_klines_with_indicators` - Technical analysis indicators
- `search_symbols` - Cryptocurrency search
- `get_account_balance` - Account balance (API required)

## License

MIT License

## Support

For questions, please open an issue on GitHub.
