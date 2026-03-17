"""
An alternative way of filtering the collected data. 

Using the filters in the brainflow library makes more sense for multiple reasons:
    1. Processing power and efficiency (lower latency).
    2. The implementation of the filters are slightly different, which can result in slightly different outputs.
    3. Convenience and code cleanliness.

Using the Butterworth's filter:

The EEG data is stored in a CSV file with each row representing a sample and each column representing a channel. 
The first two lines of the code import the necessary modules, and the third line loads the EEG data from the CSV file using the read_csv function from the pandas module.

Defining the filter's parameters, which includes: the filter's order, sampling frequency, and low and high cutoff frequencies. 
The butter function is then used to calculate the filter coefficients b and a for a fourth-order Butterworth filter with a bandpass filter type.

Finally, the filtfilt function from the scipy.signal module is used to apply the filter to the EEG data. 

This function applies a zero-phase filter to the data, which means that the filtered data has no phase shift compared to the original data. 
The filtered data is then saved to a new CSV file using the to_csv function from the pandas module.

- What does the "filter order" mean?

In digital signal processing, the filter order refers to the number of previous input and output values that a filter uses to compute the current output. 
The filter order determines the steepness of the filter's roll-off curve, which is the rate at which the filter attenuates frequencies outside its passband.

A higher filter order typically results in a steeper roll-off and more selective filtering, but also increases the computational complexity of the filter. 
The filter order is usually chosen based on the desired filtering characteristics and the available computational resources.

In the following code, the filter order is set to 4. 
This means that the Butterworth filter uses the four most recent input and output values to calculate the current output. 
"""

from scipy.signal import butter, filtfilt, iirnotch
import pandas as pd

# Load EEG data from CSV file
eeg_data = pd.read_csv('/home/.../normal_state.csv', header=None)

# Define filter parameters
order = 4  # Filter order
fs = 250  # Sampling frequency
lowcut = 8  # Low cutoff frequency in Hz
highcut = 45  # High cutoff frequency in Hz
notch_freq = 50 # Notch frequency in Hz
Q = 30  # Quality factor

# Calculate filter coefficients
nyq = 0.5 * fs
low = lowcut / nyq
high = highcut / nyq
b, a = butter(order, [low, high], btype='band')

# Apply notch filter to EEG data
w0 = notch_freq / nyq
b_notch, a_notch = iirnotch(w0, Q)
eeg_data = eeg_data.to_numpy().squeeze() # remove empty dimensions
eeg_data = filtfilt(b_notch, a_notch, eeg_data, padlen=min(len(eeg_data), 3*(max(len(a_notch), len(b_notch)) - 1))-6)

# Apply filter to EEG data
filtered_data = pd.DataFrame(filtfilt(b, a, eeg_data, axis=0))

# Save filtered data to CSV file
filtered_data.to_csv('/home/.../filtered_normal_state.csv', index=0, header=True)