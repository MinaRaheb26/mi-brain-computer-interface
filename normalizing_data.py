from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
import os
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

def normalizing_data(data):

    X = pd.DataFrame(data)
    # Normalize the data
    scaler = StandardScaler()
    X_standardized = scaler.fit_transform(X)

    # Scale the data between 0 and 1
    minmax_scaler = MinMaxScaler()
    X_normalized = minmax_scaler.fit_transform(X_standardized)      

    return X_normalized

def main():
    path_of_the_directory = '/home/.../filtered_features_no_eye_blink/'

    #for file in os.listdir(path_of_the_directory):
    for file in os.listdir(path_of_the_directory):
        if file.endswith('.csv'):
            # read_csv function which is used to read the required CSV file
            csv_data = pd.read_csv(path_of_the_directory + file)
            
            normalized_data_arr = normalizing_data(csv_data)
            print(f'arr: {normalized_data_arr}')
            normalized_data_df = pd.DataFrame(normalized_data_arr)
            print(f'df: {normalized_data_df}')

            # saving the dataframe
            normalized_data_df.to_csv('/home/.../normalized_' + file, index=False) 

            eeg_channels_new = [0, 1]
            df_normalized = normalized_data_df[[0, 1]]
            plt.figure()
            df_normalized[eeg_channels_new].plot(subplots=True)
            plt.savefig('/home/.../normalized_' + file + '_after_processing.png')
        else:
            continue

if __name__ == "__main__":
    main()