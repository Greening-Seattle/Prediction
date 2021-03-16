import pandas as pd


# pseudocode, commented for now to avoid build issue
# ideally, this should be in a different branch other than main
# def predict_change(dframe, input_vars, percents, future_year):

#     # user will input list of string inputs
#     N = np.size(input_vars)
#     model_df = dframe
#     # will be a get_params(zip_df)
#     # from model output of input dataframe
#     params = [2, 3, -0.5, 4]

#     # will refer to 2018 row in each zip dataset
#     current_vals = list(model_df.loc[23, :].values)
#     # initializing vector to store future year values
#     # from percent change in each input,
#     # as defined by user
#     future_vals = []

#     current_output = 0
#     future_output = 0
#     total_change = 0
#     for i in range(0, N):
#         future_vals.append((1+(percents[i]/100))*current_vals[i])
#         current_output += params[i]*current_vals[i]
#         future_output += params[i]*future_vals[i]
#         total_change = ((future_output - current_output)/current_output)*100

#         Print statements listing inputs, change by %, and output number
#         Bar plot showing % increase in total traffic from 2018 to future year


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
