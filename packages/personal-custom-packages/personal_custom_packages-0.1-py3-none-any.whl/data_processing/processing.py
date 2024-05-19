from data_extractor import log_function_usage
def normalise(max, min, value):
    log_function_usage('normalise-data_processing-processing.py')
    return (value - min)/(max-min)

