'''
This code runs session to collect raw eeg data using the OpenBCI Cyton Board.

The duration each session takes was convenient to the experiment. The sessions' time could be changed depending on need.

Cyton board description

{'accel_channels': [9, 10, 11],
 'analog_channels': [19, 20, 21],
 'ecg_channels': [1, 2, 3, 4, 5, 6, 7, 8],
 'eeg_channels': [1, 2, 3, 4, 5, 6, 7, 8],
 'eeg_names': 'Fp1,Fp2,C3,C4,P7,P8,O1,O2',
 'emg_channels': [1, 2, 3, 4, 5, 6, 7, 8],
 'eog_channels': [1, 2, 3, 4, 5, 6, 7, 8],
 'marker_channel': 23,
 'name': 'Cyton',
 'num_rows': 24,
 'other_channels': [12, 13, 14, 15, 16, 17, 18],
 'package_num_channel': 0,
 'sampling_rate': 250,
 'timestamp_channel': 22}
'''

import argparse
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
import pandas as pd
import datetime
from datetime import datetime

def save_csv(data, session_counter, exp_name, subject_id):
    df = pd.DataFrame(data).transpose()
    date = datetime.now().date()
    df.to_csv(f'{session_counter}_raw_{subject_id}_{exp_name}_{date}.csv')

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
    #uVolts_per_count = (4500000)/24/(2**23-1) #uV/count
    subject_id = input("Subject's ID number: ")
    session_names = ['right_hand', 'left_hand', 'right_leg', 'left_leg', 'dorsiflextion', 'plantarflextion', 'no_MI', 'no_eye_blink',  'normal_eye_blink', 'double_eye_blink']
    print()
    for i in range(len(session_names)):
        print(f'{i+1}- {session_names[i]}')
    print()
    exp_name = session_names[int(input("Choose your experiment's number: ")) - 1]

    new_session = 'y'
    session_counter = 0 # for the sessions' naming 

    while new_session == 'y':
        session_counter += 1 
        board = BoardShim(args.board_id, params)
        board.prepare_session()
        board.start_stream()
        #print(board.get_eeg_channels(-1))
        time.sleep(2)
        #print(board.get_sampling_rate(0))
        #wait for channels to calibrate after the stream starts
        for i in range(3):
            print(f"{i+1}...")
            time.sleep(1)
        print("Action!") # time of experiment initiation
        time.sleep(4) # time of needed data recording 
        print("Done!")
        #data = board.get_current_board_data (250) # get latest 256 packages or less. It doesn't remove them from the internal buffer
        raw_data = board.get_board_data() # gets all data and remove it from internal buffer, contains eeg data
        board.stop_stream()
        board.release_session()

        save_check = input("Save this session? y/n ")

        if save_check == 'y':
            save_csv(raw_data, session_counter, exp_name, subject_id)
            # Save the data of the current experiment here then procide to the next one...
        elif save_check == 'n':
            session_counter -= 1
        new_session = input("Do you want to repeat the session? y/n ")
                
                
if __name__ == "__main__":
    main()