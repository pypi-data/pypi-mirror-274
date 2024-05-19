import logging
from database.function_usage import *
import datetime

logging.basicConfig(level=logging.DEBUG)

def reformat_and_record(message):
    seeMessage = message.getMessage()
    breakApart = seeMessage.split("-")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_data("usage_data",["function_name","timestamp","utility","specific_utility"],[f"'{breakApart[0]}'",f"'{time}'",f"'{breakApart[1]}'",f"'{breakApart[2]}'"])

logger = logging.getLogger("usage")
handler = logging.StreamHandler()
handler.emit = reformat_and_record
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_function_usage(message):
    logger.info(message)


# JUST WRITE logger.info("[function name]") in the function.
# from data_extractor.from_logging import log_function_usage