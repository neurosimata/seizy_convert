# -*- coding: utf-8 -*-

### --------------- IMPORTS --------------- ###
import os
import sys
import tables
import matplotlib.pyplot as plt
### --------------------------------------- ###.

def test_load_h5(file_path):
    # open file
    with tables.open_file(file_path, mode='r') as h5file:
        data = h5file.root.data[:]
        print(f'--> Data loaded successfully with shape: {data.shape}.\n')
    
    # plot the first segment from each channel
    n_channels = data.shape[2]
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    f, axs = plt.subplots(nrows=n_channels)
    for i,ax in zip(range(n_channels), axs):
        ax.plot(data[0,:,i], label='channel_'+str(i+1), color=default_colors[i])
        ax.legend()
    plt.show()

if __name__ == '__main__':
    input_path = input('Please enter h5 file to open and plot the first segment:')
    file_path = input_path.replace('"', '')
    if os.path.isfile(file_path) is False:
        print(f'File: {file_path} was not found.\n')
        sys.exit()
    else:
        test_load_h5(file_path)
        
    