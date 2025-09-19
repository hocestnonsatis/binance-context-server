"""MCP resources for Binance data."""

import json
import logging
from typing import Any, Sequence
from datetime import datetime

from mcp.types import Resource
from mcp.types import TextContent, ImageContent, EmbeddedResource

from .binance_client import BinanceClientWrapper


logger = logging.getLogger(__name__)


class BinanceResources:
    """Binance MCP resources."""
    
    def __init__(self, client: BinanceClientWrapper):
        """Initialize resources with Binance client.
        
        Args:
            client: Binance client wrapper
        """
        self.client = client
    
    async def list_resources(self) -> list[Resource]:
        """List available resources.
        
        Returns:
            List of MCP resources
        """
        return [
            Resource(
                uri="binance://market/overview",
                name="Market Overview",
                description="Current cryptocurrency market overview with top performers",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/top-gainers",
                name="Top Gainers",
                description="Top gaining cryptocurrencies in the last 24 hours",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/top-losers",
                name="Top Losers",
                description="Top losing cryptocurrencies in the last 24 hours",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/volume-leaders",
                name="Volume Leaders",
                description="Cryptocurrencies with highest trading volume",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://exchange/info",
                name="Exchange Information",
                description="Binance exchange trading rules and symbol information",
                mimeType="application/json"
            )
        ]
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource by URI.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource content as JSON string
        """
        try:
            if uri == "binance://market/overview":
                return await self._get_market_overview()
            elif uri == "binance://market/top-gainers":
                return await self._get_top_gainers()
            elif uri == "binance://market/top-losers":
                return await self._get_top_losers()
            elif uri == "binance://market/volume-leaders":
                return await self._get_volume_leaders()
            elif uri == "binance://exchange/info":
                return await self._get_exchange_info()
            else:
                return json.dumps({"error": f"Unknown resource URI: {uri}"})
                
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_market_overview(self) -> str:
        """Get market overview data."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Sort by market cap (using quote volume as proxy)
            sorted_tickers = sorted(usdt_tickers, key=lambda x: float(x.quoteVolume), reverse=True)[:20]
            
            # Calculate market statistics
            total_volume = sum(float(t.quoteVolume) for t in usdt_tickers)
            positive_count = sum(1 for t in usdt_tickers if float(t.priceChangePercent) > 0)
            negative_count = sum(1 for t in usdt_tickers if float(t.priceChangePercent) < 0)
            neutral_count = len(usdt_tickers) - positive_count - negative_count
            
            overview = {
                "timestamp": datetime.utcnow().isoformat(),
                "market_stats": {
                    "total_symbols": len(usdt_tickers),
                    "total_volume_24h": total_volume,
                    "positive_count": positive_count,
                    "negative_count": negative_count,
                    "neutral_count": neutral_count,
                    "market_sentiment": "bullish" if positive_count > negative_count else "bearish" if negative_count > positive_count else "neutral"
                },
                "top_performers": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.volume),
                        "quote_volume_24h": float(t.quoteVolume),
                        "high_24h": float(t.highPrice),
                        "low_24h": float(t.lowPrice)
                    }
                    for t in sorted_tickers[:10]
                ]
            }
            
            return json.dumps(overview, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting market overview: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_top_gainers(self) -> str:
        """Get top gaining cryptocurrencies."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Filter and sort by price change percentage
            gainers = [t for t in usdt_tickers if float(t.priceChangePercent) > 0]
            sorted_gainers = sorted(gainers, key=lambda x: float(x.priceChangePercent), reverse=True)[:20]
            
            gainers_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "count": len(sorted_gainers),
                "gainers": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.volume),
                        "quote_volume_24h": float(t.quoteVolume),
                        "high_24h": float(t.highPrice),
                        "low_24h": float(t.lowPrice)
                    }
                    for t in sorted_gainers
                ]
            }
            
            return json.dumps(gainers_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting top gainers: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_top_losers(self) -> str:
        """Get top losing cryptocurrencies."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Filter and sort by price change percentage (ascending for losers)
            losers = [t for t in usdt_tickers if float(t.priceChangePercent) < 0]
            sorted_losers = sorted(losers, key=lambda x: float(x.priceChangePercent))[:20]
            
            losers_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "count": len(sorted_losers),
                "losers": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.volume),
                        "quote_volume_24h": float(t.quoteVolume),
                        "high_24h": float(t.highPrice),
                        "low_24h": float(t.lowPrice)
                    }
                    for t in sorted_losers
                ]
            }
            
            return json.dumps(losers_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting top losers: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_volume_leaders(self) -> str:
        """Get cryptocurrencies with highest trading volume."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Sort by quote volume (descending)
            sorted_by_volume = sorted(usdt_tickers, key=lambda x: float(x.quoteVolume), reverse=True)[:20]
            
            volume_leaders_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "count": len(sorted_by_volume),
                "volume_leaders": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.volume),
                        "quote_volume_24h": float(t.quoteVolume),
                        "high_24h": float(t.highPrice),
                        "low_24h": float(t.lowPrice)
                    }
                    for t in sorted_by_volume
                ]
            }
            
            return json.dumps(volume_leaders_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting volume leaders: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_exchange_info(self) -> str:
        """Get exchange information."""
        try:
            exchange_info = await self.client.get_exchange_info()
            
            # Extract key information
            exchange_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "server_time": exchange_info.get('serverTime'),
                "timezone": exchange_info.get('timezone'),
                "rate_limits": exchange_info.get('rateLimits', []),
                "exchange_filters": exchange_info.get('exchangeFilters', []),
                "symbols_count": len(exchange_info.get('symbols', [])),
                "symbols": [
                    {
                        "symbol": s.get('symbol'),
                        "status": s.get('status'),
                        "base_asset": s.get('baseAsset'),
                        "quote_asset": s.get('quoteAsset'),
                        "is_spot_trading_allowed": s.get('isSpotTradingAllowed', False),
                        "is_margin_trading_allowed": s.get('isMarginTradingAllowed', False)
                    }
                    for s in exchange_info.get('symbols', [])[:50]  # Limit to first 50 symbols
                ]
            }
            
            return json.dumps(exchange_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting exchange info: {e}")
            return json.dumps({"error": str(e)})
