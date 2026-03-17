"""
A simple GUI to prompt the user of the operating mode they're in.

This is just meant to be as a test to show how the final, realtime, GUI will look like.
"""

import tkinter as tk
import pandas as pd
import numpy as np
import time 

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x100")
        self.master.resizable(False, False)
        self.master.title("Op. Mode")

        # Setting the font
        self.label_font = ("Verdana", 20)

        # Creating the label
        self.label = tk.Label(self.master, text="Normal state!", font=self.label_font)
        self.label.pack(expand=True)

        # Getting the screen's dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculating the coordinates for bottom right corner
        x = screen_width - self.master.winfo_reqwidth()
        y = screen_height - self.master.winfo_reqheight()

        # Positioning the window in the bottom right corner
        self.master.geometry("+{}+{}".format(x, y))

        # Scheduling an update every 1000 milliseconds (1 second)
        self.master.after(100, self.update_label)

    def update_label(self):
        # Normal eye blink data (normal state)
        data_file = np.genfromtxt('/home/.../data_aquisition/filtered_features_Double_eye_blink/ml_ready_5_raw_no_eye_blink_2023-03-03.csv', delimiter=',', usecols=1)
        # One eye blink (normal state)
        #data_file = np.genfromtxt('/home/.../data_aquisition/filtered_features_Double_eye_blink/ml_ready_4_raw_normal_eye_blink_2023-03-03.csv', delimiter=',', usecols=1)
        # Double eye blink data
        #data_file = np.genfromtxt('/home/.../data_aquisition/filtered_features_Double_eye_blink/ml_ready_1_raw_double_eye_blink_2023-03-03.csv', delimiter=',', usecols=1)
        # Tripple eye blink data
        #data_file = np.genfromtxt('/home/.../data_aquisition/filtered_features_Double_eye_blink/ml_ready_9_raw_double_eye_blink_2023-03-03.csv', delimiter=',', usecols=1)

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

        if blink_count <= 1 or blink_count > 2:
            self.label.config(text="Normal state!")
        elif blink_count == 2:
            self.label.config(text="Operation Mode 2")
        elif blink_count == 3:
            self.label.config(text="Triple blinks!")
        else:
            self.label.config(text="Unidentified...")

        # Schedule next update every 100 milliseconds (1 second)
        self.master.after(100, self.update_label)

def classify_blink():
    start_time = time.time()
    root = tk.Tk()
    gui = GUI(root)
    print(time.time() - start_time)
    root.mainloop()


classify_blink()


