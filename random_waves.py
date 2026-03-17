'''
Generate random waves with different frequencies to get a general idea of the waves and test filters on.
'''

import numpy as np
import matplotlib.pyplot as plt

# Generate 5 random sine waves between 0.5 and 4 Hz, 4 and 8 Hz, 8 and 12 Hz, 12 and 30 Hz, and 30 and 100 Hz

# Set the sample rate and the length of the signals
sample_rate = 100
num_samples = 100

# Set the frequency range and labels for each signal
frequencies = [[0.5, 4], [4, 8], [8, 12], [12, 30], [30, 100]]
labels = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']

# Initialize a list to store the signals
signals = []

# Generate the signals
for f, label in zip(frequencies, labels):
    # Generate a random frequency within the specified range
    freq = np.random.uniform(f[0], f[1])
    # Generate the time values for the signal
    t = np.linspace(0, num_samples/sample_rate, num_samples)
    # Generate the signal
    signal = np.sin(2*np.pi*freq*t)
    # Add the signal to the list
    signals.append(signal)

# Plot the signals in separate subplots
fig, ax = plt.subplots(nrows=len(signals), ncols=1, figsize=(8,8), sharex=True)
colors = ['b', 'g', 'r', 'c', 'm']
for i, (signal, label, color) in enumerate(zip(signals, labels, colors)):
    ax[i].plot(signal, label=label, color=color)
    ax[i].legend()
    ax[i].set_title(label)
plt.show()
