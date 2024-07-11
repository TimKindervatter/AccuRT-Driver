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
repeated_run_file_location = ConfigFileType.MAIN # Determines whether repeated run file will be placed alongside the main config file or in the materials folder 

source_zenith_angles = np.arange(5, 90, 5)
print(source_zenith_angles.size)

source_zenith_angle_file_name = 'source_zenith_angle.txt'
source_zenith_angle_file_handle = open_repeated_run_text_file(source_zenith_angle_file_name, template_config_name, repeated_run_file_location)


for source_zenith_angle in source_zenith_angles:
    source_zenith_angle_file_handle.write(str(source_zenith_angle) + '\n')
    source_zenith_angle_file_handle.flush()

main_config_dict = {
    "name" : "Main",
    "SOURCE_TYPE" : "earth_solar",
    "SOURCE_ZENITH_ANGLE" : source_zenith_angle_file_name,
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
    "REPEATED_RUN_SIZE" : str(source_zenith_angles.size)
}

tags_to_print = [main_config_dict]

print_updated_tags(tags_to_print)

# change this to the name of your config file
template_config_name = "default"
clone_name_suffix = ""

clone_config_name = clone(template_config_name, clone_name_suffix)

main_config_file = MainConfigFile(template_config_name, clone_config_name)
material_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.EARTH_ATMOSPHERIC_GASES)

main_config_file.updateTags(main_config_dict)


run_accurt(clone_config_name)

output_folder = clone_config_name + "Output"
downward_irradiances_filename = output_folder + "/cosine_irradiance_total_downward.txt"
cosine_irradiances_total_downward = read_irradiance(downward_irradiances_filename)

irradiances_above_surface = np.array([struct.irradiance[0] for struct in cosine_irradiances_total_downward])
irradiances_below_surface = np.array([struct.irradiance[1] for struct in cosine_irradiances_total_downward])
Delta_F_minus = irradiances_below_surface - irradiances_above_surface

plt.plot(source_zenith_angles, Delta_F_minus)
plt.title('Delta F^- vs Source Zenith Angle')
plt.xlabel('Source Zenith Angle (deg)')
plt.ylabel('Delta F^-')
plt.savefig('delta_f_minus.png')
