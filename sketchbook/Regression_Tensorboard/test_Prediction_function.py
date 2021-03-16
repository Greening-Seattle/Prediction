

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:57:22 2021

@author: Wenqi Cui
"""

import numpy as np
import pickle

import Prediction_function
from Prediction_function import Predict_function, Predict_function_Normalization, function_tanh


def test_Predict_function_Normalization():
    '''
    test Predict_function_Normalization
    '''
    f = open('Weights_MultiFeatures.pckl', 'rb')
    [W1, b1, W2, b2, W3, b3] = pickle.load(f)
    f.close()

    x = np.zeros((1, 4))
    Norm_mean = np.ones((1, 4))
    Norm_std = np.ones((1, 4))
    y = Predict_function_Normalization(x, Norm_mean, Norm_std,
                                       W1, b1, W2, b2, W3, b3)
    assert np.allclose(y, np.maximum(function_tanh(function_tanh(b1) @ W2+b2) @ W3+b3,0)), "unexpected result for Predict_function"
    return


def test_Predict_function():
    '''
    test tanh Predict_function
    '''
    f = open('Weights_MultiFeatures.pckl', 'rb')
    [W1, b1, W2, b2, W3, b3] = pickle.load(f)
    f.close()
    x = np.zeros((1,4))
    assert np.allclose(Predict_function(x, W1, b1, W2, b2, W3, b3),
                  np.maximum(function_tanh(function_tanh(b1)@W2+b2)@W3+b3,0)), "unexpected result for Predict_function"
    return

def test_function_tanh():
    '''
    test tanh activation function
    '''
    x = 0
    assert np.all(function_tanh(x) ==
                  0), "unexpected result for function_tanh"
    return
