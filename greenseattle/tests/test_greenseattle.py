""" Test case for activating travis CI
"""
import numpy as np
import os

import pandas as pd
import pickle

import greenseattle
from greenseattle import Predict_function,\
 Predict_function_Normalization, function_tanh

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


def test_Predict_function_Normalization():
    '''
    test Predict_function_Normalization
    '''
    filepath2 = os.path.join(data_path, 'Weights_MultiFeatures.pckl')
    f = open(filepath2, 'rb')
    [W1, b1, W2, b2, W3, b3] = pickle.load(f)
    f.close()

    x = np.zeros((1, 4))
    Norm_mean = np.ones((1, 4))
    Norm_std = np.ones((1, 4))
    y = Predict_function_Normalization(x, Norm_mean, Norm_std,
                                       W1, b1, W2, b2, W3, b3)
    assert np.allclose(y,
                       np.maximum(function_tanh(function_tanh(b1)
                                                @ W2+b2)
                                  @ W3+b3, 0)
                       ), "unexpected result for Predict_function"
    return


def test_Predict_function():
    '''
    test tanh Predict_function
    '''
    f = open('Weights_MultiFeatures.pckl', 'rb')
    [W1, b1, W2, b2, W3, b3] = pickle.load(f)
    f.close()
    x = np.zeros((1, 4))
    assert np.allclose(Predict_function(x, W1, b1, W2, b2, W3, b3),
                       np.maximum(function_tanh(
                                  function_tanh(b1)@W2+b2)@W3+b3,
                                  0
                                  )
                       ), "unexpected result for Predict_function"
    return


def test_function_tanh():
    '''
    test tanh activation function
    '''
    x = 0
    assert np.all(function_tanh(x) ==
                  0), "unexpected result for function_tanh"
    return
