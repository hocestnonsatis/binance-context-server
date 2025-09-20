"""Binance MCP Server main entry point."""

import asyncio
import logging
import os
from datetime import datetime
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, ImageContent, EmbeddedResource

from binance_context_server.binance_client import BinanceClientWrapper
from binance_context_server.tools import BinanceTools
from binance_context_server.resources import BinanceResources


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BinanceMCPServer:
    """Main Binance MCP Server class."""
    
    def __init__(self):
        """Initialize the server."""
        self.server = Server("binance-context-server")
        self.binance_client = None
        self.tools = None
        self.resources = None
        
    async def initialize(self):
        """Initialize the server components."""
        try:
            # Initialize Binance client
            api_key = os.getenv('BINANCE_API_KEY')
            api_secret = os.getenv('BINANCE_API_SECRET')
            testnet = os.getenv('BINANCE_TESTNET', 'false').lower() == 'true'
            
            self.binance_client = BinanceClientWrapper(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet
            )
            
            # Initialize tools and resources
            self.tools = BinanceTools(self.binance_client)
            self.resources = BinanceResources(self.binance_client)
            
            # Register handlers
            await self._register_handlers()
            
            logger.info("Binance MCP Server initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize server: {e}")
            raise
    
    async def _register_handlers(self):
        """Register MCP server handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> list:
            """List available tools."""
            return self.tools.get_tools()
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any] | None) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Call a tool."""
            if arguments is None:
                arguments = {}
            return await self.tools.call_tool(name, arguments)
        
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available resources."""
            return await self.resources.list_resources()
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource."""
            return await self.resources.read_resource(uri)
        
        @self.server.list_prompts()
        async def list_prompts() -> list:
            """List available prompts."""
            return [
                {
                    "name": "crypto_analysis",
                    "description": "Analyze cryptocurrency market data and provide insights",
                    "arguments": [
                        {
                            "name": "symbol",
                            "description": "Cryptocurrency symbol to analyze (e.g., BTCUSDT)",
                            "required": True
                        },
                        {
                            "name": "analysis_type",
                            "description": "Type of analysis (technical, fundamental, or both)",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "market_overview",
                    "description": "Get a comprehensive overview of the cryptocurrency market",
                    "arguments": [
                        {
                            "name": "limit",
                            "description": "Number of top cryptocurrencies to include (default: 10)",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "portfolio_analysis",
                    "description": "Analyze a cryptocurrency portfolio performance and risk",
                    "arguments": [
                        {
                            "name": "symbols",
                            "description": "Comma-separated list of cryptocurrency symbols (e.g., BTCUSDT,ETHUSDT,BNBUSDT)",
                            "required": True
                        },
                        {
                            "name": "quantities",
                            "description": "Comma-separated list of quantities for each symbol (e.g., 0.1,1.0,10.0)",
                            "required": True
                        }
                    ]
                },
                {
                    "name": "market_sentiment",
                    "description": "Analyze overall market sentiment and trends",
                    "arguments": [
                        {
                            "name": "timeframe",
                            "description": "Analysis timeframe (1h, 4h, 24h, 7d) - default: 24h",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "risk_assessment",
                    "description": "Assess risk levels for specific trading pairs",
                    "arguments": [
                        {
                            "name": "symbols",
                            "description": "Comma-separated list of trading pairs to assess",
                            "required": True
                        },
                        {
                            "name": "risk_factors",
                            "description": "Risk factors to analyze (volatility, liquidity, correlation) - default: all",
                            "required": False
                        }
                    ]
                }
            ]
        
        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: dict[str, str] | None) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Get a prompt."""
            if arguments is None:
                arguments = {}
            
            if name == "crypto_analysis":
                symbol = arguments.get("symbol", "BTCUSDT")
                analysis_type = arguments.get("analysis_type", "both")
                
                # Get market data
                try:
                    market_data = await self.binance_client.get_ticker_24hr(symbol)
                    price_data = await self.binance_client.get_symbol_price(symbol)
                    order_book = await self.binance_client.get_order_book(symbol, 20)
                    
                    data = market_data[0]
                    price_change_percent = float(data.priceChangePercent)
                    emoji = "📈" if price_change_percent > 0 else "📉" if price_change_percent < 0 else "➡️"
                    
                    prompt = f"# {emoji} {symbol.upper()} Cryptocurrency Analysis\n\n"
                    prompt += f"## Current Market Data\n"
                    prompt += f"- **Current Price:** ${float(price_data['price']):,.2f}\n"
                    prompt += f"- **24hr Change:** ${float(data.priceChange):,.2f} ({price_change_percent:+.2f}%)\n"
                    prompt += f"- **24hr High:** ${float(data.highPrice):,.2f}\n"
                    prompt += f"- **24hr Low:** ${float(data.lowPrice):,.2f}\n"
                    prompt += f"- **24hr Volume:** {float(data.volume):,.2f}\n"
                    prompt += f"- **24hr Quote Volume:** ${float(data.quoteVolume):,.2f}\n\n"
                    
                    # Calculate spread
                    best_ask = float(order_book.asks[0][0])
                    best_bid = float(order_book.bids[0][0])
                    spread = best_ask - best_bid
                    spread_percent = (spread / best_bid) * 100
                    
                    prompt += f"## Order Book Analysis\n"
                    prompt += f"- **Best Bid:** ${best_bid:,.2f}\n"
                    prompt += f"- **Best Ask:** ${best_ask:,.2f}\n"
                    prompt += f"- **Spread:** ${spread:.2f} ({spread_percent:.3f}%)\n\n"
                    
                    if analysis_type in ["technical", "both"]:
                        prompt += f"## Technical Analysis\n"
                        prompt += f"Please provide technical analysis including:\n"
                        prompt += f"- Trend analysis based on price movement\n"
                        prompt += f"- Support and resistance levels\n"
                        prompt += f"- Volume analysis\n"
                        prompt += f"- Momentum indicators\n\n"
                    
                    if analysis_type in ["fundamental", "both"]:
                        prompt += f"## Fundamental Analysis\n"
                        prompt += f"Please provide fundamental analysis including:\n"
                        prompt += f"- Market sentiment based on volume and price action\n"
                        prompt += f"- Trading activity assessment\n"
                        prompt += f"- Risk factors and opportunities\n"
                        prompt += f"- Market position relative to other cryptocurrencies\n\n"
                    
                    prompt += f"## Analysis Request\n"
                    prompt += f"Based on the above data, please provide a comprehensive analysis of {symbol.upper()} including:\n"
                    prompt += f"1. Current market position and trends\n"
                    prompt += f"2. Key technical indicators and patterns\n"
                    prompt += f"3. Trading opportunities and risks\n"
                    prompt += f"4. Short-term and long-term outlook\n"
                    prompt += f"5. Recommended actions for traders/investors\n"
                    
                    return [TextContent(type="text", text=prompt)]
                    
                except Exception as e:
                    return [TextContent(type="text", text=f"Error getting market data: {str(e)}")]
            
            elif name == "market_overview":
                limit = int(arguments.get("limit", 10))
                
                try:
                    # Get top cryptocurrencies
                    all_tickers = await self.binance_client.get_ticker_24hr()
                    usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
                    sorted_tickers = sorted(usdt_tickers, key=lambda x: float(x.quoteVolume), reverse=True)[:limit]
                    
                    prompt = f"# 🏆 Top {limit} Cryptocurrencies Market Overview\n\n"
                    prompt += f"## Market Summary\n"
                    
                    total_volume = sum(float(t.quoteVolume) for t in sorted_tickers)
                    positive_count = sum(1 for t in sorted_tickers if float(t.priceChangePercent) > 0)
                    negative_count = sum(1 for t in sorted_tickers if float(t.priceChangePercent) < 0)
                    
                    prompt += f"- **Total 24hr Volume (Top {limit}):** ${total_volume:,.0f}\n"
                    prompt += f"- **Market Sentiment:** {positive_count} gaining, {negative_count} declining\n"
                    prompt += f"- **Analysis Date:** {asyncio.get_event_loop().time()}\n\n"
                    
                    prompt += f"## Individual Cryptocurrency Analysis\n"
                    for i, ticker in enumerate(sorted_tickers, 1):
                        base_asset = ticker.symbol.replace('USDT', '')
                        price_change_percent = float(ticker.priceChangePercent)
                        emoji = "🟢" if price_change_percent > 0 else "🔴" if price_change_percent < 0 else "⚪"
                        
                        prompt += f"### {i}. {base_asset} {emoji}\n"
                        prompt += f"- **Price:** ${float(ticker.lastPrice):,.2f}\n"
                        prompt += f"- **24hr Change:** {price_change_percent:+.2f}%\n"
                        prompt += f"- **24hr Volume:** ${float(ticker.quoteVolume):,.0f}\n"
                        prompt += f"- **24hr High:** ${float(ticker.highPrice):,.2f}\n"
                        prompt += f"- **24hr Low:** ${float(ticker.lowPrice):,.2f}\n\n"
                    
                    prompt += f"## Market Analysis Request\n"
                    prompt += f"Please provide a comprehensive market analysis including:\n"
                    prompt += f"1. Overall market trends and sentiment\n"
                    prompt += f"2. Sector performance analysis\n"
                    prompt += f"3. Key market movers and their impact\n"
                    prompt += f"4. Trading opportunities and risks\n"
                    prompt += f"5. Market outlook and predictions\n"
                    prompt += f"6. Investment recommendations\n"
                    
                    return [TextContent(type="text", text=prompt)]
                    
                except Exception as e:
                    return [TextContent(type="text", text=f"Error getting market overview: {str(e)}")]
            
            elif name == "portfolio_analysis":
                symbols_str = arguments.get("symbols", "")
                quantities_str = arguments.get("quantities", "")
                
                if not symbols_str or not quantities_str:
                    return [TextContent(type="text", text="Error: Both symbols and quantities are required")]
                
                symbols = [s.strip().upper() for s in symbols_str.split(",")]
                quantities = [float(q.strip()) for q in quantities_str.split(",")]
                
                if len(symbols) != len(quantities):
                    return [TextContent(type="text", text="Error: Number of symbols and quantities must match")]
                
                try:
                    prompt = f"# 💼 Portfolio Analysis\n\n"
                    prompt += f"## Portfolio Composition\n"
                    
                    total_value = 0
                    portfolio_data = []
                    
                    for symbol, quantity in zip(symbols, quantities):
                        try:
                            price_data = await self.binance_client.get_symbol_price(symbol)
                            price = float(price_data['price'])
                            value = price * quantity
                            total_value += value
                            
                            # Get 24h change
                            ticker_data = await self.binance_client.get_ticker_24hr(symbol)
                            change_percent = 0
                            if ticker_data:
                                change_percent = float(ticker_data[0].priceChangePercent)
                            
                            portfolio_data.append({
                                "symbol": symbol,
                                "quantity": quantity,
                                "price": price,
                                "value": value,
                                "change_24h": change_percent
                            })
                            
                        except Exception as e:
                            prompt += f"⚠️ Could not get data for {symbol}: {str(e)}\n"
                    
                    # Portfolio breakdown
                    prompt += f"- **Total Portfolio Value:** ${total_value:,.2f}\n"
                    prompt += f"- **Number of Assets:** {len(portfolio_data)}\n\n"
                    
                    prompt += f"## Asset Details\n"
                    for asset in portfolio_data:
                        percentage = (asset['value'] / total_value) * 100 if total_value > 0 else 0
                        change_emoji = "🟢" if asset['change_24h'] > 0 else "🔴" if asset['change_24h'] < 0 else "⚪"
                        
                        prompt += f"### {asset['symbol']} {change_emoji}\n"
                        prompt += f"- **Quantity:** {asset['quantity']:.6f}\n"
                        prompt += f"- **Current Price:** ${asset['price']:,.2f}\n"
                        prompt += f"- **Value:** ${asset['value']:,.2f} ({percentage:.1f}%)\n"
                        prompt += f"- **24h Change:** {asset['change_24h']:+.2f}%\n\n"
                    
                    prompt += f"## Portfolio Analysis Request\n"
                    prompt += f"Please provide a comprehensive portfolio analysis including:\n"
                    prompt += f"1. Portfolio diversification assessment\n"
                    prompt += f"2. Risk analysis and concentration\n"
                    prompt += f"3. Performance evaluation\n"
                    prompt += f"4. Rebalancing recommendations\n"
                    prompt += f"5. Risk management strategies\n"
                    prompt += f"6. Future outlook and adjustments\n"
                    
                    return [TextContent(type="text", text=prompt)]
                    
                except Exception as e:
                    return [TextContent(type="text", text=f"Error analyzing portfolio: {str(e)}")]
            
            elif name == "market_sentiment":
                timeframe = arguments.get("timeframe", "24h")
                
                try:
                    prompt = f"# 📊 Market Sentiment Analysis - {timeframe.upper()}\n\n"
                    
                    # Get market data
                    all_tickers = await self.binance_client.get_ticker_24hr()
                    usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
                    
                    # Calculate sentiment metrics
                    positive_count = sum(1 for t in usdt_tickers if float(t.priceChangePercent) > 0)
                    negative_count = sum(1 for t in usdt_tickers if float(t.priceChangePercent) < 0)
                    neutral_count = len(usdt_tickers) - positive_count - negative_count
                    
                    total_cryptos = len(usdt_tickers)
                    positive_percent = (positive_count / total_cryptos) * 100
                    negative_percent = (negative_count / total_cryptos) * 100
                    
                    # Top gainers and losers
                    top_gainers = sorted(usdt_tickers, key=lambda x: float(x.priceChangePercent), reverse=True)[:10]
                    top_losers = sorted(usdt_tickers, key=lambda x: float(x.priceChangePercent))[:10]
                    
                    prompt += f"## Market Sentiment Summary\n"
                    prompt += f"- **Total Cryptocurrencies Analyzed:** {total_cryptos}\n"
                    prompt += f"- **Positive Movement:** {positive_count} ({positive_percent:.1f}%)\n"
                    prompt += f"- **Negative Movement:** {negative_count} ({negative_percent:.1f}%)\n"
                    prompt += f"- **Neutral Movement:** {neutral_count}\n\n"
                    
                    # Sentiment classification
                    if positive_percent > 60:
                        sentiment = "🟢 Bullish"
                    elif negative_percent > 60:
                        sentiment = "🔴 Bearish"
                    else:
                        sentiment = "⚪ Neutral/Mixed"
                    
                    prompt += f"## Overall Sentiment: {sentiment}\n\n"
                    
                    prompt += f"## Top Performers\n"
                    for i, ticker in enumerate(top_gainers[:5], 1):
                        change = float(ticker.priceChangePercent)
                        prompt += f"{i}. **{ticker.symbol}**: {change:+.2f}% (${float(ticker.lastPrice):,.2f})\n"
                    
                    prompt += f"\n## Worst Performers\n"
                    for i, ticker in enumerate(top_losers[:5], 1):
                        change = float(ticker.priceChangePercent)
                        prompt += f"{i}. **{ticker.symbol}**: {change:+.2f}% (${float(ticker.lastPrice):,.2f})\n"
                    
                    prompt += f"\n## Market Sentiment Analysis Request\n"
                    prompt += f"Please provide a detailed market sentiment analysis including:\n"
                    prompt += f"1. Current market psychology and investor behavior\n"
                    prompt += f"2. Trend analysis and momentum indicators\n"
                    prompt += f"3. Fear and greed assessment\n"
                    prompt += f"4. Market cycle positioning\n"
                    prompt += f"5. Trading opportunities based on sentiment\n"
                    prompt += f"6. Risk factors and market warnings\n"
                    prompt += f"7. Predictions for next market moves\n"
                    
                    return [TextContent(type="text", text=prompt)]
                    
                except Exception as e:
                    return [TextContent(type="text", text=f"Error analyzing market sentiment: {str(e)}")]
            
            elif name == "risk_assessment":
                symbols_str = arguments.get("symbols", "")
                risk_factors = arguments.get("risk_factors", "all")
                
                if not symbols_str:
                    return [TextContent(type="text", text="Error: Symbols are required")]
                
                symbols = [s.strip().upper() for s in symbols_str.split(",")]
                
                try:
                    prompt = f"# ⚠️ Risk Assessment Analysis\n\n"
                    prompt += f"## Trading Pairs Analyzed\n"
                    prompt += f"- **Symbols:** {', '.join(symbols)}\n"
                    prompt += f"- **Risk Factors:** {risk_factors}\n"
                    prompt += f"- **Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    
                    risk_data = []
                    
                    for symbol in symbols:
                        try:
                            # Get price and volatility data
                            ticker_data = await self.binance_client.get_ticker_24hr(symbol)
                            if ticker_data:
                                ticker = ticker_data[0]
                                high_price = float(ticker.highPrice)
                                low_price = float(ticker.lowPrice)
                                current_price = float(ticker.lastPrice)
                                volume = float(ticker.volume)
                                change_percent = float(ticker.priceChangePercent)
                                
                                # Calculate volatility
                                price_range = high_price - low_price
                                volatility_percent = (price_range / current_price) * 100 if current_price > 0 else 0
                                
                                # Get order book for liquidity analysis
                                try:
                                    order_book = await self.binance_client.get_order_book(symbol, 10)
                                    best_bid = float(order_book.bids[0][0])
                                    best_ask = float(order_book.asks[0][0])
                                    spread_percent = ((best_ask - best_bid) / best_bid) * 100
                                    
                                    # Calculate liquidity score
                                    total_bid_volume = sum(float(bid[1]) for bid in order_book.bids)
                                    total_ask_volume = sum(float(ask[1]) for ask in order_book.asks)
                                    liquidity_ratio = total_bid_volume / total_ask_volume if total_ask_volume > 0 else 0
                                    
                                except Exception:
                                    spread_percent = 0
                                    liquidity_ratio = 1
                                
                                risk_data.append({
                                    "symbol": symbol,
                                    "price": current_price,
                                    "volatility": volatility_percent,
                                    "change_24h": change_percent,
                                    "volume": volume,
                                    "spread": spread_percent,
                                    "liquidity_ratio": liquidity_ratio
                                })
                                
                        except Exception as e:
                            prompt += f"⚠️ Could not analyze {symbol}: {str(e)}\n"
                    
                    prompt += f"## Risk Metrics\n"
                    for data in risk_data:
                        # Risk level assessment
                        risk_score = 0
                        risk_factors_list = []
                        
                        # Volatility risk
                        if data['volatility'] > 10:
                            risk_score += 3
                            risk_factors_list.append("High Volatility")
                        elif data['volatility'] > 5:
                            risk_score += 2
                            risk_factors_list.append("Medium Volatility")
                        
                        # Liquidity risk
                        if data['liquidity_ratio'] < 0.8:
                            risk_score += 2
                            risk_factors_list.append("Low Liquidity")
                        elif data['liquidity_ratio'] > 1.2:
                            risk_score += 0
                        else:
                            risk_score += 1
                            risk_factors_list.append("Medium Liquidity")
                        
                        # Spread risk
                        if data['spread'] > 0.1:
                            risk_score += 2
                            risk_factors_list.append("Wide Spread")
                        
                        # Volume risk
                        if data['volume'] < 1000:
                            risk_score += 1
                            risk_factors_list.append("Low Volume")
                        
                        # Risk level classification
                        if risk_score <= 2:
                            risk_level = "🟢 Low Risk"
                        elif risk_score <= 4:
                            risk_level = "🟡 Medium Risk"
                        else:
                            risk_level = "🔴 High Risk"
                        
                        prompt += f"### {data['symbol']} - {risk_level}\n"
                        prompt += f"- **Price:** ${data['price']:,.2f}\n"
                        prompt += f"- **24h Change:** {data['change_24h']:+.2f}%\n"
                        prompt += f"- **Volatility:** {data['volatility']:.2f}%\n"
                        prompt += f"- **Spread:** {data['spread']:.4f}%\n"
                        prompt += f"- **Liquidity Ratio:** {data['liquidity_ratio']:.2f}\n"
                        prompt += f"- **Volume:** {data['volume']:,.0f}\n"
                        prompt += f"- **Risk Factors:** {', '.join(risk_factors_list) if risk_factors_list else 'None'}\n\n"
                    
                    prompt += f"## Risk Assessment Analysis Request\n"
                    prompt += f"Please provide a comprehensive risk assessment including:\n"
                    prompt += f"1. Overall risk profile for each trading pair\n"
                    prompt += f"2. Portfolio risk diversification analysis\n"
                    prompt += f"3. Risk mitigation strategies\n"
                    prompt += f"4. Position sizing recommendations\n"
                    prompt += f"5. Stop-loss and take-profit levels\n"
                    prompt += f"6. Market conditions that could increase risk\n"
                    prompt += f"7. Alternative lower-risk opportunities\n"
                    
                    return [TextContent(type="text", text=prompt)]
                    
                except Exception as e:
                    return [TextContent(type="text", text=f"Error in risk assessment: {str(e)}")]
            
            else:
                return [TextContent(type="text", text=f"Unknown prompt: {name}")]
    
    async def run(self):
        """Run the MCP server."""
        await self.initialize()
        
        # Initialize server options
        options = InitializationOptions(
            server_name="binance-context-server",
            server_version="1.0.1",
            capabilities={
                "tools": {},
                "resources": {},
                "prompts": {}
            }
        )
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                options
            )


async def main():
    """Main entry point."""
    server = BinanceMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
