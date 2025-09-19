"""Tests for BinanceClientWrapper."""

import pytest
from unittest.mock import Mock, patch
from binance_context_server.binance_client import BinanceClientWrapper


class TestBinanceClientWrapper:
    """Test cases for BinanceClientWrapper."""
    
    @pytest.fixture
    def mock_client(self):
        """Mock Binance client."""
        with patch('binance_context_server.binance_client.Client') as mock:
            yield mock.return_value
    
    def test_init_without_credentials(self, mock_client):
        """Test initialization without API credentials."""
        client = BinanceClientWrapper()
        assert client.api_key is None
        assert client.api_secret is None
        assert client.testnet is False
        mock_client.assert_called_once_with(testnet=False)
    
    def test_init_with_credentials(self, mock_client):
        """Test initialization with API credentials."""
        api_key = "test_key"
        api_secret = "test_secret"
        
        client = BinanceClientWrapper(api_key=api_key, api_secret=api_secret)
        assert client.api_key == api_key
        assert client.api_secret == api_secret
        mock_client.assert_called_once_with(
            api_key=api_key,
            api_secret=api_secret,
            testnet=False
        )
    
    def test_init_with_testnet(self, mock_client):
        """Test initialization with testnet enabled."""
        client = BinanceClientWrapper(testnet=True)
        assert client.testnet is True
        mock_client.assert_called_once_with(testnet=True)
    
    @pytest.mark.asyncio
    async def test_get_ticker_24hr_single_symbol(self, mock_client):
        """Test getting ticker for single symbol."""
        mock_data = {
            'symbol': 'BTCUSDT',
            'lastPrice': '50000.00',
            'priceChange': '1000.00',
            'priceChangePercent': '2.04'
        }
        mock_client.get_ticker.return_value = mock_data
        
        client = BinanceClientWrapper()
        result = await client.get_ticker_24hr('BTCUSDT')
        
        assert len(result) == 1
        assert result[0].symbol == 'BTCUSDT'
        assert result[0].lastPrice == '50000.00'
        mock_client.get_ticker.assert_called_once_with(symbol='BTCUSDT')
    
    @pytest.mark.asyncio
    async def test_get_ticker_24hr_all_symbols(self, mock_client):
        """Test getting ticker for all symbols."""
        mock_data = [
            {'symbol': 'BTCUSDT', 'lastPrice': '50000.00'},
            {'symbol': 'ETHUSDT', 'lastPrice': '3000.00'}
        ]
        mock_client.get_ticker.return_value = mock_data
        
        client = BinanceClientWrapper()
        result = await client.get_ticker_24hr()
        
        assert len(result) == 2
        assert result[0].symbol == 'BTCUSDT'
        assert result[1].symbol == 'ETHUSDT'
        mock_client.get_ticker.assert_called_once_with()
    
    @pytest.mark.asyncio
    async def test_get_symbol_price(self, mock_client):
        """Test getting symbol price."""
        mock_data = {'price': '50000.00'}
        mock_client.get_symbol_ticker.return_value = mock_data
        
        client = BinanceClientWrapper()
        result = await client.get_symbol_price('BTCUSDT')
        
        assert result == mock_data
        mock_client.get_symbol_ticker.assert_called_once_with(symbol='BTCUSDT')
    
    @pytest.mark.asyncio
    async def test_get_order_book(self, mock_client):
        """Test getting order book."""
        mock_data = {
            'bids': [['49900.00', '1.5'], ['49800.00', '2.0']],
            'asks': [['50100.00', '1.2'], ['50200.00', '1.8']],
            'lastUpdateId': 12345
        }
        mock_client.get_order_book.return_value = mock_data
        
        client = BinanceClientWrapper()
        result = await client.get_order_book('BTCUSDT', 100)
        
        assert result.symbol == 'BTCUSDT'
        assert result.bids == mock_data['bids']
        assert result.asks == mock_data['asks']
        assert result.last_update_id == 12345
        mock_client.get_order_book.assert_called_once_with(symbol='BTCUSDT', limit=100)
    
    @pytest.mark.asyncio
    async def test_get_account_balance_no_credentials(self, mock_client):
        """Test getting account balance without credentials."""
        client = BinanceClientWrapper()
        
        with pytest.raises(ValueError, match="API credentials required"):
            await client.get_account_balance()
    
    @pytest.mark.asyncio
    async def test_get_account_balance_with_credentials(self, mock_client):
        """Test getting account balance with credentials."""
        mock_account = {
            'balances': [
                {'asset': 'BTC', 'free': '1.0', 'locked': '0.5'},
                {'asset': 'ETH', 'free': '10.0', 'locked': '0.0'}
            ]
        }
        mock_client.get_account.return_value = mock_account
        
        client = BinanceClientWrapper(api_key="test", api_secret="test")
        result = await client.get_account_balance()
        
        assert len(result) == 2
        assert result[0].asset == 'BTC'
        assert result[0].free == '1.0'
        assert result[0].locked == '0.5'
        mock_client.get_account.assert_called_once()
