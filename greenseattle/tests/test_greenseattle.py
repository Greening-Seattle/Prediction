""" Test case for activating travis CI
"""
import os

import pandas as pd

import greenseattle

data_path = os.path.join(greenseattle.__path__[0], 'data')


def test_convert_csv():
    """
    Test instance that the output is a pandas dataframe
    """
    filepath = os.path.join(data_path, 'testing.csv')
    dframe = greenseattle.convert_csv(filepath)
    try:
        assert isinstance(dframe, pd.DataFrame)
    except AssertionError:
        print('the input argument should be a pandas DataFrame')
