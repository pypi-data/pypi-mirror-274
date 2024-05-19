from data_extractor import log_function_usage
import pandas as pd
import numpy as np

def get_data(location,sheet_name, nrows):
    log_function_usage('get_data-data_extractor-from_excel.py')
    return pd.read_excel(location,sheet_name=sheet_name,nrows=nrows);

# How do you specific different data types for different columns?    
def convert_data_type(dataTypeDictionary,PandaData):
    log_function_usage('convert_data_type-data_extractor-from_excel.py')
    df_columns = PandaData.columns.tolist()
    # Get the keys from the datatype dictionary
    dtype_keys = list(dataTypeDictionary.keys())
    # Check if all keys in the datatype dictionary are present in the DataFrame
    missing_keys = [key for key in dtype_keys if key not in df_columns]
    if len(missing_keys) > 0:
        print("The following keys from the datatype dictionary are not present in the DataFrame:")
        print(missing_keys)
        return False
    return PandaData.astype(dataTypeDictionary);


