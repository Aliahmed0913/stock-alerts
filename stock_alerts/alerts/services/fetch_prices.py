from stock_alerts.settings import API_KEY

import requests, logging
logger = logging.getLogger('alerts')


def request_for_prices(stock_symbols:list[str]):
    prices = {}
    for symbol in stock_symbols:
        try:
            twelvedata_url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
            response = requests.get(twelvedata_url, timeout=5)
            
            response.raise_for_status()
            symbol_price = response.json()

            if 'price' in symbol_price:
                prices[symbol] = float(symbol_price['price'])
                logger.warning("{%s} Price: %s", symbol,prices[symbol])
            else:
                logger.warning("Price not found in API response for %s: %s", symbol, symbol_price)
                continue  

    
        except requests.exceptions.RequestException as e:
            logger.error(f'API fetching fail for {symbol}:{str(e)}')
            continue
 
    logger.info('Prices has successfully fetched from external API')
    return prices

class APIError(requests.exceptions.RequestException):
    def __init__(self, message, request = None, response = None):
        self.message = message
        self.request = request
        self.response = response
        super().__init__(self.message, request=request, response=response)