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
repeated_run_file_location = ConfigFileType.MAIN  # Determines whether repeated run file will be placed alongside the main config file or in the materials folder 

snow_depths = np.arange(99.9990e3, 100e3, 0.0001e3)
print(snow_depths.size)

snow_depth_file_name = 'snow_depth.txt'
snow_depth_file_handle = open_repeated_run_text_file(snow_depth_file_name, template_config_name, repeated_run_file_location)


for snow_depth in snow_depths:
    profile = "30.0e3 50.0e3 60.0e3 70.0e3 76.0e3 80.0e3 84.0e3 88.0e3 90.0e3 92.0e3 94.0e3 96.0e3 98.0e3 " +  str(snow_depth) + " 100.0e3"
    snow_depth_file_handle.write(profile + '\n')
    snow_depth_file_handle.flush()

detector_wavelength_tags = ["300:50:2500", "500"]
cosine_irradiances = []

snow_config_dict = {
    "name" : "Snow",
    "SNOW_PROFILE" : "15 200",
    "GRAIN_EFFECTIVE_RADIUS" : "15 50",
    "IMPURITY_PROFILE" : "15 1e-7",
}

for detector_wavelength_tag in detector_wavelength_tags:

    main_config_dict = {
        "name": "Main",
        "SOURCE_TYPE" : "earth_solar",
        "BOTTOM_BOUNDARY_SURFACE" : "white",
        "BOTTOM_BOUNDARY_SURFACE_SCALING_FACTOR" : "0.0",
        "STREAM_UPPER_SLAB_SIZE" : "16",
        "LAYER_DEPTHS_UPPER_SLAB" : snow_depth_file_name,
        "MATERIALS_INCLUDED_UPPER_SLAB" : "earth_atmospheric_gases snow",
        "MATERIALS_INCLUDED_LOWER_SLAB" : "vacuum",
        "DETECTOR_DEPTHS_UPPER_SLAB" : "99.999e3",
        "DETECTOR_DEPTHS_LOWER_SLAB" : "0",
        "DETECTOR_AZIMUTH_ANGLES" : "0",
        "DETECTOR_POLAR_ANGLES" : "0 180",
        "DETECTOR_WAVELENGTHS" : detector_wavelength_tag,
        "SAVE_MATERIAL_PROFILE" : "false",
        "REPEATED_RUN_SIZE" : str(snow_depths.size),
    }


    tags_to_print = [main_config_dict, snow_config_dict]

    print_updated_tags(tags_to_print)

    clone_name_suffix = ""

    clone_config_name = clone(template_config_name, clone_name_suffix)

    main_config_file = MainConfigFile(template_config_name, clone_config_name)
    earth_atmospheric_gases_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.EARTH_ATMOSPHERIC_GASES)
    snow_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.SNOW)

    main_config_file.updateTags(main_config_dict)
    snow_config_file.updateTags(snow_config_dict)


    run_accurt(clone_config_name)
    cosine_irradiances_total_downward = extract_downward_radiances(clone_config_name)
    cosine_irradiances.append(cosine_irradiances_total_downward)

F_spectrum = cosine_irradiances[0]
F_total = np.sum(F_spectrum, axis=1)
F_500 = cosine_irradiances[1].flatten()
ratio = F_500/F_total

depth_of_snow_layer = 100e3 - snow_depths

plt.plot(depth_of_snow_layer, ratio)
plt.title('Downward Ratio F_500/F_total vs Snow Depth')
plt.xlabel('Snow Depth (m)')
plt.ylabel('F_500/F_total')
plt.savefig('cosine_irradiance_total_downward.png')
