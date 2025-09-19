"""Tests for BinanceResources."""

import pytest
import json
from unittest.mock import Mock, AsyncMock
from binance_context_server.resources import BinanceResources


class TestBinanceResources:
    """Test cases for BinanceResources."""
    
    @pytest.fixture
    def mock_client(self):
        """Mock Binance client."""
        return Mock()
    
    @pytest.fixture
    def resources(self, mock_client):
        """BinanceResources instance with mocked client."""
        return BinanceResources(mock_client)
    
    @pytest.mark.asyncio
    async def test_list_resources(self, resources):
        """Test listing resources."""
        resource_list = await resources.list_resources()
        assert len(resource_list) == 15
        
        # Check that all expected resources are present
        resource_uris = [resource.uri for resource in resource_list]
        expected_resources = [
            'binance://market/overview',
            'binance://market/top-gainers',
            'binance://market/top-losers',
            'binance://market/volume-leaders',
            'binance://exchange/info',
            'binance://market/recent-trades',
            'binance://market/price-statistics',
            'binance://market/market-cap',
            'binance://market/fear-greed',
            'binance://market/technical-analysis',
            'binance://market/defi-tokens',
            'binance://market/layer1-coins',
            'binance://market/meme-coins',
            'binance://market/stablecoins'
        ]
        
        for expected_resource in expected_resources:
            assert expected_resource in resource_uris
    
    @pytest.mark.asyncio
    async def test_read_resource_market_overview(self, resources, mock_client):
        """Test reading market overview resource."""
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
        
        result = await resources.read_resource('binance://market/overview')
        data = json.loads(result)
        
        assert 'timestamp' in data
        assert 'market_stats' in data
        assert 'top_performers' in data
        assert data['market_stats']['total_symbols'] == 1
        assert len(data['top_performers']) == 1
        assert data['top_performers'][0]['symbol'] == 'BTCUSDT'
    
    @pytest.mark.asyncio
    async def test_read_resource_top_gainers(self, resources, mock_client):
        """Test reading top gainers resource."""
        from binance_context_server.binance_client import MarketData
        
        mock_tickers = [
            MarketData(
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
            ),
            MarketData(
                symbol='ETHUSDT',
                lastPrice='3000.00',
                priceChange='-50.00',
                priceChangePercent='-1.64',
                highPrice='3100.00',
                lowPrice='2900.00',
                volume='2000.0',
                quoteVolume='6000000.0',
                openTime=1234567890000,
                closeTime=1234654290000
            )
        ]
        
        mock_client.get_ticker_24hr = AsyncMock(return_value=mock_tickers)
        
        result = await resources.read_resource('binance://market/top-gainers')
        data = json.loads(result)
        
        assert 'timestamp' in data
        assert 'count' in data
        assert 'gainers' in data
        # Only BTCUSDT should be in gainers (positive price change)
        assert len(data['gainers']) == 1
        assert data['gainers'][0]['symbol'] == 'BTCUSDT'
    
    @pytest.mark.asyncio
    async def test_read_resource_top_losers(self, resources, mock_client):
        """Test reading top losers resource."""
        from binance_context_server.binance_client import MarketData
        
        mock_tickers = [
            MarketData(
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
            ),
            MarketData(
                symbol='ETHUSDT',
                lastPrice='3000.00',
                priceChange='-50.00',
                priceChangePercent='-1.64',
                highPrice='3100.00',
                lowPrice='2900.00',
                volume='2000.0',
                quoteVolume='6000000.0',
                openTime=1234567890000,
                closeTime=1234654290000
            )
        ]
        
        mock_client.get_ticker_24hr = AsyncMock(return_value=mock_tickers)
        
        result = await resources.read_resource('binance://market/top-losers')
        data = json.loads(result)
        
        assert 'timestamp' in data
        assert 'count' in data
        assert 'losers' in data
        # Only ETHUSDT should be in losers (negative price change)
        assert len(data['losers']) == 1
        assert data['losers'][0]['symbol'] == 'ETHUSDT'
    
    @pytest.mark.asyncio
    async def test_read_resource_unknown(self, resources):
        """Test reading unknown resource."""
        result = await resources.read_resource('binance://unknown/resource')
        data = json.loads(result)
        
        assert 'error' in data
        assert 'Unknown resource URI' in data['error']
    
    @pytest.mark.asyncio
    async def test_read_resource_error_handling(self, resources, mock_client):
        """Test error handling in resource reading."""
        mock_client.get_ticker_24hr = AsyncMock(side_effect=Exception("API Error"))
        
        result = await resources.read_resource('binance://market/overview')
        data = json.loads(result)
        
        assert 'error' in data
        assert 'API Error' in data['error']
    
    def test_calculate_rsi(self, resources):
        """Test RSI calculation."""
        # Test with known values that should give RSI around 50
        prices = [100, 101, 99, 102, 98, 103, 97, 104, 96, 105, 95, 106, 94, 107, 93, 108]
        rsi = resources._calculate_rsi(prices)
        
        # RSI should be between 0 and 100
        assert 0 <= rsi <= 100
        
        # Test with insufficient data
        short_prices = [100, 101]
        rsi_short = resources._calculate_rsi(short_prices)
        assert rsi_short == 50.0  # Should return neutral RSI
