import os, shutil
import numpy as np
from collections import deque

from ConfigFileTypeEnum import ConfigFileType

def clone(template_name, clone_name_suffix = "") -> str:
        clone_name = template_name + "_clone" + clone_name_suffix

        if os.path.isfile(clone_name):
            os.remove(clone_name)

        shutil.copy(template_name, clone_name)

        src  = template_name + "Materials"
        dest = clone_name    + "Materials"

        try:
            shutil.rmtree(dest)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

        shutil.copytree(src, dest)

        return clone_name


# def read_irradiance(file_name):
#     with open(file_name, 'r') as f:
#         line_1 = f.readlines(1)[0].strip()
#         n_runs = int(line_1)

#         irradiances = []

#         for i in range(n_runs):
#             line_2 = f.readlines(1)[0].strip()
#             n_streams = int(line_2)

#             line_3 = f.readlines(1)[0].strip().split()
#             n_depths = int(line_3[0])
#             n_wavelengths = int(line_3[1])

#             line_4 = f.readlines(1)[0].strip().split()
#             depths = [float(elem) for elem in line_4]

#             line_5 = f.readlines(1)[0].strip().split()
#             wavelengths = [float(elem) for elem in line_5]

#             irradiances_this_run = np.zeros([n_depths, n_wavelengths])

#             for j in range(n_depths):
#                 line = f.readlines(1)[0]
#                 irradiances_str = line.strip().split()
#                 for k in range(n_wavelengths):
#                     irradiances_this_run[j, k] = float(irradiances_str[k])

#             irradiances.append(irradiances_this_run)

#     return irradiances

class IrradianceStruct:
    def __init__(self):
        self.nStreams = None
        self.nDepths = None
        self.nWavelengths = None
        self.depth = []
        self.wavelength = []
        self.irradiance = []


class RadianceStruct:
    def __init__(self):
        self.nStreams = None
        self.nDepths = None
        self.nWavelengths = None
        self.nPolarAngles = None
        self.nAzimuthAngles = None
        self.depth = []
        self.wavelength = []
        self.polarAngle = []
        self.azimuthAngle = []
        self.radiance = None


def read_irradiance(file_name):
    data = []

    with open(file_name, 'r') as f:
        line_1 = f.readlines(1)[0].strip()
        n_runs = int(line_1)        

        for i in range(n_runs):
            this_run_data = IrradianceStruct()

            line_2 = f.readlines(1)[0].strip()
            this_run_data.nStreams = int(line_2)

            line_3 = f.readlines(1)[0].strip().split()
            this_run_data.nDepths = int(line_3[0])
            this_run_data.nWavelengths = int(line_3[1])

            depths = f.readlines(1)[0].strip().split()
            this_run_data.depth = [float(elem) for elem in depths]

            wavelengths = f.readlines(1)[0].strip().split()
            this_run_data.wavelength = [float(elem) for elem in wavelengths]

            for j in range(this_run_data.nDepths):
                next_line = f.readlines(1)[0].strip().split()
                irradiances = [float(elem) for elem in next_line]
                this_run_data.irradiance.append(irradiances)

            data.append(this_run_data)

    return data


def read_radiance(file_name):
    data = []

    with open(file_name, 'r') as f:
        line_1 = f.readlines(1)[0].strip()
        n_runs = int(line_1)        

        for i in range(n_runs):
            this_run_data = RadianceStruct()

            line_2 = f.readlines(1)[0].strip()
            this_run_data.nStreams = int(line_2)

            line_3 = f.readlines(1)[0].strip().split()
            this_run_data.nDepths = int(line_3[0])
            this_run_data.nWavelengths = int(line_3[1])
            this_run_data.nPolarAngles = int(line_3[2])
            this_run_data.nAzimuthAngles = int(line_3[3])

            depths = f.readlines(1)[0].strip().split()
            this_run_data.depth = [float(elem) for elem in depths]

            wavelengths = f.readlines(1)[0].strip().split()
            this_run_data.wavelength = [float(elem) for elem in wavelengths]

            polar_angles = f.readlines(1)[0].strip().split()
            this_run_data.polarAngle = [float(elem) for elem in polar_angles]

            azimuth_angles = f.readlines(1)[0].strip().split()
            this_run_data.azimuthAngle = [float(elem) for elem in azimuth_angles]

            radiances = np.zeros((this_run_data.nDepths, this_run_data.nWavelengths, this_run_data.nPolarAngles, this_run_data.nAzimuthAngles))

            radiance_line = f.readlines(1)[0].strip().split()
            radiance_queue = deque(radiance_line)

            for j in range(this_run_data.nDepths):
                for k in range(this_run_data.nWavelengths):
                    for l in range(this_run_data.nPolarAngles):
                        for m in range(this_run_data.nAzimuthAngles):
                            radiances[j, k, l, m] = radiance_queue.popleft()

            this_run_data.radiance = radiances

            data.append(this_run_data)

    return data


def extract_downward_radiances(clone_config_name):
    output_folder = clone_config_name + "Output"
    radiance_file = output_folder + "/cosine_irradiance_total_downward.txt"

    my_rad_file = open('my_radiances.txt', 'w')

    cosine_irradiances_total_downward_list = []

    with open(radiance_file, 'r') as f:
        next(f) # Skip first line, which indicates how many runs were done

        i = 2

        for line in f:
            if i % 6 == 1:
                my_rad = line.split()

                cosine_irradiances_total_downward_this_run = np.array([])

                for rad in my_rad:
                    my_rad_file.write(rad + " ")
                    cosine_irradiances_total_downward_this_run = np.append(cosine_irradiances_total_downward_this_run, float(rad))

                cosine_irradiances_total_downward_list.append(cosine_irradiances_total_downward_this_run)

                my_rad_file.write("\n")
                my_rad_file.flush()

            i = i + 1

    my_rad_file.close()

    cosine_irradiances_total_downward = np.asarray(cosine_irradiances_total_downward_list)

    return cosine_irradiances_total_downward


def copy_input_config_files(clone_config_name, output_folder):
    # Copy input config files to output folder so that there is a record of which inputs were used for this set of output files
    copy_config_file_command = "cp " + clone_config_name + " " + output_folder
    os.system(copy_config_file_command)

    copy_config_file_command = "cp -r " + clone_config_name + "Materials " + output_folder
    os.system(copy_config_file_command)


def run_accurt(clone_config_name):
    output_folder = clone_config_name + "Output"

    cmd = "AccuRT " + clone_config_name + " | tee " + output_folder + "/AccuRT_terminal_output.txt"
        
    print("running cmd =", cmd)

    #this is where accurt is ran
    os.system(cmd)

    copy_input_config_files(clone_config_name, output_folder)


def print_tags(dict):
    if 'name' in dict:
        config_file_name = dict['name']
    else:
        config_file_name = 'Anonymous'

    print('\n\nValues Specified for ' + config_file_name + ' Config File')
    print('------------------------')
    for key, value in dict.items():
        
        print(key + " = " + value)
    print('------------------------\n')


def print_updated_tags(list_of_tag_dicts):
    for dict in list_of_tag_dicts:
        print_tags(dict)


def open_repeated_run_text_file(repeated_run_text_file_name, template_config_name, config_file_type):
    path_to_text_file = ""

    if (config_file_type == ConfigFileType.MAIN):
        path_to_text_file = ""
    elif (config_file_type == ConfigFileType.MATERIAL):
        path_to_text_file = template_config_name + 'Materials/'

    open_repeated_run_text_file_handle = open(path_to_text_file + repeated_run_text_file_name, 'w')

    return open_repeated_run_text_file_handle