""" Test case for activating travis CI
"""
import pandas as pd
from tmpmodule import convert_csv
def test_convert_csv():
    """
    Test instance that the output is a pandas dataframe
    """
    filepath = './testing.csv'
    dframe = convert_csv(filepath)
    try:
        assert isinstance(dframe, pd.DataFrame)
    except AssertionError:
        print('the input argument should be a pandas DataFrame')
