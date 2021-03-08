""" An arbitrary function for activating travis
"""
import pandas as pd
def convert_csv(*args):
    """
    Converts a an input csv file to a pandas dataframe
    Input:
        filepath-- string
    Output:
        returns a pandas dataframe
    """
    filepath = args[0]
    try:
        assert isinstance(filepath, str)
    except AssertionError:
        print('the input argument is a string for the filpath ' + \
                 'to the csv file')
    else:
        dframe = pd.read_csv(filepath)
    return dframe
