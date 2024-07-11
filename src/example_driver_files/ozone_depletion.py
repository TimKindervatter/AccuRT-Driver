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

ozone_fractions = np.array([1.0, 0.95, 0.9, 0.8, 0.7, 0.5])

ozone_fractions_file_name = 'ozone_fractions.txt'
ozone_fractions_file_handle = open_repeated_run_text_file(ozone_fractions_file_name, template_config_name, repeated_run_file_location)

for ozone_fraction in ozone_fractions:
    ozone_fractions_file_handle.write(str(ozone_fraction) + '\n')
    ozone_fractions_file_handle.flush()

main_config_dict = {
    "name" : "Main",
    "SOURCE_TYPE" : "earth_solar",
    "SOURCE_ZENITH_ANGLE" : "45",
    "BOTTOM_BOUNDARY_SURFACE" : "white",
    "BOTTOM_BOUNDARY_SURFACE_SCALING_FACTOR" : "0.95",
    "STREAM_UPPER_SLAB_SIZE" : "16",
    "MATERIALS_INCLUDED_UPPER_SLAB" : "earth_atmospheric_gases",
    "MATERIALS_INCLUDED_LOWER_SLAB" : "vacuum",
    "DETECTOR_DEPTHS_LOWER_SLAB" : "0.0001",
    "DETECTOR_WAVELENGTHS" : "305 340",
    "SAVE_MATERIAL_PROFILE" : "false",
    "REPEATED_RUN_SIZE" : str(ozone_fractions.size)
}

earth_atmospheric_gases_dict = {
    "F_H2O" : "0.0",
    "F_CO2" : "0.0",
    "F_O3" : ozone_fractions_file_name,
    "F_N2O" : "0.0",
    "F_CO" : "0.0",
    "F_CH4" : "0.0",
    "F_O2" : "0.0",
    "F_NO" : "0.0",
    "F_SO2" : "0.0",
    "F_NO2" : "0.0",
    "F_NH3" : "0.0",
    "F_HNO3" : "0.0",
    "F_N2" : "0.0",
    "F_H2O_CON" : "0.0",
    "F_RAY_SCA" : "1.0",
}

tags_to_print = [main_config_dict]

print_updated_tags(tags_to_print)

clone_name_suffix = ""

clone_config_name = clone(template_config_name, clone_name_suffix)

main_config_file = MainConfigFile(template_config_name, clone_config_name)
earth_atmospheric_gases_config_file = MaterialConfigFile(template_config_name, clone_config_name, Material.EARTH_ATMOSPHERIC_GASES)

main_config_file.updateTags(main_config_dict)
earth_atmospheric_gases_config_file.updateTags(earth_atmospheric_gases_dict)

run_accurt(clone_config_name)

output_folder = clone_config_name + "Output"
downward_irradiances_filename = output_folder + "/cosine_irradiance_total_downward.txt"
cosine_irradiances_total_downward = read_irradiance(downward_irradiances_filename)

irradiances_305nm = np.array([struct.irradiance[1][0] for struct in cosine_irradiances_total_downward])
irradiances_340nm = np.array([struct.irradiance[1][1] for struct in cosine_irradiances_total_downward])

plt.figure(1)
plt.plot(ozone_fractions, irradiances_305nm)
plt.title('Cosine Irradiance Total Upward vs Ozone Fraction, 305 nm')
plt.xlabel('Ozone Fraction')
plt.ylabel('Cosine Irradiance Total Downward')
plt.savefig('ozone_depletion_305nm.png')

plt.figure(2)
plt.plot(ozone_fractions, irradiances_340nm)
plt.title('Cosine Irradiance Total Upward vs Ozone Fraction, 340 nm')
plt.xlabel('Ozone Fraction')
plt.ylabel('Cosine Irradiance Total Downward')
plt.savefig('ozone_depletion_340nm.png')