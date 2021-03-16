#Standard import libraries
import adjustText as aT
import pandas as pd    
import geopandas as gpd
import numpy as np
import matplotlib 
from matplotlib import pyplot as plt
matplotlib.rcParams.update({'font.size': 20})

#Greening Seattle libraries
#to import

percents = [5,5,10,10]

def predict_change(df,input_vars,percents,future_year):
    
    N = np.size(inputs) #user will input list of string inputs
    model_df = dataset
    params = [2, 3, -0.5, 4] #will be a get_params(zip_df) from model output of input dataframe
    
    current_vals = list(model_df.loc[23,:].values) #will refer to 2018 row in each zip dataset
    future_vals = [] #initializing vector to store future year values from percent change in each input,
    #as defined by user
    
    current_output = 0
    future_output = 0
    total_change = 0
    for i in range(0,N):
        future_vals.append((1+(percents[i]/100))*current_vals[i])
        current_output += params[i]*current_vals[i]
        future_output += params[i]*future_vals[i]
        total_change = ((future_output - current_output)/current_output)*100  
        
    #Print statements listing inputs, change by %, and output number
    #Bar plot showing % increase in total traffic from 2018 to future year


""" An arbitrary function for activating travis
"""


def convert_csv(*args):
    """
    Converts a an input csv file to a pandas dataframe
    Input-- filepath, string type
    Output-- returns a pandas dataframe

    """
    filepath = args[0]
    try:
        assert isinstance(filepath, str)
    except AssertionError:
        print('the input argument is a string for the filpath ' +
              'to the csv file')
    else:
        dframe = pd.read_csv(filepath)
        return dframe
