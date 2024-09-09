# SeizyConvert
This is an accompanying toolbox for SeizyML to allow conversion of EEG/LFP recordings to
the appropriate file format. Briefly, the files will be downsampled (decimated) to 100Hz
in 5 second windows and will be converted to HDF5 files (.h5) in the following format:

    1st-dimension = nSegments (ie. Number of 5 second segments)
    2nd-dimension = win * new_fs (Default is 500 : 100 Hz * 5 seconds)
    3rd-dimension = number of channels (Equals to the number of selected channels in the `config.json` file)

- Currently supports the conversion of continuous EDF files containing 1 animal per recording.

### :snake: Dependencies

    pip install numpy, scipy, tables, pyedflib, tqdm

- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- [pytables](https://www.pytables.org/)
- [pyedflib](https://pyedflib.readthedocs.io/en/latest/)
- [tqdm](https://github.com/tqdm/tqdm)

### Configuration settings
The `config.json` file contains the parameters. Usually only the `selected_channels` field needs to be edited by user.

    - win : window size in seconds, Default = 5
    - new_fs : sampling rate after downsampling (samples per second), Default = 100
    - scale : signal scaling factor, Default = 1
    - selected_channels: Name of channels to be selected.
    - selected_channel_idx: Index of channels to be selected. Default is None. Overwrites selected_channels.

### How to use

#### One Animal per File - Select by Channel name
1) Modify the `config.json` file to include the correct channel names. Ensure those channel names are present accross all files.
Using channel names is usually the best option to ensure that the correct channels are selected. 
If for some reason channel names can not be edited to be consistent across channels, `selected_channel_idx` can be used instead.

2) Open anaconda shell and cd to the seizy_convert directory

    cd .\seizy_convert

3) Run the main conversion file and follow the prompt

    python .\edf_convert.py

If all tests pass and conversion completes successfully an equivalent .h5 file will be created for each .edf file in the folder

### Examples
There are example .edf files in the `\example_data` subfolder that we can use to try the app.
1) For example there is a 2 channel file in `\example_data\edf_2channels` with channel names `Channel_1` and `Channel_2`.
2) To convert this file to `.h5` follow the instructions from How-to-use section from [above](###How-to-use) to run the app.
3) When prompted for the parent directory type enter the full path to the `edf_2channels` folder.
4) The converted file can be inspected by running the following:

    python .\inspect_h5file.py

When prompted for the file path copy and paste the path of the converted .h5 file, which will print the data shape and plot the first segment of each channel.

### Updates
Depending on demand new features will be added such as:
1) Multiple Animals per EDF file.
2) Addition of other file format.

### Contributions
We welcome all project contributions including raising issues and pull requests!

---
