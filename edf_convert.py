# -*- coding: utf-8 -*-

### --------------- IMPORTS --------------- ###
import os, sys, json
import tables
import pyedflib
import numpy as np
from scipy import signal
from tqdm import tqdm
### --------------------------------------- ###

class EdfConvert:
    """ Class for conversion of .edf files to .h5 format.
    """
    
    def __init__(self, prop_dict):
        """

        Parameters
        ----------
        prop_dict : Dict, with properties from config.json file

        Returns
        -------
        None.

        """
        
        # get values from dictionary
        for key, value in prop_dict.items():
               setattr(self, key, value)
        
        self.winsize = int(self.new_fs*self.win)
        self.filelist = list(filter(lambda k: '.edf' in k, os.listdir(self.main_path)))
        self.h5_filelist = list(filter(lambda k: '.h5' in k, os.listdir(self.main_path)))
        
        
    def _read_edf(self, file_name):
        """
        Opens edf file using pyedflib and returns a reference object.
        ----------------------------------------------------------------------

        Parameters
        ----------
        file_name : Str, file name

        Returns
        -------
        fread : pyedflib obj
        """
        
        fread = pyedflib.EdfReader(os.path.join(self.main_path, file_name))
        
        return fread
        
        
    def edf_check(self, file_name, read_length=1000):
        """
        Read small parts of an edf file. Read samples from 
        start, mid and end across all channels of the edf file.
        ----------------------------------------------------------------------
        
        Parameters
        ----------
        file_name : Str, file name
        read_length: Int, Number of samples to be read for each segment
                     Optional, Default = 1000

        Returns
        -------

        """
        
        # open edf file and check if sampling rate is higher than user set sampling rate (default 100Hz)
        f_edf = self._read_edf(file_name)
        sampling_rate = f_edf.getSampleFrequencies()
        if np.any(sampling_rate < self.new_fs):
            raise Exception(f'--> Original sampling rate {sampling_rate} is lower than new sampling rate ({self.new_fs} Hz).\n')
        
        if self.selected_channel_idx is None:
        
            # check whether selected channels exist
            channel_labels = f_edf.getSignalLabels()
            if not set(self.selected_channels) <= set(channel_labels):
                raise Exception(f'--> Selected channels {self.selected_channels} were not found in File: {file_name}. Got {channel_labels} instead.\n')
                                
            # get channel index
            ch_idx = []
            for channel_name in self.selected_channels:
                ch_idx.append(channel_labels.index(channel_name))
        else:
            ch_idx = self.selected_channel_idx
        
        if not set(ch_idx) <= set(np.arange(len(sampling_rate))):
            raise Exception(f'--> Selected channels were not found in file: {file_name}. ' \
                            f'Available channels are {np.arange(len(sampling_rate))} but got channel index: {ch_idx} instead.\n')
        
        # read signal samples from start, mid, and end portions
        for i in ch_idx:
            signal_length = f_edf.getNSamples()[i]
            f_edf.readSignal(chn=i, start=0, n=read_length)
            f_edf.readSignal(chn=i, start=int(signal_length/2), n=read_length)               
            f_edf.readSignal(chn=i, start=int(signal_length - read_length - 1) , n=read_length)
            
        del f_edf
    
    def edf_to_h5(self, file_name):
        """
        Convert an edf to h5 file.
        
        h5 file shape:
        1st-dimension, X = nSamples/Y
        2nd-dimension, Y = win * new_fs
        3rd-dimension, Z = number of channels
        Where 'nSamples' is the number of samples in one channel of the edf file.
        ----------------------------------------------------------------------
        
        Parameters
        ----------
        file_name : Str, file name

        Returns
        -------

        """
        
        # open edf reader and get number of rows
        # assuming recorded time is the same across channels different sampling rate should not affect number of rows
        f_edf = self._read_edf(file_name)
        sampling_rate = f_edf.getSampleFrequencies()
        down_factor = int(sampling_rate[0]/self.new_fs)
        nrows = int(f_edf.getNSamples()[0]/down_factor/self.winsize)

        # get channel index
        if self.selected_channel_idx is None:
            channel_labels = f_edf.getSignalLabels()
            ch_idx = []
            for channel_name in self.selected_channels:
                ch_idx.append(channel_labels.index(channel_name))
        else:
            ch_idx = self.selected_channel_idx
        
        # open tables object for saving
        with tables.open_file(os.path.join(self.main_path, file_name.replace('.edf','.h5')), mode='w') as fsave:
            # create data store
            ds = fsave.create_earray(fsave.root, 'data', tables.Float64Atom(), shape=[nrows, self.winsize, 0])
            
            # iterate over channels to preprocess signal (decimate, scale, reshape) and append to datastore
            for ch_num in ch_idx: # iterate over channels

                fs = f_edf.getSampleFrequency(ch_num)
                down_factor = int(fs/self.new_fs)
                data = signal.decimate(f_edf.readSignal(ch_num), down_factor) * self.scale
                # trim data to winsize*rows and reshape
                data = np.reshape(data[:self.winsize*nrows], (-1, self.winsize, 1))
                ds.append(data)
                
        del f_edf 
        
                
    def all_files(self, func):
        """
        Run func operation on all edf files in parent edf directory.
        ----------------------------------------------------------------------

        Parameters
        ----------
        func : Function or method for manipulation of one edf file

        Returns
        -------
        bool : False/True for successful/unsuccessful operation

        """
        
        # get file list and iterate over all files for conversion
        try:
            for file in tqdm((self.filelist), desc='Progress', file=sys.stdout, total=len(self.filelist)):
                func(file)
            return False
        
        except Exception as err:
            print(f'\n -> Error! File: {file} could not be read.\n {str(err)}\n')
            return True


