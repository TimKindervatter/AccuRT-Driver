#!/usr/bin/python3
# script to run AccuRT in a loop
# also can edit config file tags (to be added)

import os, sys
import numpy as np
import matplotlib.pyplot as plt

accurt_python_driver_path = os.environ.get('ACCURT_PYTHON_DRIVER_PATH')
sys.path.insert(1, accurt_python_driver_path)

from ConfigFile import *
from MaterialEnum import Material
from ConfigFileTypeEnum import ConfigFileType
from utils import *


# This will be used to find the config file that you will use as a template
template_config_name = "default"  # Change this to the name of the config file you would like to use as a template

# Programmatically set up text file(s) to be used for repeated runs (not needed if not using repeated run)
repeated_run_file_location = ConfigFileType.MATERIAL  # Determines whether repeated run file will be placed alongside the main config file or in the materials folder 

desired_depth = np.array([0, 0.01, 0.1, 0.5])
volume_fraction = 2.8e-11
depth = 0.37800547865663

aerosol_volume_fractions = volume_fraction*(desired_depth/depth)

aerosol_volume_fractions_file_name = 'aerosol_volume_fractions.txt'
aerosol_volume_fractions_file_handle = open_repeated_run_text_file(aerosol_volume_fractions_file_name, template_config_name, repeated_run_file_location)

for aerosol_volume_fraction in aerosol_volume_fractions:
    aerosol_volume_fractions_file_handle.write("6 " + str(aerosol_volume_fraction) + '\n')
    aerosol_volume_fractions_file_handle.flush()

main_config_dict = {
    "name" : "Main",
    "SOURCE_TYPE" : "earth_solar",
    "SOURCE_ZENITH_ANGLE" : "45",
    "BOTTOM_BOUNDARY_SURFACE" : "white",
    "BOTTOM_BOUNDARY_SURFACE_SCALING_FACTOR" : "0.95",
    "STREAM_UPPER_SLAB_SIZE" : "16",
    "MATERIALS_INCLUDED_LOWER_SLAB" : "vacuum",
    "DETECTOR_DEPTHS_LOWER_SLAB" : "0.0001",
    "DETECTOR_WAVELENGTHS" : "532",
    "SAVE_MATERIAL_PROFILE" : "false",
    "REPEATED_RUN_SIZE" : str(aerosol_volume_fractions.size)
}

aerosols_dict = {
    "MATERIAL_PROFILE" : aerosol_volume_fractions_file_name,
    "FINE_MODE_FRACTION" : "1.0"
}

tags_to_print = [main_config_dict]

print_updated_tags(tags_to_print)

clone_name_suffix = ""

clone_config_name = clone(template_config_name, clone_name_suffix)

main_config_file = MainConfigFile(template_config_name, clone_config_name)
aerosols_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.AEROSOLS)

main_config_file.updateTags(main_config_dict)
aerosols_config_file.updateTags(aerosols_dict)

run_accurt(clone_config_name)

output_folder = clone_config_name + "Output"
downward_irradiances_filename = output_folder + "/cosine_irradiance_total_downward.txt"
cosine_irradiances_total_downward = read_irradiance(downward_irradiances_filename)

irradiances = np.array([struct.irradiance[1] for struct in cosine_irradiances_total_downward])

plt.figure(1)
plt.plot(desired_depth, irradiances)
plt.title('Cosine Irradiance Total Upward vs Aerosol Optical Depth, 532 nm')
plt.xlabel('Aerosol Volume Fraction')
plt.ylabel('Cosine Irradiance Total Downward')
plt.savefig('aerosol_depletion.png')