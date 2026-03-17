"""
Using the brainflow library to filter the collected data, in order to create files ready for analysis.
"""

import os
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes

def filtering_eeg_channels(data,eeg_channels, board_id):
    for count, channel in enumerate(eeg_channels):
            # filters work in-place
            print(f"count is {count}, channel is {channel}")
            DataFilter.remove_environmental_noise(data[int(channel)+1], BoardShim.get_sampling_rate(board_id),
                                                NoiseTypes.FIFTY.value)
            DataFilter.perform_bandstop(data[int(channel)+1], BoardShim.get_sampling_rate(board_id), 8.0, 45.0, 3, 
                                                FilterTypes.BUTTERWORTH.value, 0)
    return data

def main():
    BoardShim.enable_dev_board_logger()
    board_id = BoardIds.CYTON_BOARD.value

    path_of_the_directory = '/home/.../normal_eye_blink/'

    for file in os.listdir(path_of_the_directory):
        if file.endswith('.csv'):
            # read_csv function which is used to read the required CSV file
            csv_data = pd.read_csv(path_of_the_directory + file)

            eeg_channels = ['1', '2']

            csv_data = pd.DataFrame(csv_data).to_numpy().transpose()

            filtered_data = filtering_eeg_channels(csv_data, eeg_channels, board_id)

            df_filtered = pd.DataFrame(np.transpose(filtered_data))
            # removing rows and columns from the CSV files
            filtered_features = df_filtered[[2, 3]].iloc[1000:2000,:]
            # saving the dataframe
            filtered_features.to_csv('/home/.../filtered_normal_eye_blink/ml_ready_' + file, index=False) 

            eeg_channels_new = [2,  3]
            df_filtered = df_filtered[[2, 3]]
            plt.figure()
            filtered_features[eeg_channels_new].plot(subplots=True)
            plt.savefig('/home/.../filtered_normal_eye_blink/ml_ready_' + file + '_after_processing.png')
        else:
            continue

if __name__ == "__main__":
    main()