def run_conversion(config_path='config.json'):
    # load properties from configuration file
    openpath = open( config_path, 'r').read(); 
    prop_dict = json.loads(openpath)
        
    # get parent directory
    main_path = input('Please enter path of folder containing edf files: \n')
    if not os.path.isdir(main_path):
        print('---> Path:', "'" + main_path + "'", 'is not valid.\n Please enter a valid path.')
        sys.exit()
    else:
        prop_dict.update({'main_path':main_path})
    
    # init object
    obj = EdfConvert(prop_dict)
    if len(obj.filelist) == 0:
        print('--> No Edf files were detected.')
        sys.exit()
    
    # Verify how to proceed
    if len(obj.h5_filelist) > 0:
        options = ['y', 'n']
        answer = ''
        while answer not in options:
            answer = input(f'H5 files were detected and proceeding might overwrite them. Continue? {str(options)}\n')
            if answer not in options:
                print('\n---> Input error: Please choose one of the following options:', str(options) +'.', 
                      'This was received instead:', str(answer)+'\n')
            if answer == 'n':
                 print('\n---> No Further Action Will Be Performed.\n')
                 sys.exit()

    print('\n---------------------------------------------------------------------')
    print(f'{len(obj.filelist)} files were detected. Initiate Error Check: \n')
    
    success = obj.all_files(obj.edf_check)

    print('\n------------------------ Error Check Finished -----------------------')
    print('---------------------------------------------------------------------\n')
    
    if success == False:
        print('-> File Check Completed Successfully.\n')  
    else:
        print('--> Warning! File check was not successful. Please remove/edit problematic edf files or adjust the config file.\n')
        sys.exit()
        
    # Verify how to proceed
    options = ['y', 'n']
    answer = ''
    while answer not in options:
        answer = input(f'Would you like to proceed with File Conversion? {options}\n')
        if answer not in options:
            print('\n---> Input error: Please choose one of the following options:', str(options) +'.', 
                  'This was received instead:', str(answer)+'\n')
        
    if answer == 'n':
         print('\n---> No Further Action Will Be Performed.\n')
         sys.exit()
        
    elif answer == 'y':
        
        print('\n-------------------------------------------------------------------------------')
        print('------------------------ Initiating edf -> h5 Conversion ----------------------\n')
        
        obj.all_files(obj.edf_to_h5)
        
        print('\n************************* Conversion Completed *************************\n')            
    
if __name__ == '__main__':
    run_conversion(config_path='config.json')
