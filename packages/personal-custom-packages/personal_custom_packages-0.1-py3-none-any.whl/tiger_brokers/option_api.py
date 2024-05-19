# from .data_extractor import log_function_usage
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.common.consts import BarPeriod
import re


def get_time_period(time_specified):
    # log_function_usage('get_time_period-tiger_brokers-option_api.py')
    if time_specified == "1min":
        return BarPeriod.ONE_MINUTE
    elif time_specified == "5min":
        return BarPeriod.FIVE_MINUTES
    elif time_specified == "30min":
        return BarPeriod.HALF_HOUR
    elif time_specified == "60min":
        return BarPeriod.ONE_HOUR
    elif time_specified == "144min":
        return BarPeriod.DAY
    else:
        return False  # Handle invalid input

def get_expiry_list(config,symbols):
    # log_function_usage('get_expiry_list-tiger_brokers-option_api.py')
    quote_config = QuoteClient(config)
    data = quote_config.get_option_expirations(symbols)
    return data

def get_option_chain(config,symbol, expiry):
    # log_function_usage('get_option_chain-tiger_brokers-option_api.py')
    quote_config = QuoteClient(config)
    data = quote_config.get_option_chain(symbol, expiry)
    return data

def get_option_bar(config,identifier, beginTime=None,endTime=None,period=None):
    # log_function_usage('get_option_bar-tiger_brokers-option_api.py')
    quote_config = QuoteClient(config)
    # print(BarPeriod.ONE_MINUTE.value)
    data = None
    if beginTime == None and endTime == None and period == None:
        data = quote_config.get_option_bars(identifier)
    else:
        time = get_time_period(period)
        if time == False:
            return False
        data = quote_config.get_option_bars(identifier,beginTime,endTime,time)
    return data


