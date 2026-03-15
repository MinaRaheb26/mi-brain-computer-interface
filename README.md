# mi-brain-computer-interface

The approach that was taken to build this project was the approach of an experiment made for a research. So there're multiple separated python "small" programs that perform a specific thing.

Multiple of those programs could be combined together. For example, there's a progrma that collects the data, a second one that filtes the data, a third one that saves the desired dataframes. They could be combined to work together and save different versions of the data files (raw data, filtered data, segmented data) as it goes.

Motor Imagery Brain-Computer Interfaces (MI-BCIs) are interaction systems that enable users to send commands to a computer by the sole use of brain activity produced from imagined movement. 

To build this project, 8 electrode channels are used, one for eye blinks and 7 for motor imagery, MI, data collection.

The BCI system operates on two modes, when a double blink event is detected, it switches to the second mode where the detection of the same MI class sends a different command to the computer, thus, doubling the capability of the system.

Electroencephalogram, EEG, data acquisition sessions were conducted to build datasets for analysis corresponding to the normal eye state (eyes open or one eye blink), a double eye blink event and a triple eye blink event. 

The mathematical method used for their classification has proven to be highly reliable; however, it wasn't taken into consideration when someone closes their eyes for a long time.

For the MI, Dataset “A” from the BCI Competition 2008 is used to train EEGNet NN architecture with an average accuracy of ~77% for the classification of 4 MI classes using only the data of 7 of the original 22 electrodes used to acquire the data.

The data of 3 subjects were ignored (unreliable data).

The average accuracy of classification for the same subjects using the 22 electrodes was ~83%, which means the data of the 7 electrodes chosen to build the system well represent the MI signals components.

A simple GUI to let the user know in which operating mode they're at. Thus, a complete MI-BCI system.
