
import pytest,requests_mock
from alerts.services.fetch_prices import request_for_prices, APIError

comma = ','
def test_valid_stock_symbol_returns_prices(requests_mock:requests_mock):
    symbols = ["AAPL",'MSFT','GOOGL','TSLA','AMZN','META','NVDA','JPM','JNJ','PG']
    mocked_prices = ["195.64","200.00","40.04","75.90","30.02","195.64","200.00","40.04","75.90","30.02"]
    url = f"https://api.twelvedata.com/price?symbol={comma.join(symbols)}&apikey=demo"
    
    mocked_response = {
        symbol:{'price':price} for symbol,price in zip(symbols, mocked_prices)
    }
    
    requests_mock.get(url, json = mocked_response)
    

    symbols_prices = request_for_prices(symbols)
   
    for symbol in symbols:
        assert symbols_prices[symbol] == float(mocked_response[symbol]['price'])

