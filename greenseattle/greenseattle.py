#Standard import libraries
import pandas as pd    
import numpy as np
import matplotlib 
from matplotlib import pyplot as plt
matplotlib.rcParams.update({'font.size': 20})

#Greening Seattle libraries
#to import
from Prediction_function import Predict_function
from Prediction_function import Predict_function_Normalization
from Prediction_function import function_tanh

def prepare_nn():
    
    dataset0 = pd.read_csv('all_data.csv',encoding='latin-1')
    
    # Normlized
    features_select = ['Total_Population', 'Pop_fraction', 'RACK_CAPACITY', 'Miles_Bike_Lanes'] # name of features
    label_select = ['AAWDT'] # name of label

    #### Note the the prediction should use the same Normlization
    dataset = dataset0/dataset0.mean() # Normlized the data
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_features = train_dataset[features_select]
    test_features = test_dataset[features_select]

    train_labels = train_dataset[label_select]
    test_labels = test_dataset[label_select]
    
    f = open('Weights_MultiFeatures.pckl', 'rb')
    [W1, b1, W2, b2,W3, b3] = pickle.load(f)
    f.close()
    
    return W1, b1, W2, b2,W3, b3


def feature_projection(feature,zipcode):

    features_select = ['Total_Population', 'Pop_fraction', 'RACK_CAPACITY', 'Miles_Bike_Lanes'] # name of features
    label_select = ['AAWDT'] # name of label
    
    dataset0 = pd.read_csv('all_data.csv',encoding='latin-1')
    zip_data = dataset0.loc[dataset0['ZIPCODE']==zipcode]

    W1, b1, W2, b2, W3, b3 = prepare_nn()
    
    feature0 = zip_data.max()[features_select]
    
    list_proportion = np.arange(0,10,0.5)
    feature_idx = feature
    list_prediction = []
    Norm_mean = dataset0.mean()[features_select]
    Norm_std = dataset0.std()[features_select]
    label_mean = dataset0.mean()[label_select]
    label_std = dataset0.std()[label_select]

    for proportion in list_proportion:
        feature_test = feature0.copy()
        feature_test[feature_idx] = feature0[feature_idx]*proportion
        Label_test = Predict_function_Normalization(feature_test,Norm_mean,Norm_std,W1, b1, W2, b2,W3, b3)
        list_prediction.append(Label_test*label_mean)
    
    output_list = []
    for i in range(0,np.size(list_proportion)):
        output_list.append(list_prediction[i][0])
            
    return output_list


def model_viz(zipcode):
    
    dataset0 = pd.read_csv('all_data.csv',encoding='latin-1')
    list_proportion = np.arange(0,10,0.5)
    
    pop_val = feature_projection(0,zipcode)
    rack_val = feature_projection(2,zipcode)
    lanes_val = feature_projection(3,zipcode)
    
    zipcode_identifier = zipcode*np.ones(np.size(pop_val))

    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(list_proportion,np.log(pop_val),'o-',color='blue',label='Population')
    ax.plot(list_proportion,np.log(rack_val),'x-',color='red',label='Bike Rack Capacity')
    ax.plot(list_proportion,np.log(lanes_val),'s-',color='green', label='Bike Lanes (ft)')

    plt.xlabel('Proportional changes')
    plt.ylabel('Log10 Traffic')
    plt.suptitle('Projected Traffic Change in Zipcode', fontsize=18)
    plt.xlim([-0.1,10.5])
    plt.tight_layout
    plt.legend(loc='lower right', title_fontsize='xx-small')
    
    matrix = np.stack((np.log(pop_val),np.log(rack_val),np.log(lanes_val),zipcode_identifier)).T
    
    return matrix


def convert_csv(*args):
    """
    An arbitrary function for activating travis
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
