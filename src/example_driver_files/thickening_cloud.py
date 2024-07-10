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
repeated_run_file_location = ConfigFileType.MATERIAL  # Determines whether repeated run file will be placed alongside the main config file or in the materials folder 

cloud_volume_fractions = np.linspace(1e-9, 9.9e-8, 100)
repeated_run_size = cloud_volume_fractions.size

repeated_run_file_name = 'profile.txt'
repeated_run_file_handle = open_repeated_run_text_file(repeated_run_file_name, template_config_name, repeated_run_file_location)

for cloud_volume_fraction in cloud_volume_fractions:
    repeated_run_file_handle.write('2 ' + str(cloud_volume_fraction) + '\n')
    repeated_run_file_handle.flush()

# Set up values to put in config files. Any values listed here will replace those in the template config file.
# Any values not listed here will simply use the values from the template config file.
main_config_tags = {
    "name" : "Main",
    "SOURCE_TYPE" : "constant_one",
    "SOURCE_ZENITH_ANGLE" : "53",
    "BOTTOM_BOUNDARY_SURFACE" : "white",
    "BOTTOM_BOUNDARY_SURFACE_SCALING_FACTOR" : "0.0",
    "LAYER_DEPTHS_UPPER_SLAB" : "96.0e3 98.0e3 100.0e3",
    "LAYER_DEPTHS_LOWER_SLAB" : "100",
    "MATERIALS_INCLUDED_UPPER_SLAB" : "cloud",
    "MATERIALS_INCLUDED_LOWER_SLAB" : "vacuum",
    "DETECTOR_DEPTHS_UPPER_SLAB" : "96.0e3 98.0e3",
    "DETECTOR_DEPTHS_LOWER_SLAB" : "0.001",
    "DETECTOR_AZIMUTH_ANGLES" : "0",
    "DETECTOR_POLAR_ANGLES" : "180",
    "DETECTOR_WAVELENGTHS" : "532",
    "SAVE_RADIANCE" : "true",
    "SAVE_IOPS" : "true",
    "REPEATED_RUN_SIZE" : str(repeated_run_size)
}

cloud_config_tags = {
    "name" : "Cloud",
    "CLOUD_PROFILE" : repeated_run_file_name,
    "USE_PARAMETERIZED_MIE_CODE" : "false"
}


# Print out the tags that will be changed from their default values. These values will print to the command line.
tags_to_print = [main_config_tags, cloud_config_tags]
print_updated_tags(tags_to_print)


# Create a "clone" of the template config file and Materials directory, but with modified tags according to those listed above.
clone_name_suffix = ""  # If running in a loop, you may choose to add a suffix to each clone file/directory name to avoid overwriting the files/directories from previous loops
clone_config_name = clone(template_config_name, clone_name_suffix)

main_config_file = MainConfigFile(template_config_name, clone_config_name)
cloud_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.CLOUD)

main_config_file.updateTags(main_config_tags)
cloud_config_file.updateTags(cloud_config_tags)


# Run AccuRT on the cloned config file
run_accurt(clone_config_name)


# Open an output file that was generated in the Output directory and read the values out of it
output_folder = clone_config_name + "Output"
diffuse_downward_irradiances_filename = output_folder + "/cosine_irradiance_diffuse_downward.txt"
cosine_irradiances_diffuse_downward_struct = read_irradiance(diffuse_downward_irradiances_filename)

diffuse_irradiances_below_cloud = np.zeros(repeated_run_size)

# Format data for plotting
for i in range(repeated_run_size):
    irradiances = cosine_irradiances_diffuse_downward_struct[i].irradiance
    irradiance_below_cloud = irradiances[1][0]  # Below cloud = second layer (zero-indexed -> second layer has index 1)
    diffuse_irradiances_below_cloud[i] = irradiance_below_cloud

# Plot output data
plt.plot(cloud_volume_fractions, diffuse_irradiances_below_cloud)
plt.title('Diffuse Downward Irradiances vs Cloud Volume Fraction')
plt.xlabel('Cloud Volume Fraction')
plt.ylabel('Irradiance')
plt.savefig('diffuse_downward_irradiance.png')



total_downward_irradiances_filename = output_folder + "/cosine_irradiance_total_downward.txt"
cosine_irradiances_total_downward_struct = read_irradiance(total_downward_irradiances_filename)

total_irradiances_below_cloud = np.zeros(repeated_run_size)

# Format data for plotting
for i in range(repeated_run_size):
    irradiances = cosine_irradiances_total_downward_struct[i].irradiance
    irradiance_below_cloud = irradiances[1][0]  # Below cloud = second layer (zero-indexed -> second layer has index 1)
    total_irradiances_below_cloud[i] = irradiance_below_cloud

# Plot output data
plt.figure()
plt.plot(cloud_volume_fractions, total_irradiances_below_cloud)
plt.title('Total Downward Irradiances vs Cloud Volume Fraction')
plt.xlabel('Cloud Volume Fraction')
plt.ylabel('Irradiance')
plt.savefig('total_downward_irradiance.png')