"""Tests for BinanceTools."""

import pytest
from unittest.mock import Mock, AsyncMock
from binance_context_server.tools import BinanceTools


class TestBinanceTools:
    """Test cases for BinanceTools."""
    
    @pytest.fixture
    def mock_client(self):
        """Mock Binance client."""
        return Mock()
    
    @pytest.fixture
    def tools(self, mock_client):
        """BinanceTools instance with mocked client."""
        return BinanceTools(mock_client)
    
    def test_get_tools(self, tools):
        """Test getting list of tools."""
        tool_list = tools.get_tools()
        assert len(tool_list) == 17
        
        # Check that all expected tools are present
        tool_names = [tool.name for tool in tool_list]
        expected_tools = [
            'get_crypto_price',
            'get_market_stats', 
            'get_top_cryptocurrencies',
            'get_order_book',
            'get_candlestick_data',
            'get_account_balance',
            'get_exchange_info',
            'get_recent_trades',
            'get_historical_trades',
            'get_avg_price',
            'get_price_change_statistics',
            'get_24hr_ticker',
            'get_server_time',
            'get_symbol_info',
            'get_klines_with_indicators',
            'search_symbols'
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names
    
    @pytest.mark.asyncio
    async def test_call_tool_get_crypto_price(self, tools, mock_client):
        """Test calling get_crypto_price tool."""
        mock_client.get_symbol_price = AsyncMock(return_value={'price': '50000.00'})
        
        result = await tools.call_tool('get_crypto_price', {'symbol': 'BTCUSDT'})
        
        assert len(result) == 1
        assert result[0].type == 'text'
        assert 'BTCUSDT Price' in result[0].text
        assert '$50,000.00' in result[0].text
        mock_client.get_symbol_price.assert_called_once_with('BTCUSDT')
    
    @pytest.mark.asyncio
    async def test_call_tool_get_market_stats(self, tools, mock_client):
        """Test calling get_market_stats tool."""
        from binance_context_server.binance_client import MarketData
        
        mock_ticker = MarketData(
            symbol='BTCUSDT',
            lastPrice='50000.00',
            priceChange='1000.00',
            priceChangePercent='2.04',
            highPrice='51000.00',
            lowPrice='49000.00',
            volume='1000.0',
            quoteVolume='50000000.0',
            openTime=1234567890000,
            closeTime=1234654290000
        )
        
        mock_client.get_ticker_24hr = AsyncMock(return_value=[mock_ticker])
        
        result = await tools.call_tool('get_market_stats', {'symbol': 'BTCUSDT'})
        
        assert len(result) == 1
        assert result[0].type == 'text'
        assert 'BTCUSDT - 24hr Market Stats' in result[0].text
        assert '$50,000.00' in result[0].text
        assert '+2.04%' in result[0].text
        mock_client.get_ticker_24hr.assert_called_once_with('BTCUSDT')
    
    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool(self, tools):
        """Test calling unknown tool."""
        result = await tools.call_tool('unknown_tool', {})
        
        assert len(result) == 1
        assert result[0].type == 'text'
        assert 'Unknown tool: unknown_tool' in result[0].text
    
    @pytest.mark.asyncio
    async def test_call_tool_error_handling(self, tools, mock_client):
        """Test error handling in tool calls."""
        mock_client.get_symbol_price = AsyncMock(side_effect=Exception("API Error"))
        
        result = await tools.call_tool('get_crypto_price', {'symbol': 'BTCUSDT'})
        
        assert len(result) == 1
        assert result[0].type == 'text'
        assert 'Error: API Error' in result[0].text
    
    def test_calculate_rsi(self, tools):
        """Test RSI calculation."""
        # Test with known values that should give RSI around 50
        prices = [100, 101, 99, 102, 98, 103, 97, 104, 96, 105, 95, 106, 94, 107, 93, 108]
        rsi = tools._calculate_rsi(prices)
        
        # RSI should be between 0 and 100
        assert 0 <= rsi <= 100
        
        # Test with insufficient data
        short_prices = [100, 101]
        rsi_short = tools._calculate_rsi(short_prices)
        assert rsi_short is None
