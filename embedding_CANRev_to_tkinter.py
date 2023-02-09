import tkinter
import numpy as np
import os
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def getHS(dataFrame):
  return list(dataFrame.Description.unique())

def extract(dataFrame, HSCAN):
    dataFrame.index[dataFrame["Description"]== HSCAN]
    locHSCAN = dataFrame.index[dataFrame["Description"]== HSCAN]
    locHSCAN = list(locHSCAN)
    index = []
    for i in locHSCAN:
        indexHSCAN = dataFrame.loc[[i]]
        index.append(indexHSCAN)
    result = pd.concat(index)
    return result

def plot_CAN_log(time, B1, B2, B3, B4, B5, B6, B7, B8):
    #plot 1:
    y = B1
    x = time
    plt.subplot(8, 1, 1)
    plt.plot(x,y)

    #plot 2:
    y = B2
    x = time
    plt.subplot(8, 1, 2)
    plt.plot(x,y)

    #plot 3:
    y = B3
    x = time
    plt.subplot(8, 1, 3)
    plt.plot(x,y)

    #plot 4:
    y = B4
    x = time
    plt.subplot(8, 1, 4)
    plt.plot(x,y)

    #plot 5:
    y = B5
    x = time
    plt.subplot(8, 1, 5)
    plt.plot(x,y)

    #plot 6:
    y = B6
    x = time
    plt.subplot(8, 1, 6)
    plt.plot(x,y)

    #plot 7:
    y = B7
    x = time
    plt.subplot(8, 1, 7)
    plt.plot(x,y)

    #plot 8:
    y = B8
    x = time
    plt.subplot(8, 1, 8)
    plt.plot(x,y)

    plt.subplots_adjust(top=0.979,
                    bottom=0.054,
                    left=0.043,
                    right=0.988,
                    hspace=0.802,
                    wspace=0.2)

    plt.show()

def save_csv(dataFrame, file_name):
    if os.path.isdir("/csv_files/") is False:
        os.makedirs("/csv_files/")
        dataFrame.to_csv("/csv_files/{}".format(file_name), index=False)
    else:
        dataFrame.to_csv("/csv_files/{}".format(file_name), index=False)

def hex_to_decimal(hex):
    list_hex = list(hex)
    value = []
    result = []
    for i in list_hex:
        if i.isnumeric():
            new_i = int(i)
            value.append(new_i)
        elif i == 'a' or i == 'A':
            value.append(10)
        elif i == 'b' or i == 'B':
            value.append(11)
        elif i == 'c' or i == 'C':
            value.append(12)
        elif i == 'd' or i == 'D':
            value.append(13)
        elif i == 'e' or i == 'E':
            value.append(14)
        elif i == 'f' or i == 'F':
            value.append(15)
    value.reverse()
    value_length = len(value)
    for n, i in enumerate(value):
        formula = (i * 16**n)
        result.append(formula)
    return(sum(result))

def get_data(dataFrame, HSCAN):
    analyzeHScan = extract(dataFrame, HSCAN)
    timestamp = analyzeHScan['Abs Time(Sec)']

    times = []
    decimals1 = []
    decimals2 = []
    decimals3 = []
    decimals4 = []
    decimals5 = []
    decimals6 = []
    decimals7 = []
    decimals8 = []

    for i in timestamp:
        times.append(i)

    for i in analyzeHScan["B1"]:
        decimal = hex_to_decimal(i)
        decimals1.append(decimal)
    for i in analyzeHScan["B2"]:
        decimal = hex_to_decimal(i)
        decimals2.append(decimal)
    for i in analyzeHScan["B3"]:
        decimal = hex_to_decimal(i)
        decimals3.append(decimal)
    for i in analyzeHScan["B4"]:
        decimal = hex_to_decimal(i)
        decimals4.append(decimal)
    for i in analyzeHScan["B5"]:
        decimal = hex_to_decimal(i)
        decimals5.append(decimal)
    for i in analyzeHScan["B6"]:
        decimal = hex_to_decimal(i)
        decimals6.append(decimal)
    for i in analyzeHScan["B7"]:
        decimal = hex_to_decimal(i)
        decimals7.append(decimal)
    for i in analyzeHScan["B8"]:
        decimal = hex_to_decimal(i)
        decimals8.append(decimal)
    
    return times, decimals1, decimals2, decimals3, decimals4, decimals5, decimals6, decimals7, decimals8

def compare_CAN_log(HSCAN1, HSCAN2):
    times,B1,B2,B3,B4,B5,B6,B7,B8 = get_data(canFrame, HSCAN1)
    times,B10,B20,B30,B40,B50,B60,B70,B80 = get_data(canFrame, HSCAN2)
    plot_CAN_log(times,B1,B2,B3,B4,B5,B6,B7,B8)
    plot_CAN_log(times,B10,B20,B30,B40,B50,B60,B70,B80)

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

canFrame = pd.read_csv("voice command open window wrong (left opened) 7-14-2022 2-35-37 pm.csv", sep=',', skiprows=61)
times,B1,B2,B3,B4,B5,B6,B7,B8 = get_data(canFrame, "HS CAN $1C6")
'''fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")'''

canvas = FigureCanvasTkAgg(plot_CAN_log(times,B1,B2,B3,B4,B5,B6,B7,B8), master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)


def update_frequency(new_val):
    # retrieve frequency
    f = float(new_val)

    # update data
    y = 2 * np.sin(2 * np.pi * f * t)
    line.set_data(t, y)

    # required to update canvas and attached toolbar!
    canvas.draw()


slider_update = tkinter.Scale(root, from_=1, to=5, orient=tkinter.HORIZONTAL,
                              command=update_frequency, label="Frequency [Hz]")

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tkinter.BOTTOM)
slider_update.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

tkinter.mainloop()