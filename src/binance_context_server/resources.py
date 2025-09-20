"""MCP resources for Binance data."""

import json
import logging
from typing import Any, Sequence
from datetime import datetime

from mcp.types import Resource
from mcp.types import TextContent, ImageContent, EmbeddedResource

from binance_context_server.binance_client import BinanceClientWrapper


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
            ),
            Resource(
                uri="binance://market/recent-trades",
                name="Recent Trades",
                description="Recent trades data for major trading pairs",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/price-statistics",
                name="Price Statistics",
                description="24hr price change statistics for top cryptocurrencies",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/market-cap",
                name="Market Cap Leaders",
                description="Cryptocurrencies ranked by market capitalization",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/fear-greed",
                name="Market Sentiment",
                description="Market sentiment analysis based on price movements",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/technical-analysis",
                name="Technical Analysis",
                description="Technical indicators and analysis for major pairs",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/defi-tokens",
                name="DeFi Tokens",
                description="DeFi tokens performance and statistics",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/layer1-coins",
                name="Layer 1 Coins",
                description="Layer 1 blockchain coins performance",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/meme-coins",
                name="Meme Coins",
                description="Meme coins and their market performance",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/stablecoins",
                name="Stablecoins",
                description="Stablecoin market data and statistics",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/price-alerts",
                name="Price Alerts",
                description="Active price alerts and significant movements",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/market-depth",
                name="Market Depth",
                description="Market depth analysis for major trading pairs",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/correlation-matrix",
                name="Correlation Matrix",
                description="Price correlation analysis between major cryptocurrencies",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/liquidity-ranking",
                name="Liquidity Ranking",
                description="Cryptocurrencies ranked by market liquidity",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/volatility-index",
                name="Volatility Index",
                description="Market volatility analysis and ranking",
                mimeType="application/json"
            ),
            Resource(
                uri="binance://market/sector-performance",
                name="Sector Performance",
                description="Performance analysis by cryptocurrency sectors",
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
            elif uri == "binance://market/recent-trades":
                return await self._get_recent_trades()
            elif uri == "binance://market/price-statistics":
                return await self._get_price_statistics()
            elif uri == "binance://market/market-cap":
                return await self._get_market_cap()
            elif uri == "binance://market/fear-greed":
                return await self._get_fear_greed()
            elif uri == "binance://market/technical-analysis":
                return await self._get_technical_analysis()
            elif uri == "binance://market/defi-tokens":
                return await self._get_defi_tokens()
            elif uri == "binance://market/layer1-coins":
                return await self._get_layer1_coins()
            elif uri == "binance://market/meme-coins":
                return await self._get_meme_coins()
            elif uri == "binance://market/stablecoins":
                return await self._get_stablecoins()
            elif uri == "binance://market/price-alerts":
                return await self._get_price_alerts()
            elif uri == "binance://market/market-depth":
                return await self._get_market_depth()
            elif uri == "binance://market/correlation-matrix":
                return await self._get_correlation_matrix()
            elif uri == "binance://market/liquidity-ranking":
                return await self._get_liquidity_ranking()
            elif uri == "binance://market/volatility-index":
                return await self._get_volatility_index()
            elif uri == "binance://market/sector-performance":
                return await self._get_sector_performance()
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
    
    async def _get_recent_trades(self) -> str:
        """Get recent trades for major trading pairs."""
        try:
            major_pairs = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
            trades_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "recent_trades": []
            }
            
            for symbol in major_pairs:
                try:
                    trades = await self.client.get_recent_trades(symbol, 5)
                    trades_data["recent_trades"].append({
                        "symbol": symbol,
                        "trades": [
                            {
                                "price": float(trade['price']),
                                "quantity": float(trade['qty']),
                                "time": int(trade['time']),
                                "is_buyer_maker": trade['isBuyerMaker']
                            }
                            for trade in trades
                        ]
                    })
                except Exception as e:
                    logger.warning(f"Could not get trades for {symbol}: {e}")
                    continue
            
            return json.dumps(trades_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting recent trades: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_price_statistics(self) -> str:
        """Get price statistics for top cryptocurrencies."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Sort by quote volume
            sorted_tickers = sorted(usdt_tickers, key=lambda x: float(x.quoteVolume), reverse=True)[:30]
            
            price_stats = {
                "timestamp": datetime.utcnow().isoformat(),
                "statistics": {
                    "total_symbols": len(usdt_tickers),
                    "positive_count": sum(1 for t in usdt_tickers if float(t.priceChangePercent) > 0),
                    "negative_count": sum(1 for t in usdt_tickers if float(t.priceChangePercent) < 0),
                    "neutral_count": sum(1 for t in usdt_tickers if float(t.priceChangePercent) == 0)
                },
                "top_performers": [
                    {
                        "symbol": t.symbol,
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.quoteVolume)
                    }
                    for t in sorted_tickers
                ]
            }
            
            return json.dumps(price_stats, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting price statistics: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_market_cap(self) -> str:
        """Get market cap leaders (using volume as proxy)."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Sort by quote volume (proxy for market cap)
            market_cap_leaders = sorted(usdt_tickers, key=lambda x: float(x.quoteVolume), reverse=True)[:25]
            
            market_cap_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "market_cap_leaders": [
                    {
                        "rank": i + 1,
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.quoteVolume),
                        "market_dominance_score": float(t.quoteVolume) / sum(float(t.quoteVolume) for t in market_cap_leaders) * 100
                    }
                    for i, t in enumerate(market_cap_leaders)
                ]
            }
            
            return json.dumps(market_cap_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting market cap leaders: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_fear_greed(self) -> str:
        """Get market sentiment analysis."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Calculate market sentiment metrics
            total_volume = sum(float(t.quoteVolume) for t in usdt_tickers)
            positive_volume = sum(float(t.quoteVolume) for t in usdt_tickers if float(t.priceChangePercent) > 0)
            negative_volume = sum(float(t.quoteVolume) for t in usdt_tickers if float(t.priceChangePercent) < 0)
            
            # Calculate fear & greed index (simplified)
            positive_ratio = positive_volume / total_volume if total_volume > 0 else 0.5
            fear_greed_score = int(positive_ratio * 100)
            
            # Determine sentiment level
            if fear_greed_score >= 75:
                sentiment = "Extreme Greed"
            elif fear_greed_score >= 55:
                sentiment = "Greed"
            elif fear_greed_score >= 45:
                sentiment = "Neutral"
            elif fear_greed_score >= 25:
                sentiment = "Fear"
            else:
                sentiment = "Extreme Fear"
            
            fear_greed_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "fear_greed_index": fear_greed_score,
                "sentiment": sentiment,
                "market_metrics": {
                    "total_volume_24h": total_volume,
                    "positive_volume_24h": positive_volume,
                    "negative_volume_24h": negative_volume,
                    "positive_volume_ratio": positive_ratio,
                    "total_symbols": len(usdt_tickers)
                },
                "analysis": {
                    "market_trend": "Bullish" if positive_ratio > 0.6 else "Bearish" if positive_ratio < 0.4 else "Sideways",
                    "volatility_level": "High" if abs(fear_greed_score - 50) > 30 else "Medium" if abs(fear_greed_score - 50) > 15 else "Low"
                }
            }
            
            return json.dumps(fear_greed_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting fear greed index: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_technical_analysis(self) -> str:
        """Get technical analysis for major pairs."""
        try:
            major_pairs = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
            technical_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "technical_analysis": []
            }
            
            for symbol in major_pairs:
                try:
                    # Get klines for technical analysis
                    klines = await self.client.get_klines(symbol, '1h', 100)
                    
                    if len(klines) >= 20:
                        closes = [float(kline[4]) for kline in klines]
                        volumes = [float(kline[5]) for kline in klines]
                        
                        # Calculate basic indicators
                        sma_20 = sum(closes[-20:]) / 20
                        sma_50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else None
                        current_price = closes[-1]
                        
                        # Calculate RSI
                        rsi = self._calculate_rsi(closes)
                        
                        # Volume analysis
                        avg_volume = sum(volumes[-20:]) / 20
                        current_volume = volumes[-1]
                        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                        
                        technical_data["technical_analysis"].append({
                            "symbol": symbol,
                            "current_price": current_price,
                            "indicators": {
                                "sma_20": sma_20,
                                "sma_50": sma_50,
                                "rsi_14": rsi,
                                "volume_ratio": volume_ratio
                            },
                            "signals": {
                                "trend": "Bullish" if current_price > sma_20 else "Bearish",
                                "rsi_signal": "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral",
                                "volume_signal": "High" if volume_ratio > 1.5 else "Low" if volume_ratio < 0.5 else "Normal"
                            }
                        })
                        
                except Exception as e:
                    logger.warning(f"Could not analyze {symbol}: {e}")
                    continue
            
            return json.dumps(technical_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting technical analysis: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_defi_tokens(self) -> str:
        """Get DeFi tokens performance."""
        try:
            # Common DeFi tokens on Binance
            defi_symbols = ['UNIUSDT', 'AAVEUSDT', 'COMPUSDT', 'SUSHIUSDT', 'CRVUSDT', 'YFIUSDT', '1INCHUSDT', 'SNXUSDT']
            
            all_tickers = await self.client.get_ticker_24hr()
            defi_tickers = [t for t in all_tickers if t.symbol in defi_symbols]
            
            defi_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "defi_tokens": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.quoteVolume),
                        "category": "DeFi"
                    }
                    for t in defi_tickers
                ]
            }
            
            return json.dumps(defi_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting DeFi tokens: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_layer1_coins(self) -> str:
        """Get Layer 1 blockchain coins performance."""
        try:
            # Major Layer 1 coins
            layer1_symbols = ['ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT', 'DOTUSDT', 'AVAXUSDT', 'MATICUSDT', 'ALGOUSDT', 'ATOMUSDT', 'NEARUSDT']
            
            all_tickers = await self.client.get_ticker_24hr()
            layer1_tickers = [t for t in all_tickers if t.symbol in layer1_symbols]
            
            layer1_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "layer1_coins": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.quoteVolume),
                        "category": "Layer 1"
                    }
                    for t in layer1_tickers
                ]
            }
            
            return json.dumps(layer1_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting Layer 1 coins: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_meme_coins(self) -> str:
        """Get meme coins performance."""
        try:
            # Popular meme coins
            meme_symbols = ['DOGEUSDT', 'SHIBUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'BONKUSDT', 'WIFUSDT']
            
            all_tickers = await self.client.get_ticker_24hr()
            meme_tickers = [t for t in all_tickers if t.symbol in meme_symbols]
            
            meme_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "meme_coins": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.quoteVolume),
                        "category": "Meme Coin"
                    }
                    for t in meme_tickers
                ]
            }
            
            return json.dumps(meme_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting meme coins: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_stablecoins(self) -> str:
        """Get stablecoin market data."""
        try:
            # Major stablecoins
            stablecoin_symbols = ['USDTUSDT', 'USDCUSDT', 'BUSDUSDT', 'DAIUSDT', 'TUSDUSDT']
            
            all_tickers = await self.client.get_ticker_24hr()
            stablecoin_tickers = [t for t in all_tickers if t.symbol in stablecoin_symbols]
            
            stablecoin_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "stablecoins": [
                    {
                        "symbol": t.symbol,
                        "base_asset": t.symbol.replace('USDT', ''),
                        "price": float(t.lastPrice),
                        "price_change_24h": float(t.priceChange),
                        "price_change_percent_24h": float(t.priceChangePercent),
                        "volume_24h": float(t.quoteVolume),
                        "category": "Stablecoin",
                        "stability": "Stable" if abs(float(t.priceChangePercent)) < 1 else "Volatile"
                    }
                    for t in stablecoin_tickers
                ]
            }
            
            return json.dumps(stablecoin_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting stablecoins: {e}")
            return json.dumps({"error": str(e)})
    
    def _calculate_rsi(self, prices: list, period: int = 14) -> float:
        """Calculate RSI (Relative Strength Index)."""
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI if not enough data
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [delta if delta > 0 else 0 for delta in deltas]
        losses = [-delta if delta < 0 else 0 for delta in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    async def _get_price_alerts(self) -> str:
        """Get price alerts resource data."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Find significant movers (>5% change)
            significant_movers = []
            for ticker in usdt_tickers:
                change_percent = float(ticker.priceChangePercent)
                if abs(change_percent) >= 5.0:
                    significant_movers.append({
                        "symbol": ticker.symbol,
                        "price": float(ticker.lastPrice),
                        "change_percent": change_percent,
                        "volume": float(ticker.volume),
                        "quote_volume": float(ticker.quoteVolume)
                    })
            
            # Sort by absolute change
            significant_movers.sort(key=lambda x: abs(x["change_percent"]), reverse=True)
            
            return json.dumps({
                "resource_type": "price_alerts",
                "timestamp": datetime.now().isoformat(),
                "total_alerts": len(significant_movers),
                "threshold_percent": 5.0,
                "alerts": significant_movers[:20]  # Top 20 alerts
            })
        except Exception as e:
            logger.error(f"Error getting price alerts: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_market_depth(self) -> str:
        """Get market depth resource data."""
        try:
            # Analyze market depth for major pairs
            major_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
            depth_analysis = []
            
            for symbol in major_pairs:
                try:
                    order_book = await self.client.get_order_book(symbol, 20)
                    
                    # Calculate depth metrics
                    total_bid_volume = sum(float(bid[1]) for bid in order_book.bids)
                    total_ask_volume = sum(float(ask[1]) for ask in order_book.asks)
                    
                    best_bid = float(order_book.bids[0][0])
                    best_ask = float(order_book.asks[0][0])
                    spread = best_ask - best_bid
                    spread_percent = (spread / best_bid) * 100
                    
                    depth_ratio = total_bid_volume / total_ask_volume if total_ask_volume > 0 else 0
                    
                    depth_analysis.append({
                        "symbol": symbol,
                        "best_bid": best_bid,
                        "best_ask": best_ask,
                        "spread": spread,
                        "spread_percent": spread_percent,
                        "total_bid_volume": total_bid_volume,
                        "total_ask_volume": total_ask_volume,
                        "depth_ratio": depth_ratio,
                        "liquidity_score": "high" if depth_ratio > 1.2 else "low" if depth_ratio < 0.8 else "medium"
                    })
                except Exception as e:
                    logger.warning(f"Could not get depth data for {symbol}: {e}")
            
            return json.dumps({
                "resource_type": "market_depth",
                "timestamp": datetime.now().isoformat(),
                "pairs_analyzed": len(depth_analysis),
                "depth_analysis": depth_analysis
            })
        except Exception as e:
            logger.error(f"Error getting market depth: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_correlation_matrix(self) -> str:
        """Get correlation matrix resource data."""
        try:
            # Get top cryptocurrencies for correlation analysis
            major_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT", "AVAXUSDT", "MATICUSDT"]
            correlation_data = {}
            
            # Get price changes for all pairs
            for symbol in major_pairs:
                try:
                    ticker_data = await self.client.get_ticker_24hr(symbol)
                    if ticker_data:
                        correlation_data[symbol] = float(ticker_data[0].priceChangePercent)
                except Exception as e:
                    logger.warning(f"Could not get data for {symbol}: {e}")
                    correlation_data[symbol] = 0
            
            # Calculate correlation matrix (simplified)
            correlation_matrix = {}
            symbols = list(correlation_data.keys())
            
            for i, sym1 in enumerate(symbols):
                correlation_matrix[sym1] = {}
                for j, sym2 in enumerate(symbols):
                    if i == j:
                        correlation_matrix[sym1][sym2] = 1.0
                    else:
                        # Simple correlation based on direction
                        price1, price2 = correlation_data[sym1], correlation_data[sym2]
                        if (price1 > 0 and price2 > 0) or (price1 < 0 and price2 < 0):
                            correlation_matrix[sym1][sym2] = 0.7  # Positive correlation
                        elif (price1 > 0 and price2 < 0) or (price1 < 0 and price2 > 0):
                            correlation_matrix[sym1][sym2] = -0.7  # Negative correlation
                        else:
                            correlation_matrix[sym1][sym2] = 0.0  # No correlation
            
            return json.dumps({
                "resource_type": "correlation_matrix",
                "timestamp": datetime.now().isoformat(),
                "symbols": symbols,
                "price_changes": correlation_data,
                "correlation_matrix": correlation_matrix
            })
        except Exception as e:
            logger.error(f"Error getting correlation matrix: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_liquidity_ranking(self) -> str:
        """Get liquidity ranking resource data."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Calculate liquidity scores based on volume and spread
            liquidity_rankings = []
            
            for ticker in usdt_tickers[:50]:  # Analyze top 50 by volume
                try:
                    # Get order book for spread calculation
                    order_book = await self.client.get_order_book(ticker.symbol, 5)
                    
                    best_bid = float(order_book.bids[0][0])
                    best_ask = float(order_book.asks[0][0])
                    spread_percent = ((best_ask - best_bid) / best_bid) * 100
                    
                    # Calculate liquidity score (higher volume, lower spread = higher score)
                    volume_score = float(ticker.quoteVolume)
                    spread_score = 1 / (1 + spread_percent)  # Lower spread = higher score
                    liquidity_score = volume_score * spread_score
                    
                    liquidity_rankings.append({
                        "symbol": ticker.symbol,
                        "price": float(ticker.lastPrice),
                        "volume_24h": float(ticker.volume),
                        "quote_volume_24h": float(ticker.quoteVolume),
                        "spread_percent": spread_percent,
                        "liquidity_score": liquidity_score
                    })
                except Exception as e:
                    logger.warning(f"Could not analyze liquidity for {ticker.symbol}: {e}")
            
            # Sort by liquidity score
            liquidity_rankings.sort(key=lambda x: x["liquidity_score"], reverse=True)
            
            return json.dumps({
                "resource_type": "liquidity_ranking",
                "timestamp": datetime.now().isoformat(),
                "total_analyzed": len(liquidity_rankings),
                "rankings": liquidity_rankings[:20]  # Top 20 by liquidity
            })
        except Exception as e:
            logger.error(f"Error getting liquidity ranking: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_volatility_index(self) -> str:
        """Get volatility index resource data."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Calculate volatility based on 24h price range
            volatility_rankings = []
            
            for ticker in usdt_tickers:
                high_price = float(ticker.highPrice)
                low_price = float(ticker.lowPrice)
                current_price = float(ticker.lastPrice)
                
                # Calculate volatility as percentage of price range
                price_range = high_price - low_price
                volatility_percent = (price_range / current_price) * 100 if current_price > 0 else 0
                
                volatility_rankings.append({
                    "symbol": ticker.symbol,
                    "price": current_price,
                    "high_24h": high_price,
                    "low_24h": low_price,
                    "price_range": price_range,
                    "volatility_percent": volatility_percent,
                    "volume_24h": float(ticker.volume)
                })
            
            # Sort by volatility (highest first)
            volatility_rankings.sort(key=lambda x: x["volatility_percent"], reverse=True)
            
            # Calculate market volatility index
            top_volatile = volatility_rankings[:20]
            avg_volatility = sum(item["volatility_percent"] for item in top_volatile) / len(top_volatile)
            
            return json.dumps({
                "resource_type": "volatility_index",
                "timestamp": datetime.now().isoformat(),
                "market_volatility_index": avg_volatility,
                "total_analyzed": len(volatility_rankings),
                "most_volatile": volatility_rankings[:15],  # Top 15 most volatile
                "least_volatile": volatility_rankings[-10:]  # Top 10 least volatile
            })
        except Exception as e:
            logger.error(f"Error getting volatility index: {e}")
            return json.dumps({"error": str(e)})
    
    async def _get_sector_performance(self) -> str:
        """Get sector performance resource data."""
        try:
            all_tickers = await self.client.get_ticker_24hr()
            usdt_tickers = [t for t in all_tickers if t.symbol.endswith('USDT')]
            
            # Define sectors
            sectors = {
                "Layer 1": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT", "DOTUSDT", "AVAXUSDT", "MATICUSDT", "ALGOUSDT", "ATOMUSDT"],
                "DeFi": ["UNIUSDT", "AAVEUSDT", "COMPUSDT", "SUSHIUSDT", "CRVUSDT", "YFIUSDT", "1INCHUSDT", "SNXUSDT"],
                "Meme": ["DOGEUSDT", "SHIBUSDT", "PEPEUSDT", "FLOKIUSDT", "BONKUSDT", "WIFUSDT"],
                "Stablecoins": ["USDTUSDT", "USDCUSDT", "BUSDUSDT", "DAIUSDT", "TUSDUSDT"],
                "Gaming": ["AXSUSDT", "SANDUSDT", "MANAUSDT", "GALAUSDT", "ILVUSDT"],
                "Storage": ["FILUSDT", "ARUSDT", "SCUSDT"]
            }
            
            sector_performance = {}
            
            for sector_name, symbols in sectors.items():
                sector_tickers = [t for t in usdt_tickers if t.symbol in symbols]
                
                if sector_tickers:
                    total_change = sum(float(t.priceChangePercent) for t in sector_tickers)
                    avg_change = total_change / len(sector_tickers)
                    total_volume = sum(float(t.volume) for t in sector_tickers)
                    
                    sector_performance[sector_name] = {
                        "symbols_count": len(sector_tickers),
                        "average_change_percent": avg_change,
                        "total_volume_24h": total_volume,
                        "top_performer": max(sector_tickers, key=lambda x: float(x.priceChangePercent)).symbol,
                        "worst_performer": min(sector_tickers, key=lambda x: float(x.priceChangePercent)).symbol,
                        "symbols": [t.symbol for t in sector_tickers]
                    }
            
            return json.dumps({
                "resource_type": "sector_performance",
                "timestamp": datetime.now().isoformat(),
                "sectors_analyzed": len(sector_performance),
                "sector_performance": sector_performance
            })
        except Exception as e:
            logger.error(f"Error getting sector performance: {e}")
            return json.dumps({"error": str(e)})
