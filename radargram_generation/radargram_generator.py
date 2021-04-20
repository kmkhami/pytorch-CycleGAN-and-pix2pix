"""
Generates radargrams from .nc files.

Files should be located in data sub-directory
"""
from os import listdir, getcwd
from os.path import isdir, join, dirname, split
import numpy as np
import netCDF4 as nc
from PIL import Image


def convert_to_pixel_values(data):
    """Normalizes data between 0 and 255 for conversion into a greyscale image."""
    return 255*(data-np.amin(data))/(np.amax(data)-np.amin(data))


def create_radargram(file_path):
    """Creates a radargram from the .nc file at the specified path."""
    _, file_name = split(file_path)
    file_name = file_name[:-3]
    dataset = nc.Dataset(file_path)
    # Extract data values in np format
    low_gain = np.asarray(dataset['amplitude_low_gain'])
    high_gain = np.asarray(dataset['amplitude_high_gain'])
    low_gain = convert_to_pixel_values(low_gain)
    high_gain = convert_to_pixel_values(high_gain)
    # Save data as images
    Image.fromarray(low_gain.T).convert("L").save("images/"+file_name+"_LOW.png")
    Image.fromarray(high_gain.T).convert("L").save("images/"+file_name+"_HIGH.png")

# Iterates over every file and converts it into a radargram.
path = join(dirname(getcwd()),'data')
dirs = listdir(path)

for folder in dirs:
    tmp_path = join(path, folder)
    if isdir(tmp_path):
        files = listdir(tmp_path)
        for file in files:
            if file.endswith(".nc"):
                create_radargram(join(tmp_path, file))
