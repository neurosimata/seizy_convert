# -*- coding: utf-8 -*-

### --------------- IMPORTS --------------- ###
import os
import pyedflib
import numpy as np
### --------------------------------------- ###

def create_test_edf(file_name, n_channels=2, sample_rate=100, duration=10, signal_type='valid'):
    """
    Function to create small .edf files for testing.
    
    Parameters
    ----------
    file_name : str
        Name of the .edf file to be created.
    n_channels : int
        Number of channels in the edf file.
    sample_rate : int
        Sampling rate for the signal.
    duration : int
        Duration of the signal in seconds.
    signal_type : str
        Type of signal ('valid', 'low_sampling_rate', 'missing_channels', 'empty_signal')
    
    Returns
    -------
    None
    """
    # Create signal data based on type
    n_samples = sample_rate * duration
    
    if signal_type == 'valid':
        signals = [np.sin(2 * np.pi * np.arange(n_samples) / sample_rate) for _ in range(n_channels)]
    elif signal_type == 'low_sampling_rate':
        sample_rate = 50  # intentionally too low
        signals = [np.sin(2 * np.pi * np.arange(sample_rate * duration) / sample_rate) for _ in range(n_channels)]
    elif signal_type == 'missing_channels':
        # Intentionally only one channel for testing missing channels
        signals = [np.sin(2 * np.pi * np.arange(n_samples) / sample_rate)]
    elif signal_type == 'empty_signal':
        # Channels with zero signal
        signals = [np.zeros(n_samples) for _ in range(n_channels)]
    else:
        raise ValueError("Unknown signal type")
    
    # Create a new EDF file
    f = pyedflib.EdfWriter(file_name, n_channels, file_type=pyedflib.FILETYPE_EDFPLUS)

    channel_info = []
    for i in range(n_channels):
        channel_dict = {
            'label': f'Channel_{i+1}',
            'dimension': 'uV',
            'sample_rate': sample_rate,
            'physical_max': 1000,
            'physical_min': -1000,
            'digital_max': 32767,
            'digital_min': -32768,
            'transducer': '',
            'prefilter': ''
        }
        channel_info.append(channel_dict)

    f.setSignalHeaders(channel_info)
    f.writeSamples(signals)
    f.close()

# Create test .edf files in a directory called "test_edf_files"
os.makedirs('test_edf_files', exist_ok=True)

# Create a valid EDF file
create_test_edf('test_edf_files/valid_1000hz_2channels.edf', n_channels=2, sample_rate=1000, duration=20, signal_type='valid')

# Create a valid EDF file
create_test_edf('test_edf_files/valid_500hz_3channels.edf', n_channels=3, sample_rate=500, duration=30, signal_type='valid')

# Create an EDF file with a low sampling rate
create_test_edf('test_edf_files/low_sampling_rate_3channels.edf', n_channels=3, sample_rate=50, duration=10, signal_type='low_sampling_rate')

# Create an EDF file with missing channels
create_test_edf('test_edf_files/missing_channels_1channel.edf', n_channels=1, sample_rate=100, duration=10, signal_type='missing_channels')

# Create an EDF file with empty signals
create_test_edf('test_edf_files/empty_signal_2channels.edf', n_channels=2, sample_rate=100, duration=10, signal_type='empty_signal')

print('--> Test EDF files created.\n')