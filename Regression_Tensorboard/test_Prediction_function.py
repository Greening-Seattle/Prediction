

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:57:22 2021

@author: Wenqi Cui
"""

import numpy as np
import pickle


def Predict_function(Predict_input, W1, b1, W2, b2, W3, b3):
    '''
    The prediction function represented by neural network with tanh activation
    Predict_input is the data after normlization
    '''
    Predict_output = function_tanh(function_tanh(Predict_input@W1+b1)
                                   @ W2 + b2) @ W3 + b3
    return Predict_output


def Predict_function_Normalization(Predict_input, Norm_mean, Norm_std,
                                   W1, b1, W2, b2, W3, b3):
    '''
    The prediction function represented by neural network with tanh activation
    Predict_input is the raw data withour normlization
    Predict_df is the dataframe for prediction
    '''
    Predict_input = (Predict_input-Norm_mean)/Norm_std
    Predict_output = function_tanh(function_tanh(Predict_input@W1+b1)
                                   @ W2+b2)@W3+b3
    return Predict_output


def function_tanh(x):
    '''
    tanh activation function
    '''
    y = (2 / (1 + np.exp(-2 * x))) - 1
    return y


def test_Predict_function_Normalization():
    '''
    test Predict_function_Normalization
    '''
    f = open('Weights_MultiFeatures.pckl', 'rb')
    [W1, b1, W2, b2, W3, b3] = pickle.load(f)
    f.close()

    x = np.ones((1, 3))
    Norm_mean = np.ones((1, 3))
    Norm_std = np.ones((1, 3))
    y = Predict_function_Normalization(x, Norm_mean, Norm_std,
                                       W1, b1, W2, b2, W3, b3)
    assert np.allclose(y, function_tanh(function_tanh(b1) @ W2+b2) @ W3+b3), "unexpected result for Predict_function"
    return



def test_Predict_function():
    '''
    test tanh Predict_function
    '''
    f = open('Weights_MultiFeatures.pckl', 'rb')
    [W1, b1, W2, b2, W3, b3] = pickle.load(f)
    f.close()
    x = np.zeros((1,3))
    assert np.allclose(Predict_function(x, W1, b1, W2, b2, W3, b3),
                  function_tanh(function_tanh(b1)@W2+b2)@W3+b3), "unexpected result for Predict_function"
    return


def test_function_tanh():
    '''
    test tanh activation function
    '''
    x = 0
    assert np.all(function_tanh(x) ==
                  0), "unexpected result for function_tanh"
    return
