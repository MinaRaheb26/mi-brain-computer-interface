"""
A certain threshold was selected based on a visual analysis of the data, which enabled us to classify the eye blink events mathematically
in a non-complix way.
"""

import pandas as pd
import numpy as np

data_file = np.genfromtxt('/home/.../normal_eye_blink_2023-03-30.csv', delimiter=',', usecols=1)
#data_file = np.genfromtxt('/home/.../double_eye_blink_2023-03-03.csv', delimiter=',', usecols=1)

max_val = np.amax(data_file)
min_val = np.amin(data_file)

max_min_diff = max_val - min_val

max_200_diff = max_val - 200
blink_count = 0
i = 1

# If True, there's at least one eye blink
if max_min_diff > 200:
    while(i < len(data_file)):
        if max_200_diff > data_file[i]: # max_val - 200 > row_val
            blink_count += 1
            i += 50
        else:
            i += 10

if blink_count == 0 or blink_count == 1:
    print('Normal state!')
elif blink_count == 2:
    print('Double blink!')
elif blink_count == 3:
    print('Tripple blinks!')
else:
    print('Unidentified...')
