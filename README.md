# Binance Context Server

A comprehensive MCP (Model Context Protocol) server for Binance cryptocurrency market data and trading operations. This server provides tools, resources, and prompts for accessing real-time cryptocurrency data from Binance.

## Features

### 🔧 Tools
- **get_crypto_price** - Get current price for any cryptocurrency trading pair
- **get_market_stats** - Get 24hr market statistics for trading pairs
- **get_top_cryptocurrencies** - Get top cryptocurrencies by 24hr volume
- **get_order_book** - Get order book (bid/ask prices) for trading pairs
- **get_candlestick_data** - Get candlestick/kline data for technical analysis
- **get_account_balance** - Get account balance (requires API credentials)
- **get_exchange_info** - Get exchange trading rules and symbol information

### 📚 Resources
- **Market Overview** - Current cryptocurrency market overview with top performers
- **Top Gainers** - Top gaining cryptocurrencies in the last 24 hours
- **Top Losers** - Top losing cryptocurrencies in the last 24 hours
- **Volume Leaders** - Cryptocurrencies with highest trading volume
- **Exchange Information** - Binance exchange trading rules and symbol information

### 💬 Prompts
- **crypto_analysis** - Analyze cryptocurrency market data and provide insights
- **market_overview** - Get a comprehensive overview of the cryptocurrency market

## Installation

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
# Get Bitcoin price
await tools.call_tool("get_crypto_price", {"symbol": "BTCUSDT"})

# Get market statistics
await tools.call_tool("get_market_stats", {"symbol": "ETHUSDT"})

# Get top 10 cryptocurrencies
await tools.call_tool("get_top_cryptocurrencies", {"limit": 10})

# Get order book
await tools.call_tool("get_order_book", {"symbol": "BTCUSDT", "limit": 20})
```

### Example Resource Access

```python
# Get market overview
market_data = await resources.read_resource("binance://market/overview")

# Get top gainers
gainers = await resources.read_resource("binance://market/top-gainers")
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

### Resources

#### binance://market/overview
Current cryptocurrency market overview with top performers.

#### binance://market/top-gainers
Top gaining cryptocurrencies in the last 24 hours.

#### binance://market/top-losers
Top losing cryptocurrencies in the last 24 hours.

#### binance://market/volume-leaders
Cryptocurrencies with highest trading volume.

#### binance://exchange/info
Binance exchange trading rules and symbol information.

## Development

### Project Structure

```
src/binance_context_server/
├── __init__.py          # Package initialization
├── server.py            # Main MCP server implementation
├── binance_client.py    # Binance API client wrapper
├── tools.py             # MCP tools implementation
└── resources.py         # MCP resources implementation
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
