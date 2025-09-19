"""Binance API client wrapper for MCP server."""

import os
import logging
from typing import Dict, List, Optional, Any
from decimal import Decimal

from binance.client import Client
from binance.exceptions import BinanceAPIException
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class MarketData(BaseModel):
    """Market data model."""
    symbol: str
    lastPrice: str
    priceChange: str
    priceChangePercent: str
    highPrice: str
    lowPrice: str
    volume: str
    quoteVolume: str
    openTime: int
    closeTime: int


class OrderBookData(BaseModel):
    """Order book data model."""
    symbol: str
    bids: List[List[str]]
    asks: List[List[str]]
    last_update_id: int


class AccountBalance(BaseModel):
    """Account balance model."""
    asset: str
    free: str
    locked: str


class BinanceClientWrapper:
    """Wrapper for Binance API client with error handling."""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = False):
        """Initialize Binance client.
        
        Args:
            api_key: Binance API key (optional for public data)
            api_secret: Binance API secret (optional for public data)
            testnet: Whether to use testnet
        """
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        self.testnet = testnet
        
        try:
            if self.api_key and self.api_secret:
                self.client = Client(
                    api_key=self.api_key,
                    api_secret=self.api_secret,
                    testnet=self.testnet
                )
                logger.info("Binance client initialized with API credentials")
            else:
                self.client = Client(testnet=self.testnet)
                logger.info("Binance client initialized for public data only")
                
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    async def get_ticker_24hr(self, symbol: Optional[str] = None) -> List[MarketData]:
        """Get 24hr ticker price change statistics.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT). If None, returns all symbols.
            
        Returns:
            List of market data
        """
        try:
            if symbol:
                data = self.client.get_ticker(symbol=symbol.upper())
                return [MarketData(**data)]
            else:
                data = self.client.get_ticker()
                return [MarketData(**item) for item in data]
                
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting ticker: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting ticker: {e}")
            raise
    
    async def get_symbol_price(self, symbol: str) -> Dict[str, str]:
        """Get current price for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            
        Returns:
            Price data
        """
        try:
            data = self.client.get_symbol_ticker(symbol=symbol.upper())
            return data
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting price: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting price: {e}")
            raise
    
    async def get_order_book(self, symbol: str, limit: int = 100) -> OrderBookData:
        """Get order book for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            limit: Number of entries to return (default 100)
            
        Returns:
            Order book data
        """
        try:
            data = self.client.get_order_book(symbol=symbol.upper(), limit=limit)
            return OrderBookData(
                symbol=symbol.upper(),
                bids=data['bids'],
                asks=data['asks'],
                last_update_id=data['lastUpdateId']
            )
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting order book: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting order book: {e}")
            raise
    
    async def get_klines(self, symbol: str, interval: str = '1h', limit: int = 100) -> List[List[Any]]:
        """Get kline/candlestick data.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            interval: Kline interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
            limit: Number of klines to return (default 100)
            
        Returns:
            List of kline data
        """
        try:
            data = self.client.get_klines(
                symbol=symbol.upper(),
                interval=interval,
                limit=limit
            )
            return data
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting klines: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting klines: {e}")
            raise
    
    async def get_account_balance(self) -> List[AccountBalance]:
        """Get account balance (requires API credentials).
        
        Returns:
            List of account balances
        """
        if not (self.api_key and self.api_secret):
            raise ValueError("API credentials required for account data")
            
        try:
            account_info = self.client.get_account()
            balances = []
            
            for balance in account_info['balances']:
                if float(balance['free']) > 0 or float(balance['locked']) > 0:
                    balances.append(AccountBalance(**balance))
                    
            return balances
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting account balance: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting account balance: {e}")
            raise
    
    async def get_exchange_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get exchange trading rules and symbol information.
        
        Args:
            symbol: Specific symbol to get info for (optional)
            
        Returns:
            Exchange information
        """
        try:
            if symbol:
                data = self.client.get_exchange_info()
                for symbol_info in data['symbols']:
                    if symbol_info['symbol'] == symbol.upper():
                        return symbol_info
                raise ValueError(f"Symbol {symbol} not found")
            else:
                return self.client.get_exchange_info()
                
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting exchange info: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting exchange info: {e}")
            raise
    
    async def get_recent_trades(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent trades for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            limit: Number of trades to return (max 1000)
            
        Returns:
            List of recent trades
        """
        try:
            data = self.client.get_recent_trades(symbol=symbol.upper(), limit=limit)
            return data
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting recent trades: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting recent trades: {e}")
            raise
    
    async def get_historical_trades(self, symbol: str, limit: int = 100, from_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get historical trades for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            limit: Number of trades to return (max 1000)
            from_id: Trade ID to fetch from (optional)
            
        Returns:
            List of historical trades
        """
        if not (self.api_key and self.api_secret):
            raise ValueError("API credentials required for historical trades")
            
        try:
            kwargs = {'symbol': symbol.upper(), 'limit': limit}
            if from_id:
                kwargs['fromId'] = from_id
                
            data = self.client.get_historical_trades(**kwargs)
            return data
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting historical trades: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting historical trades: {e}")
            raise
    
    async def get_avg_price(self, symbol: str) -> Dict[str, Any]:
        """Get current average price for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            
        Returns:
            Average price data
        """
        try:
            data = self.client.get_avg_price(symbol=symbol.upper())
            return data
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting avg price: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting avg price: {e}")
            raise
    
    async def get_price_change_statistics(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """Get 24hr ticker price change statistics for multiple symbols.
        
        Args:
            symbols: List of trading pair symbols
            
        Returns:
            List of ticker statistics
        """
        try:
            data = self.client.get_ticker()
            # Filter for requested symbols
            filtered_data = [item for item in data if item['symbol'] in [s.upper() for s in symbols]]
            return filtered_data
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting price change statistics: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting price change statistics: {e}")
            raise
    
    async def get_server_time(self) -> Dict[str, Any]:
        """Get Binance server time.
        
        Returns:
            Server time data
        """
        try:
            data = self.client.get_server_time()
            return data
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting server time: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting server time: {e}")
            raise
    
    async def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get detailed information about a trading pair.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            
        Returns:
            Symbol information
        """
        try:
            data = self.client.get_exchange_info()
            for symbol_info in data['symbols']:
                if symbol_info['symbol'] == symbol.upper():
                    return symbol_info
            raise ValueError(f"Symbol {symbol} not found")
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting symbol info: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting symbol info: {e}")
            raise