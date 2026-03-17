"""
Selecting the desired features of the eye blink events (based on a previuos knowledge of the data collection process).

The range is based on a previous knowledge of when eyeblink event has happend during the data collection phase and the frequency rate of the collecting device.
"""

import os
import pandas as pd

path_of_the_directory = '/home/.../No_eye_blink/'

for file in os.listdir(path_of_the_directory):
    if file.endswith('.csv'):
        # read_csv function which is used to read the required CSV file
        data = pd.read_csv(path_of_the_directory + file)
        
        # display 
        #print("Original 'input.csv' CSV Data: \n")
        #print(data)
        
        # removing rows and columns from the CSV files
        data = data[['1', '2']].iloc[1000:2000,:]

        # display 
        #print("\nCSV Data after deleting the column 'year':\n")
        #print(data)

        # sacing the dataframe
        data.to_csv('/home/.../ml_ready_' + file, index=False) 
    else:
        continue