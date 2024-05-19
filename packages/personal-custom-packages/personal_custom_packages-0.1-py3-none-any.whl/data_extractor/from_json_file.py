from data_extractor import log_function_usage
import json

def extract_json_data(location):
    log_function_usage('extract_json_data-data_extractor-from_json_file.py')
    data = None
    with open(location, 'r') as file:
        # Load the JSON data into a Python dictionary
        extract = json.load(file)
        data = extract
    return data

# print(extract_json_data('/Users/marcus/Downloads/extracted_data.json'))