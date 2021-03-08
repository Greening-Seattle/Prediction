""" Test case for activating travis CI
"""
import pandas as pd
import tmp_fortravis
def test_convert_csv():
    """
    Test instance that the output is a pandas dataframe
    """
    filepath = './testing.csv'
    dframe = tmp_fortravis.convert_csv(filepath)
    try:
        assert isinstance(dframe, pd.DataFrame)
    except AssertionError:
        print('the input argument should be a pandas DataFrame')
