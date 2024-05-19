
# Schwab API Python Library

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A Python library for interacting with the Schwab API. This library provides a simple and convenient way to access Schwab's trading data and market data.

## Installation

You can install the library using pip:

```bash
pip install pyschwab
```

## Preparation

In the root directory, copy https://github.com/hzheng/pyschwab/blob/main/config/pyschwab.yaml to config directory. copy https://github.com/hzheng/pyschwab/blob/main/env_example to .env and replace variables with your settings.

## Usage

Here's a basic example of how to use the library:

```python
from pyschwab.auth import Authorizer
from pyschwab.trading import TradingApi
from pyschwab.market import MarketApi

# Configuration
with open("config/pyschwab.yaml", 'r') as file:
    app_config = yaml.safe_load(file)

authorizer = Authorizer(app_config['auth'])
access_token = authorizer.get_access_token()

# Create trading api client 
trading_api = TradingApi(access_token, app_config['trading'])

account_num = 0 # CHANGE this to your actual account number
trading_data = trading_api.fetch_trading_data(account_num)
# list positions
for position in trading_data.positions:
    print("position:", position)

# list transactions 
for transaction in trading_api.get_transactions(account_num):
    print("transaction:", transaction)

# list orders
for order in trading_api.get_orders(account_num):
    print("order:", order)

# place order
order_dict = {
    "orderType": "LIMIT", "session": "NORMAL", "duration": "DAY", "orderStrategyType": "SINGLE", "price": '100.00',
    "orderLegCollection": [
        {"instruction": "BUY", "quantity": 1, "instrument": {"symbol": "TSLA", "assetType": "EQUITY"}}
    ]
    }
trading_api.place_order(order_dict, account_num)


# Create market api client 
market_api = MarketApi(access_token, app_config['market'])

# get quotes
symbols = ['TSLA', 'NVDA']
quotes = market_api.get_quotes(symbols)
for symbol in symbols:
    print("quote for ", symbol, ":", quotes[symbol] )

option_chain = market_api.get_option_chains('TSLA')
print(option_chain)
 
history = market_api.get_price_history('TSLA')
print(history)
```

## Features

- Retrieve account information
- Place trades
- Check order status
- Access market data
- And more...

---

## License

MIT License

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
