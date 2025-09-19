"""Binance MCP Server main entry point."""

import asyncio
import logging
import os
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
            
            else:
                return [TextContent(type="text", text=f"Unknown prompt: {name}")]
    
    async def run(self):
        """Run the MCP server."""
        await self.initialize()
        
        # Initialize server options
        options = InitializationOptions(
            server_name="binance-context-server",
            server_version="0.1.0",
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
