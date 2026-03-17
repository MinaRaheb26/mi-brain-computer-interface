import os
import re
import pandas as pd

path_of_the_directory = '/home/.../normalized_old/double_eye_blink/'

aggregated = pd.DataFrame()

# Define a sorting key function to extract the file number from the file name
def sort_key(file_name):
    match = re.search(r'\d+', file_name)
    if match:
        return int(match.group())
    else:
        return 0

# Sort the list of file names based on the file number
sorted_files = sorted(os.listdir(path_of_the_directory), key=sort_key)

# Aggregate the files in the sorted order
for file in sorted_files:
    if file.endswith('.csv'):
        # read_csv function which is used to read the required CSV file
        data = pd.read_csv(os.path.join(path_of_the_directory, file))
        aggregated = pd.concat([aggregated, data], axis=0, ignore_index=True)
    else:
        continue

# saving the dataframe
aggregated.to_csv('/home/.../normalized_old/normalized_filtered_aggregated_double_eye_blink.csv', index=False)
