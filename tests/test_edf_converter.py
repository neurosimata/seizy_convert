# -*- coding: utf-8 -*-

### --------------- IMPORTS --------------- ###
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)
from edf_convert import EdfConvert
### --------------------------------------- ###

# Helper function to run tests and print results
def run_test(test_func):
    try:
        test_func()
        print(f"{test_func.__name__}: Passed")
    except AssertionError as e:
        print(f"{test_func.__name__}: Failed - {e}")
    except Exception as e:
        print(f"{test_func.__name__}: Failed - {e}")

# 1. Test with a valid EDF file
def test_valid_file_config1():
    try:
        properties = {"new_fs": 100, "win": 5, "scale": 1, "selected_channels":["Channel_1", "Channel_2"],
                      "selected_channel_idx":None, "main_path": "test_edf_files"}
        converter = EdfConvert(properties)
        converter.edf_check('valid_1000hz_2channels.edf')
        assert True  # If no exception is raised, the test is passed
    except Exception as e:
        assert False, f"Valid EDF test failed: {e}"
        
# 2. Test with a valid EDF file
def test_valid_file_config2():
    try:
        properties = {"new_fs": 100, "win": 5, "scale": 1, "selected_channels":["Channel_1", "Channel_2", "Channel_3"],
                      "selected_channel_idx":None, "main_path": "test_edf_files"}
        converter = EdfConvert(properties)
        converter.edf_check('valid_500hz_3channels.edf')
        assert True  # If no exception is raised, the test is passed
    except Exception as e:
        assert False, f"Valid EDF test failed: {e}"
        
# 3. Test with a valid EDF file
def test_valid_file_channel_idx():
    try:
        properties = {"new_fs": 100, "win": 5, "scale": 1, "selected_channels":["Channel_1", "Channel_2", "Channel_3"],
                      "selected_channel_idx":[0,2], "main_path": "test_edf_files"}
        converter = EdfConvert(properties)
        converter.edf_check('valid_500hz_3channels.edf')
        assert True  # If no exception is raised, the test is passed
    except Exception as e:
        assert False, f"Valid EDF test failed: {e}"
        
# 4. Test with missing channels EDF file
def test_missing_channel_ch_names():
    try:
        properties = {"new_fs": 100, "win": 5, "scale": 1, "selected_channels":["Channel_1", "Channel_2"],
                      "selected_channel_idx":None, "main_path": "test_edf_files"}
        converter = EdfConvert(properties)
        converter.edf_check('missing_channels_1channel.edf')
        assert False, "Expected exception for missing channels, but none was raised"
    except Exception as e:
        assert 'Selected channels' in str(e), f"Unexpected exception: {e}"
        
# 5. Test with a valid EDF file
def test_missing_channel_ch_idx():
    try:
        properties = {"new_fs": 100, "win": 5, "scale": 1, "selected_channels":["Channel_1", "Channel_2", "Channel_3"],
                      "selected_channel_idx":[0,2], "main_path": "test_edf_files"}
        converter = EdfConvert(properties)
        converter.edf_check('valid_1000hz_2channels.edf')
        assert False, "Expected exception for missing channels, but none was raised"
    except Exception as e:
        assert 'Selected channels' in str(e), f"Unexpected exception: {e}"

# 6. Test with a low sampling rate EDF file
def test_low_sampling_rate():
    try:
        properties = {"new_fs": 100, "win": 5, "scale": 1, "selected_channels":["Channel_1", "Channel_2", "Channel_3"],
                      "selected_channel_idx":None, "main_path": "test_edf_files"}
        converter = EdfConvert(properties)
        converter.edf_check('low_sampling_rate_3channels.edf')
        assert False, "Expected exception for low sampling rate, but none was raised"
    except Exception as e:
        assert 'Original sampling rate' in str(e), f"Unexpected exception: {e}"

# 7. Test with empty signal EDF file
def test_empty_signal():
    try:
        properties = {"new_fs": 100, "win": 5, "scale": 1, "selected_channels":["Channel_1", "Channel_2", "Channel_3"],
                      "selected_channel_idx":None, "main_path": "test_edf_files"}
        converter = EdfConvert(properties)
        converter.edf_check('empty_signal.edf')
        assert False
    except Exception as e:
        assert True, f"Valid EDF test failed: {e}"

# Run the tests
print('\n------------- Initiating Tests: ------------------\n')
run_test(test_valid_file_config1)
run_test(test_valid_file_config2)
run_test(test_valid_file_channel_idx)
run_test(test_missing_channel_ch_names)
run_test(test_missing_channel_ch_idx)
run_test(test_low_sampling_rate)
run_test(test_empty_signal)
print('\n--------------- Tests completed. -----------------\n')
