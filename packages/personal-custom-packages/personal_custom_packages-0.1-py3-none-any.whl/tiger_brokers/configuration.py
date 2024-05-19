from data_extractor import log_function_usage
import configparser
from tigeropen.common.consts import (Language,        # Language
                                Market,           # Market
                                BarPeriod,        # Size of each time window of the K-Line
                                QuoteRight)       # Price adjustment type
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.quote.quote_client import QuoteClient
import re

config = configparser.ConfigParser()
config.read('/Users/marcus/Desktop/AI/custom_packages/tiger_brokers/tiger_openapi_config.properties')



def create_configuration_object():
    log_function_usage('create_configuration_object-tiger_brokers-configuration.py')
    print(config["configuration"]["tiger_id"])
    client_config = TigerOpenClientConfig(sandbox_debug=False)
    client_config.private_key = config["configuration"]["private_key_pk1"]
    client_config.tiger_id = config["configuration"]["tiger_id"]
    client_config.account = config["configuration"]["account"]
    # client_config.timezone = 'US/Eastern' # default timezone 
    return client_config



