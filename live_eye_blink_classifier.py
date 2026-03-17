"""
Eye blink events classifier of livestreamed data.

We're relying on the data collected through the first channel.
The data is collected, filtered, the needed rows and column are then selected, and at the end the data is classified.

Note: if we're using this data for the sole purpose of analyzing eye blink event through one channel, it makes sense to select the desired
raws and column before filtering (we don't need to filter data we're going to disregard).
"""

import argparse
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
import pandas as pd
import datetime
from datetime import datetime
from scipy.signal import butter, filtfilt, iirnotch
import numpy as np

from brainflow.board_shim import BoardShim, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes

def data_filtering(data, eeg_channels):
    board_id = BoardIds.CYTON_BOARD.value

    for count, channel in enumerate(eeg_channels):
            # filters work in-place
            print(f"count is {count}, channel is {channel}")
            DataFilter.remove_environmental_noise(data[int(channel)+1], BoardShim.get_sampling_rate(board_id),
                                                NoiseTypes.FIFTY.value)
            DataFilter.perform_bandstop(data[int(channel)+1], BoardShim.get_sampling_rate(board_id), 0.5, 100.0, 3, 
                                                FilterTypes.BUTTERWORTH.value, 0)

    return data

def eye_blink_counter(filtered_data_file): # fix input from numpy to dataframe

    column_index = 1
    value_range = slice(1000, 1750)

    selected_column = filtered_data_file[column_index,:]
    selected_values = selected_column[value_range]

    max_val = np.amax(selected_values)
    min_val = np.amin(selected_values)
    max_min_diff = max_val - min_val

    max_200_diff = max_val - 200
    blink_count = 0
    i = 1

    # If True, there's at least one eye blink
    if max_min_diff > 200:
        while(i < len(selected_values)):
            if max_200_diff > selected_values[i]: # max_val - 200 > row_val
                blink_count += 1
                i += 50
            else:
                i += 10
    
    return blink_count


def main():
    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='') # COM7
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board

    # Multiply uVolts_per_count to convert the channels_data to uVolts.
    # uVolts_per_count = (4500000)/24/(2**23-1) #uV/count
 
    start_session = 'y'

    while start_session == 'y':
        
        board = BoardShim(args.board_id, params)
        board.prepare_session()
        board.start_stream()
        time.sleep(2)
        # wait for channels to calibrate after the stream starts
        for i in range(3):
            print(f"{i+1}...")
            time.sleep(1)
        print("Action!") # time of experiment initiation
        time.sleep(4) # time of needed data recording 
        print("Done!")
        raw_data = board.get_board_data() # gets all data and remove it from internal buffer, contains eeg data

        filtered_data = data_filtering(raw_data, eeg_channels=['1'])

        eye_blink_result = eye_blink_counter(filtered_data)

        if eye_blink_result == 0 or eye_blink_result == 1:
            print('Normal state!')
        elif eye_blink_result == 2:
            print('Double blink!')
        elif eye_blink_result == 3:
            print('Tripple blinks!')
        else:
            print('Unidentified...')    
        
        board.stop_stream()
        board.release_session()
                
                
if __name__ == "__main__":
    main()