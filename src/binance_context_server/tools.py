"""MCP tools for Binance operations."""

import json
import logging
from typing import Any, Sequence, Dict

from mcp.types import Tool
from mcp.types import TextContent, ImageContent, EmbeddedResource

from .binance_client import BinanceClientWrapper


logger = logging.getLogger(__name__)


class BinanceTools:
    """Binance MCP tools."""
    
    def __init__(self, client: BinanceClientWrapper):
        """Initialize tools with Binance client.
        
        Args:
            client: Binance client wrapper
        """
        self.client = client
    
    def get_tools(self) -> list[Tool]:
        """Get list of available tools.
        
        Returns:
            List of MCP tools
        """
        return [
            Tool(
                name="get_crypto_price",
                description="Get current price for a cryptocurrency trading pair",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
                        }
                    },
                    "required": ["symbol"]
                }
            ),
            Tool(
                name="get_market_stats",
                description="Get 24hr market statistics for a trading pair",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
                        }
                    },
                    "required": ["symbol"]
                }
            ),
            Tool(
                name="get_top_cryptocurrencies",
                description="Get top cryptocurrencies by 24hr volume",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Number of top cryptos to return (default: 10, max: 50)",
                            "minimum": 1,
                            "maximum": 50,
                            "default": 10
                        },
                        "quote_asset": {
                            "type": "string",
                            "description": "Quote asset to filter by (e.g., USDT, BTC, ETH). Default: USDT",
                            "default": "USDT"
                        }
                    }
                }
            ),
            Tool(
                name="get_order_book",
                description="Get order book (bid/ask prices) for a trading pair",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of price levels to return (5, 10, 20, 50, 100, 500, 1000, 5000). Default: 20",
                            "enum": [5, 10, 20, 50, 100, 500, 1000, 5000],
                            "default": 20
                        }
                    },
                    "required": ["symbol"]
                }
            ),
            Tool(
                name="get_candlestick_data",
                description="Get candlestick/kline data for technical analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
                        },
                        "interval": {
                            "type": "string",
                            "description": "Kline interval",
                            "enum": ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"],
                            "default": "1h"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of klines to return (max 1000). Default: 100",
                            "minimum": 1,
                            "maximum": 1000,
                            "default": 100
                        }
                    },
                    "required": ["symbol"]
                }
            ),
            Tool(
                name="get_account_balance",
                description="Get account balance (requires API credentials)",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            ),
            Tool(
                name="get_exchange_info",
                description="Get exchange trading rules and symbol information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Specific symbol to get info for (optional)"
                        }
                    }
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Call a tool with given arguments.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool response
        """
        try:
            if name == "get_crypto_price":
                return await self._get_crypto_price(arguments)
            elif name == "get_market_stats":
                return await self._get_market_stats(arguments)
            elif name == "get_top_cryptocurrencies":
                return await self._get_top_cryptocurrencies(arguments)
            elif name == "get_order_book":
                return await self._get_order_book(arguments)
            elif name == "get_candlestick_data":
                return await self._get_candlestick_data(arguments)
            elif name == "get_account_balance":
                return await self._get_account_balance(arguments)
            elif name == "get_exchange_info":
                return await self._get_exchange_info(arguments)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
                
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _get_crypto_price(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Get crypto price tool implementation."""
        symbol = arguments["symbol"]
        price_data = await self.client.get_symbol_price(symbol)
        
        response = f"💰 **{symbol.upper()} Price**\n"
        response += f"Current Price: ${float(price_data['price']):,.2f}"
        
        return [TextContent(type="text", text=response)]
    
    async def _get_market_stats(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Get market stats tool implementation."""
        symbol = arguments["symbol"]
        market_data = await self.client.get_ticker_24hr(symbol)
        data = market_data[0]  # get_ticker_24hr returns a list
        
        price_change_percent = float(data.priceChangePercent)
        emoji = "📈" if price_change_percent > 0 else "📉" if price_change_percent < 0 else "➡️"
        
        response = f"{emoji} **{data.symbol} - 24hr Market Stats**\n\n"
        response += f"• **Current Price:** ${float(data.lastPrice):,.2f}\n"
        response += f"• **24hr Change:** ${float(data.priceChange):,.2f} ({price_change_percent:+.2f}%)\n"
        response += f"• **24hr High:** ${float(data.highPrice):,.2f}\n"
        response += f"• **24hr Low:** ${float(data.lowPrice):,.2f}\n"
        response += f"• **24hr Volume:** {float(data.volume):,.2f} {data.symbol.replace('USDT', '').replace('BTC', '').replace('ETH', '')}\n"
        response += f"• **24hr Quote Volume:** ${float(data.quoteVolume):,.2f}"
        
        return [TextContent(type="text", text=response)]
    
    async def _get_top_cryptocurrencies(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Get top cryptocurrencies tool implementation."""
        limit = arguments.get("limit", 10)
        quote_asset = arguments.get("quote_asset", "USDT")
        
        all_tickers = await self.client.get_ticker_24hr()
        
        # Filter by quote asset and sort by quote volume
        filtered_tickers = [
            ticker for ticker in all_tickers 
            if ticker.symbol.endswith(quote_asset)
        ]
        
        # Sort by 24hr quote volume (descending)
        sorted_tickers = sorted(
            filtered_tickers, 
            key=lambda x: float(x.quoteVolume), 
            reverse=True
        )[:limit]
        
        response = f"🏆 **Top {limit} Cryptocurrencies by Volume ({quote_asset} pairs)**\n\n"
        
        for i, ticker in enumerate(sorted_tickers, 1):
            base_asset = ticker.symbol.replace(quote_asset, '')
            price_change_percent = float(ticker.priceChangePercent)
            emoji = "🟢" if price_change_percent > 0 else "🔴" if price_change_percent < 0 else "⚪"
            
            response += f"**{i}. {base_asset}/{quote_asset}** {emoji}\n"
            response += f"   Price: ${float(ticker.lastPrice):,.2f} ({price_change_percent:+.2f}%)\n"
            response += f"   Volume: ${float(ticker.quoteVolume):,.0f}\n\n"
        
        return [TextContent(type="text", text=response)]
    
    async def _get_order_book(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Get order book tool implementation."""
        symbol = arguments["symbol"]
        limit = arguments.get("limit", 20)
        
        order_book = await self.client.get_order_book(symbol, limit)
        
        response = f"📊 **{symbol.upper()} Order Book (Top {limit})**\n\n"
        
        response += "**🔴 Asks (Sell Orders)**\n"
        for i, ask in enumerate(order_book.asks[:5]):  # Show top 5 asks
            price, quantity = ask
            response += f"  ${float(price):,.2f} - {float(quantity):,.4f}\n"
        
        response += "\n**🟢 Bids (Buy Orders)**\n"
        for i, bid in enumerate(order_book.bids[:5]):  # Show top 5 bids
            price, quantity = bid
            response += f"  ${float(price):,.2f} - {float(quantity):,.4f}\n"
        
        # Calculate spread
        best_ask = float(order_book.asks[0][0])
        best_bid = float(order_book.bids[0][0])
        spread = best_ask - best_bid
        spread_percent = (spread / best_bid) * 100
        
        response += f"\n**📏 Spread:** ${spread:.2f} ({spread_percent:.3f}%)"
        
        return [TextContent(type="text", text=response)]
    
    async def _get_candlestick_data(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Get candlestick data tool implementation."""
        symbol = arguments["symbol"]
        interval = arguments.get("interval", "1h")
        limit = arguments.get("limit", 100)
        
        klines = await self.client.get_klines(symbol, interval, limit)
        
        if not klines:
            return [TextContent(type="text", text="No candlestick data available")]
        
        # Get the latest few candles for display
        latest_candles = klines[-5:]  # Show last 5 candles
        
        response = f"🕯️ **{symbol.upper()} Candlestick Data ({interval} interval)**\n\n"
        response += f"**Showing last 5 of {len(klines)} candles:**\n\n"
        
        for kline in latest_candles:
            open_time = int(kline[0])
            open_price = float(kline[1])
            high_price = float(kline[2])
            low_price = float(kline[3])
            close_price = float(kline[4])
            volume = float(kline[5])
            
            # Determine candle color
            candle_emoji = "🟢" if close_price >= open_price else "🔴"
            
            from datetime import datetime
            time_str = datetime.fromtimestamp(open_time / 1000).strftime("%Y-%m-%d %H:%M")
            
            response += f"{candle_emoji} **{time_str}**\n"
            response += f"   O: ${open_price:,.2f} | H: ${high_price:,.2f} | L: ${low_price:,.2f} | C: ${close_price:,.2f}\n"
            response += f"   Volume: {volume:,.2f}\n\n"
        
        # Add summary statistics
        all_closes = [float(kline[4]) for kline in klines]
        all_volumes = [float(kline[5]) for kline in klines]
        
        avg_price = sum(all_closes) / len(all_closes)
        avg_volume = sum(all_volumes) / len(all_volumes)
        price_change = ((all_closes[-1] - all_closes[0]) / all_closes[0]) * 100
        
        response += f"**📈 Summary ({len(klines)} {interval} candles)**\n"
        response += f"• Average Price: ${avg_price:,.2f}\n"
        response += f"• Average Volume: {avg_volume:,.2f}\n"
        response += f"• Total Price Change: {price_change:+.2f}%"
        
        return [TextContent(type="text", text=response)]
    
    async def _get_account_balance(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Get account balance tool implementation."""
        try:
            balances = await self.client.get_account_balance()
            
            if not balances:
                return [TextContent(type="text", text="No balances found or API credentials not configured")]
            
            response = "💼 **Account Balance**\n\n"
            
            # Sort by total value (free + locked)
            sorted_balances = sorted(
                balances, 
                key=lambda x: float(x.free) + float(x.locked), 
                reverse=True
            )
            
            for balance in sorted_balances:
                free = float(balance.free)
                locked = float(balance.locked)
                total = free + locked
                
                if total > 0:  # Only show non-zero balances
                    response += f"**{balance.asset}**\n"
                    response += f"  Free: {free:,.6f}\n"
                    if locked > 0:
                        response += f"  Locked: {locked:,.6f}\n"
                    response += f"  Total: {total:,.6f}\n\n"
            
            return [TextContent(type="text", text=response)]
            
        except ValueError as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _get_exchange_info(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Get exchange info tool implementation."""
        symbol = arguments.get("symbol")
        
        exchange_info = await self.client.get_exchange_info(symbol)
        
        if symbol:
            # Show detailed info for specific symbol
            response = f"ℹ️ **Exchange Info for {symbol.upper()}**\n\n"
            response += f"• **Status:** {exchange_info.get('status', 'N/A')}\n"
            response += f"• **Base Asset:** {exchange_info.get('baseAsset', 'N/A')}\n"
            response += f"• **Quote Asset:** {exchange_info.get('quoteAsset', 'N/A')}\n"
            
            # Show filters
            filters = exchange_info.get('filters', [])
            if filters:
                response += "\n**Trading Filters:**\n"
                for filter_info in filters[:5]:  # Show first 5 filters
                    filter_type = filter_info.get('filterType', 'Unknown')
                    response += f"• {filter_type}\n"
                    
        else:
            # Show general exchange info
            response = "ℹ️ **Binance Exchange Information**\n\n"
            response += f"• **Server Time:** {exchange_info.get('serverTime', 'N/A')}\n"
            response += f"• **Rate Limits:** {len(exchange_info.get('rateLimits', []))} configured\n"
            response += f"• **Exchange Filters:** {len(exchange_info.get('exchangeFilters', []))} active\n"
            response += f"• **Total Symbols:** {len(exchange_info.get('symbols', []))}\n"
            
            # Show some popular symbols
            symbols = exchange_info.get('symbols', [])
            usdt_symbols = [s for s in symbols if s.get('quoteAsset') == 'USDT' and s.get('status') == 'TRADING'][:10]
            
            if usdt_symbols:
                response += "\n**Popular USDT Pairs:**\n"
                for symbol_info in usdt_symbols:
                    response += f"• {symbol_info.get('symbol', 'N/A')}\n"
        
        return [TextContent(type="text", text=response)]