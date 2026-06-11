#!/usr/bin/python3

import os, sys
import numpy as np
import matplotlib.pyplot as plt

accurt_python_driver_path = os.environ.get('ACCURT_PYTHON_DRIVER_PATH')
sys.path.insert(1, accurt_python_driver_path)

from ConfigFile import ConfigFileCopier
from utils import *


# This will be used to find the config file that you will use as a template
template_config_name = "default_AccuRT_config"  # Change this to the name of the config file you would like to use as a template

brine_volume_fractions = np.arange(0.01, 0.06, 0.01)

irradiances_above_surface = []
irradiances_below_surface = []

for i, brine_volume_fraction in enumerate(brine_volume_fractions):
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
    }

    ice_config_tags = {
        "name" : "Ice",
        "BRINE_PROFILE" : f"1 {brine_volume_fraction} 2 {brine_volume_fraction}"
    }

    tags_to_print = [main_config_tags, ice_config_tags]
    print_updated_tags(tags_to_print)  # Print out the tags that will be changed from their default values. These values will print to the command line.

    config_file_copier = ConfigFileCopier(template_config_name, clone_name_suffix=str(i))
    clone_config_name = config_file_copier.clone_config_name

    config_file_copier.updateMainConfigTags(main_config_tags)
    config_file_copier.updateIceConfigTags(ice_config_tags)

    # Run AccuRT on the cloned config file
    run_accurt(clone_config_name)


    # Open an output file that was generated in the Output directory and read the values out of it
    output_folder = clone_config_name + "Output"
    downward_irradiances_filename = output_folder + "/cosine_irradiance_total_downward.txt"
    cosine_irradiances_total_downward = read_irradiance(downward_irradiances_filename)


    # Format data for plotting
    irradiances_above_surface.append(cosine_irradiances_total_downward.irradiance[0])
    irradiances_below_surface.append(cosine_irradiances_total_downward.irradiance[1])
    
    
Delta_F_minus = np.array(irradiances_below_surface) - np.array(irradiances_above_surface)

# Plot output data
plt.plot(brine_volume_fractions, Delta_F_minus)
plt.title('Delta F^- vs Brine Volume Fraction')
plt.xlabel('Brine Volume Fraction')
plt.ylabel('Delta F^-')
plt.savefig('delta_f_minus.png')
