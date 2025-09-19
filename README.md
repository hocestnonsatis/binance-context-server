# Binance Context Server

A comprehensive MCP (Model Context Protocol) server for Binance cryptocurrency market data and trading operations. This server provides **17 tools**, **15 resources**, and **2 prompts** for accessing real-time cryptocurrency data from Binance with advanced technical analysis capabilities.

## Features

### 🔧 Tools (17 total)
**Market Data Tools:**
- **get_crypto_price** - Get current price for any cryptocurrency trading pair
- **get_market_stats** - Get 24hr market statistics for trading pairs
- **get_top_cryptocurrencies** - Get top cryptocurrencies by 24hr volume
- **get_order_book** - Get order book (bid/ask prices) for trading pairs
- **get_candlestick_data** - Get candlestick/kline data for technical analysis
- **get_24hr_ticker** - Get detailed 24hr ticker price change statistics
- **get_avg_price** - Get current average price for a trading pair
- **get_price_change_statistics** - Get 24hr statistics for multiple symbols

**Trading & Account Tools:**
- **get_account_balance** - Get account balance (requires API credentials)
- **get_recent_trades** - Get recent trades for a trading pair
- **get_historical_trades** - Get historical trades for a trading pair

**Technical Analysis Tools:**
- **get_klines_with_indicators** - Get kline data with technical indicators (SMA, RSI, etc.)
- **get_symbol_info** - Get detailed information about a trading pair
- **search_symbols** - Search for trading pairs by asset name or symbol

**System Tools:**
- **get_exchange_info** - Get exchange trading rules and symbol information
- **get_server_time** - Get Binance server time

### 📚 Resources (15 total)
**Market Overview:**
- **Market Overview** - Current cryptocurrency market overview with top performers
- **Top Gainers** - Top gaining cryptocurrencies in the last 24 hours
- **Top Losers** - Top losing cryptocurrencies in the last 24 hours
- **Volume Leaders** - Cryptocurrencies with highest trading volume
- **Price Statistics** - 24hr price change statistics for top cryptocurrencies
- **Market Cap Leaders** - Cryptocurrencies ranked by market capitalization

**Market Analysis:**
- **Market Sentiment** - Market sentiment analysis based on price movements
- **Technical Analysis** - Technical indicators and analysis for major pairs
- **Recent Trades** - Recent trades data for major trading pairs

**Category-Specific Resources:**
- **DeFi Tokens** - DeFi tokens performance and statistics
- **Layer 1 Coins** - Layer 1 blockchain coins performance
- **Meme Coins** - Meme coins and their market performance
- **Stablecoins** - Stablecoin market data and statistics

**System Resources:**
- **Exchange Information** - Binance exchange trading rules and symbol information

### 💬 Prompts
- **crypto_analysis** - Analyze cryptocurrency market data and provide insights
- **market_overview** - Get a comprehensive overview of the cryptocurrency market

## Installation

### Option 1: From Source
1. Clone the repository:
```bash
git clone <repository-url>
cd binance-context-server
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

### Option 2: Using Pre-built Executable
Download the pre-built Windows executable from the `dist/` folder:
```bash
# Run the executable directly
./dist/binance-mcp-server.exe
```

### Dependencies
- **mcp** - Model Context Protocol implementation
- **python-binance** - Binance API client
- **pydantic** - Data validation
- **pandas-ta** - Technical analysis indicators
- **httpx** - HTTP client
- **anyio** - Async I/O

## Configuration

1. Copy the example environment file:
```bash
cp env.example .env
```

2. Edit `.env` file with your Binance API credentials (optional for public data):
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=false
LOG_LEVEL=INFO
```

**Note:** API credentials are only required for account-specific operations like `get_account_balance`. All other tools work with public data and don't require authentication.

## Usage

### Running the Server

```bash
python -m src.binance_context_server.server
```

### Using with MCP Clients

The server implements the MCP protocol and can be used with any MCP-compatible client. Configure your MCP client to connect to this server using stdio transport.

### Example Tool Calls

```python
# Market Data Tools
await tools.call_tool("get_crypto_price", {"symbol": "BTCUSDT"})
await tools.call_tool("get_market_stats", {"symbol": "ETHUSDT"})
await tools.call_tool("get_top_cryptocurrencies", {"limit": 10})
await tools.call_tool("get_order_book", {"symbol": "BTCUSDT", "limit": 20})

# Trading Tools
await tools.call_tool("get_recent_trades", {"symbol": "BTCUSDT", "limit": 100})
await tools.call_tool("get_historical_trades", {"symbol": "ETHUSDT", "limit": 50})

# Technical Analysis Tools
await tools.call_tool("get_klines_with_indicators", {
    "symbol": "BTCUSDT", 
    "interval": "1h", 
    "limit": 100,
    "include_indicators": True
})

# Search and Info Tools
await tools.call_tool("search_symbols", {"query": "bitcoin", "quote_asset": "USDT"})
await tools.call_tool("get_symbol_info", {"symbol": "BTCUSDT"})
await tools.call_tool("get_server_time", {})
```

### Example Resource Access

```python
# Market Overview Resources
market_data = await resources.read_resource("binance://market/overview")
gainers = await resources.read_resource("binance://market/top-gainers")
losers = await resources.read_resource("binance://market/top-losers")

# Market Analysis Resources
sentiment = await resources.read_resource("binance://market/fear-greed")
technical = await resources.read_resource("binance://market/technical-analysis")

# Category-Specific Resources
defi_tokens = await resources.read_resource("binance://market/defi-tokens")
layer1_coins = await resources.read_resource("binance://market/layer1-coins")
meme_coins = await resources.read_resource("binance://market/meme-coins")
```

