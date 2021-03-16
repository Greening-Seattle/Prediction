# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:57:22 2021

@author: Wenqi Cui
"""

import numpy as np


def Predict_function(Predict_input, W1, b1, W2, b2, W3, b3):
    '''
    The prediction function represented by neural network with tanh activation
    Predict_input is the data after normlization
    '''
    Predict_output = function_tanh(function_tanh(Predict_input@W1+b1)
                                   @ W2 + b2) @ W3 + b3
    return np.maximum(Predict_output, 0)


def Predict_function_Normalization(Predict_input, Norm_mean, Norm_std,
                                   W1, b1, W2, b2, W3, b3):
    '''
    The prediction function represented by neural network with tanh activation
    Predict_input is the raw data withour normlization
    Predict_df is the dataframe for prediction
    '''
    Predict_input = (Predict_input) / Norm_mean
    Predict_output = function_tanh(function_tanh(Predict_input@W1+b1)
                                   @ W2+b2)@W3+b3
    return np.maximum(Predict_output, 0)


def function_tanh(x):
    '''
    tanh activation function
    '''
    y = (2 / (1 + np.exp(-2 * x))) - 1
    return y
