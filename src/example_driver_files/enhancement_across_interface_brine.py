#!/usr/bin/python3

import os, sys
import numpy as np
import matplotlib.pyplot as plt

accurt_python_driver_path = os.environ.get('ACCURT_PYTHON_DRIVER_PATH')
sys.path.insert(1, accurt_python_driver_path)

from ConfigFile import MainConfigFile, MaterialConfigFile
from MaterialEnum import Material
from ConfigFileTypeEnum import ConfigFileType
from utils import *


# This will be used to find the config file that you will use as a template
template_config_name = "default"  # Change this to the name of the config file you would like to use as a template


# Programmatically set up text file(s) to be used for repeated runs (not needed if not using repeated run)
config_file_type = ConfigFileType.MATERIAL

brine_volume_fractions = np.arange(0.01, 0.06, 0.01)
print(brine_volume_fractions.size)

brine_volume_fractions_file_name = 'brine_volume_fractions.txt'
brine_volume_fractions_file_handle = open_repeated_run_text_file(brine_volume_fractions_file_name, template_config_name, config_file_type)

for brine_volume_fraction in brine_volume_fractions:
    brine_volume_fractions_file_handle.write('1 ' + str(brine_volume_fraction) + ' 2 ' + str(brine_volume_fraction) + '\n')
    brine_volume_fractions_file_handle.flush()


# Set up values to put in config files. Any values listed here will replace those in the template config file.
# Any values not listed here will simply use the values from the template config file.
main_config_tags = {
    "name" : "Main",
    "SOURCE_TYPE" : "earth_solar",
    "SOURCE_ZENITH_ANGLE" : "45",
    "BOTTOM_BOUNDARY_SURFACE" : "white",
    "BOTTOM_BOUNDARY_SURFACE_SCALING_FACTOR" : "0.0",
    "LAYER_DEPTHS_LOWER_SLAB" : "0.000001 100",
    "MATERIALS_INCLUDED_UPPER_SLAB" : "earth_atmospheric_gases",
    "MATERIALS_INCLUDED_LOWER_SLAB" : "ice",
    "DETECTOR_DEPTHS_UPPER_SLAB" : "99.999e3",
    "DETECTOR_DEPTHS_LOWER_SLAB" : "0.001",
    "DETECTOR_AZIMUTH_ANGLES" : "0",
    "DETECTOR_POLAR_ANGLES" : "0 180",
    "DETECTOR_WAVELENGTHS" : "532",
    "SAVE_MATERIAL_PROFILE" : "false",
    "REPEATED_RUN_SIZE" : str(brine_volume_fractions.size)
}

ice_config_tags = {
    "name" : "Ice",
    "BRINE_PROFILE" : brine_volume_fractions_file_name
}


# Print out the tags that will be changed from their default values. These values will print to the command line.
tags_to_print = [main_config_tags, ice_config_tags]
print_updated_tags(tags_to_print)


# Create a "clone" of the template config file and Materials directory, but with modified tags according to those listed above.
clone_name_suffix = ""  # If running in a loop, you may choose to add a suffix to each clone file/directory name to avoid overwriting the files/directories from previous loops
clone_config_name = clone(template_config_name, clone_name_suffix)

main_config_file = MainConfigFile(template_config_name, clone_config_name)
earth_gases_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.EARTH_ATMOSPHERIC_GASES)
ice_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.ICE)

main_config_file.updateTags(main_config_tags)
ice_config_file.updateTags(ice_config_tags)


# Run AccuRT on the cloned config file
run_accurt(clone_config_name)


# Open an output file that was generated in the Output directory and read the values out of it
output_folder = clone_config_name + "Output"
downward_irradiances_filename = output_folder + "/cosine_irradiance_total_downward.txt"
cosine_irradiances_total_downward = read_irradiance(downward_irradiances_filename)


# Format data for plotting
irradiances_above_surface = np.array([array[0] for array in cosine_irradiances_total_downward])
irradiances_below_surface = np.array([array[1] for array in cosine_irradiances_total_downward])
Delta_F_minus = irradiances_below_surface - irradiances_above_surface


# Plot output data
plt.plot(brine_volume_fractions, Delta_F_minus)
plt.title('Delta F^- vs Brine Volume Fraction')
plt.xlabel('Brine Volume Fraction')
plt.ylabel('Delta F^-')
plt.savefig('delta_f_minus.png')