## API Reference

### Tools

#### get_crypto_price
Get current price for a cryptocurrency trading pair.

**Parameters:**
- `symbol` (string, required): Trading pair symbol (e.g., BTCUSDT, ETHUSDT)

#### get_market_stats
Get 24hr market statistics for a trading pair.

**Parameters:**
- `symbol` (string, required): Trading pair symbol

#### get_top_cryptocurrencies
Get top cryptocurrencies by 24hr volume.

**Parameters:**
- `limit` (integer, optional): Number of top cryptos to return (default: 10, max: 50)
- `quote_asset` (string, optional): Quote asset to filter by (default: USDT)

#### get_order_book
Get order book (bid/ask prices) for a trading pair.

**Parameters:**
- `symbol` (string, required): Trading pair symbol
- `limit` (integer, optional): Number of price levels to return (default: 20)

#### get_candlestick_data
Get candlestick/kline data for technical analysis.

**Parameters:**
- `symbol` (string, required): Trading pair symbol
- `interval` (string, optional): Kline interval (default: 1h)
- `limit` (integer, optional): Number of klines to return (default: 100)

#### get_account_balance
Get account balance (requires API credentials).

**Parameters:** None

#### get_exchange_info
Get exchange trading rules and symbol information.

**Parameters:**
- `symbol` (string, optional): Specific symbol to get info for

#### get_recent_trades
Get recent trades for a trading pair.

**Parameters:**
- `symbol` (string, required): Trading pair symbol
- `limit` (integer, optional): Number of trades to return (default: 100, max: 1000)

#### get_historical_trades
Get historical trades for a trading pair.

**Parameters:**
- `symbol` (string, required): Trading pair symbol
- `limit` (integer, optional): Number of trades to return (default: 100, max: 1000)
- `from_id` (integer, optional): Trade ID to fetch from

#### get_klines_with_indicators
Get kline data with basic technical indicators.

**Parameters:**
- `symbol` (string, required): Trading pair symbol
- `interval` (string, optional): Kline interval (default: 1h)
- `limit` (integer, optional): Number of klines to return (default: 100)
- `include_indicators` (boolean, optional): Include technical indicators (default: true)

#### search_symbols
Search for trading pairs by asset name or symbol.

**Parameters:**
- `query` (string, required): Search query (asset name or symbol)
- `quote_asset` (string, optional): Filter by quote asset (default: USDT)
- `limit` (integer, optional): Maximum number of results (default: 20)

### Resources

#### Market Overview Resources
- **binance://market/overview** - Current cryptocurrency market overview with top performers
- **binance://market/top-gainers** - Top gaining cryptocurrencies in the last 24 hours
- **binance://market/top-losers** - Top losing cryptocurrencies in the last 24 hours
- **binance://market/volume-leaders** - Cryptocurrencies with highest trading volume
- **binance://market/price-statistics** - 24hr price change statistics for top cryptocurrencies
- **binance://market/market-cap** - Cryptocurrencies ranked by market capitalization

#### Market Analysis Resources
- **binance://market/fear-greed** - Market sentiment analysis based on price movements
- **binance://market/technical-analysis** - Technical indicators and analysis for major pairs
- **binance://market/recent-trades** - Recent trades data for major trading pairs

#### Category-Specific Resources
- **binance://market/defi-tokens** - DeFi tokens performance and statistics
- **binance://market/layer1-coins** - Layer 1 blockchain coins performance
- **binance://market/meme-coins** - Meme coins and their market performance
- **binance://market/stablecoins** - Stablecoin market data and statistics

#### System Resources
- **binance://exchange/info** - Binance exchange trading rules and symbol information

## Advanced Features

### Technical Analysis
The server includes advanced technical analysis capabilities:
- **RSI (Relative Strength Index)** calculation
- **SMA (Simple Moving Average)** indicators
- **Volume analysis** and ratios
- **Trend detection** algorithms
- **Market sentiment** analysis

### Market Categories
Specialized resources for different cryptocurrency categories:
- **DeFi Tokens**: UNI, AAVE, COMP, SUSHI, CRV, YFI, 1INCH, SNX
- **Layer 1 Coins**: ETH, BNB, ADA, SOL, DOT, AVAX, MATIC, ALGO, ATOM, NEAR
- **Meme Coins**: DOGE, SHIB, PEPE, FLOKI, BONK, WIF
- **Stablecoins**: USDT, USDC, BUSD, DAI, TUSD

### Production Ready
- ✅ **17 comprehensive tools** for market analysis
- ✅ **15 specialized resources** for different market segments
- ✅ **Pre-built Windows executable** for easy deployment
- ✅ **Advanced technical indicators** with pandas-ta integration
- ✅ **Real-time market sentiment** analysis
- ✅ **Comprehensive error handling** and logging

## Development

### Project Structure

```
src/binance_context_server/
├── __init__.py          # Package initialization
├── server.py            # Main MCP server implementation
├── binance_client.py    # Binance API client wrapper
├── tools.py             # MCP tools implementation (17 tools)
└── resources.py         # MCP resources implementation (15 resources)

dist/
└── binance-mcp-server.exe  # Pre-built Windows executable

build/
└── binance-mcp-server/     # PyInstaller build files
```

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller binance-mcp-server.spec
```

### Running Tests

```bash
python -m pytest
```

### Code Formatting

```bash
black src/
ruff check src/
```

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.
