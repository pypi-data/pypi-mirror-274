from data_extractor import log_function_usage
'''
    NOTE: 
        STEPS:
            1. Read the configuration data from the (tiger_openapi_config.properties) file
            2. Store configuration data in the configuration object (TigerOpenClienConfig)
            3. initialise the quoteClient (The encapsulator for market data API)
            4. Run the respective method from the quoteClient to access certain market data.

'''

import configparser
from tigeropen.common.consts import (Language,        # Language
                                Market,           # Market
                                BarPeriod,        # Size of each time window of the K-Line
                                QuoteRight)       # Price adjustment type
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient
import re
from tigeropen.common.consts import BarPeriod

def get_time_period(time_specified):
    log_function_usage('get_time_period-tiger_brokers-stock_api.py')
    if time_specified == "1min":
        return BarPeriod.ONE_MINUTE
    elif time_specified == "5min":
        return BarPeriod.FIVE_MINUTES
    elif time_specified == "30min":
        return BarPeriod.HALF_HOUR
    elif time_specified == "60min":
        return BarPeriod.ONE_HOUR
    else:
        return False  # Handle invalid input
    
def get_latest_top_of_book_data(config):
    log_function_usage('get_latest_top_of_book_data-tiger_brokers-stock_api.py')
    quote_client = QuoteClient(config)
    # query Stock quotes
    result = quote_client.get_market_status(market=Market.ALL, lang=None)
    # stock_price = quote_client.get_stock_briefs(['00700'])
    return result

def bid_ask_for_price_quantity_and_orderCount(config,symbol,market):
    log_function_usage('bid_ask_for_price_quantity_and_orderCount-tiger_brokers-stock_api.py')
    if type(symbol) != "list":
        return False
    data = config.get_depth_quote(symbol, market)
    organised = {}
    if len(symbol) > 1:
        for key,value in data.items():
            for content in value["asks"]:
                organised[key]["ask"]["price"].append(value[0])
                organised[key]["ask"]["quantity"].append(value[1])
                organised[key]["ask"]["order count"].append(value[2])
            for value in value["bids"]:
                organised[key]["bid"]["price"].append(value[0])
                organised[key]["bid"]["quantity"].append(value[1])
                organised[key]["bid"]["order count"].append(value[2])
    if len(symbol) == 1:
        organised[symbol]["ask"] = {
            "price": [],
            "quantity": [],
            "order count": []
        }
        organised[symbol]["bid"] = {
            "price": [],
            "quantity": [],
            "order count": []
        }
        for value in data["asks"]:
            organised[symbol]["ask"]["price"].append(value[0])
            organised[symbol]["ask"]["quantity"].append(value[1])
            organised[symbol]["ask"]["order count"].append(value[2])
        for value in data["bids"]:
            organised[symbol]["bid"]["price"].append(value[0])
            organised[symbol]["bid"]["quantity"].append(value[1])
            organised[symbol]["bid"]["order count"].append(value[2])
    return organised

def get_candle_stick_data(config,interval,symbols,beginTime,endTime,limit=251):
    # print("CHECK!!!!!!!!!")
    log_function_usage('get_candle_stick_data-tiger_brokers-stock_api.py')
    unix_time_pattern = r'^\d{13}$'  # Unix timestamp pattern (13 digits)
    date_string_pattern = r'^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}|\d{4}-\d{2}-\d{2})$'  # Date string pattern (YYYY-MM-DD HH:MM:SS or YYYY-MM-DD)
    if limit > 251 or limit < 0:
        return False
    # Check if the input matches either Unix timestamp or date string format
    if re.match(unix_time_pattern, str(beginTime)) or re.match(date_string_pattern, str(beginTime)):
        if re.match(unix_time_pattern, str(endTime)) or re.match(date_string_pattern, str(endTime)):
            # print("\nCHECK 2 !!!!!!!!!!\n")
            quote_config = QuoteClient(config)
            time = get_time_period(interval)
            if time == False:
                return False
            data = quote_config.get_bars(symbols, period=time, begin_time=beginTime, end_time=endTime, right=QuoteRight.BR, limit=limit, lang=None)
            # print('\n')
            # bars = quote_config.get_bars(['NVDA'],get_time_period('1min'),begin_time='2024-04-22 00:00:00',end_time='2024-04-23 00:00:00',limit=251)
            # print(bars)
            # print('\n')
            return data

    else:
        return False
    # if right not in [QuoteRight.BR_forward_adjust, QuoteRight.NR_no_adjustment]:
    #     return False
    
def get_candle_stick_data_by_page(config,interval, symbol,begin_time,end_time):
    quote_config = QuoteClient(config)
    data = quote_config.get_bars_by_page(symbol,period=get_time_period(interval),begin_time=begin_time,end_time=end_time)
    return data

def latest_minute_timeline_data(symbols, beginTime):
    log_function_usage('latest_minute_timeline_data-tiger_brokers-stock_api.py')
    unix_time_pattern = r'^\d{13}$'  # Unix timestamp pattern (13 digits)
    date_string_pattern = r'^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}|\d{4}-\d{2}-\d{2})$'  # Date string pattern (YYYY-MM-DD HH:MM:SS or YYYY-MM-DD)
    if re.match(unix_time_pattern, beginTime) or re.match(date_string_pattern, beginTime):
        data = QuoteClient.get_timeline(symbols, include_hour_trading=True, begin_time=beginTime, lang=None)
        return data
    else:
        return False
    
def historical_minute_timeline_data(symbol, date):
    log_function_usage('historical_minute_timeline_data-tiger_brokers-stock_api.py')
    date_string_pattern = '^\d{4}-\d{2}-\d{2})'
    if re.match(date_string_pattern,date):
        return QuoteClient.get_timeline_history(symbol, date)
    else:
        return False
    
def price_direction(symbol, trade_session, ):
    log_function_usage('price_direction-tiger_brokers-stock_api.py')
    QuoteClient.get_trade_ticks(symbols, trade_session=None, begin_index=0, end_index=30, limit=30, lang=None)

def delayed_real_time_data(config):
    log_function_usage('delayed_real_time_data-tiger_brokers-stock_api.py')
    quote_client = QuoteClient(config)
    data = quote_client.get_stock_delay_briefs(["NVDA"], lang=None)
    return data

def historical_price_volume_data(config,symbols,date):
    log_function_usage('historical_price_volume_data-tiger_brokers-stock_api.py')
    quote_client = QuoteClient(config)
    return quote_client.get_timeline_history(symbols, date)

def real_time_data(config,symbols):
    log_function_usage('real_time_data-tiger_brokers-stock_api.py')
    quote_client = QuoteClient(config)
    data = quote_client.get_stock_briefs(symbols, lang=None)
    return data



# quote_client = QuoteClient(config)
# data = quote_client.get_trade_ticks(["NVDA"], begin_index=0, end_index=5, limit=30)
# print(data)