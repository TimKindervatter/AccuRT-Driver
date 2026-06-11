from MaterialEnum import Material
from utils import clone

class ConfigFile:
    def __init__(self, template_config_name, clone_config_name):
        self.template_name = template_config_name
        self.clone_name = clone_config_name
        self.template_file_handle = None
        self.clone_file_handle = None

    def __del__(self):
        if self.template_file_handle is not None and not self.template_file_handle.closed:
            self.template_file_handle.close()

        if self.clone_file_handle is not None and not self.clone_file_handle.closed:
            self.clone_file_handle.close()


    def openTemplateForReading(self):
        self.template_file_handle = open(self.template_name, 'r')


    def openCloneForWriting(self):
        self.clone_file_handle = open(self.clone_name, 'w')


    def updateTags(self, dict):
        if self.template_file_handle is None or self.template_file_handle.closed:
            self.openTemplateForReading()

        if self.clone_file_handle is None or self.clone_file_handle.closed:
            self.openCloneForWriting()

        lines = []

        for line in self.template_file_handle:
            keep_original_line = True
            tag_found = False

            if line.strip() and line.strip()[0] != '#':
                lines.append(line)
                continue
            else:
                if not lines:
                    self.clone_file_handle.write(line)
                    self.clone_file_handle.flush()
                    continue

                for tag, value in dict.items():
                    for elem in lines:
                        tokens = elem.split()
                        if tag in tokens:
                            tag_found = True
                            string_to_write = tag + " = " + value + "#\n"
                            self.clone_file_handle.write(string_to_write)
                            self.clone_file_handle.flush()
                            keep_original_line = False

                if keep_original_line:   
                    for old_line in lines: 
                        self.clone_file_handle.write(old_line)
                        self.clone_file_handle.flush()

                lines.clear()

                self.clone_file_handle.write(line)
                self.clone_file_handle.flush()

    

class MainConfigFile(ConfigFile):
    def __init__(self, template_config_name, clone_config_name):
        ConfigFile.__init__(self, template_config_name, clone_config_name)


class MaterialConfigFile(ConfigFile):
    def __init__(self, template_config_name, clone_config_name, material_type):
            ConfigFile.__init__(self, template_config_name, clone_config_name)
            self.material_type = material_type

            self.template_name = self.template_name + "Materials/" + self.material_type.value
            self.clone_name    = self.clone_name + "Materials/" + self.material_type.value


class ConfigFileCopier:
    def __init__(self, template_config_name, clone_name_suffix=""):
        self.template_config_name = template_config_name
        self.clone_config_name = clone(template_config_name, clone_name_suffix)


    def updateMainConfigTags(self, config_tags):
        config_file = MainConfigFile(self.template_config_name, self.clone_config_name)
        config_file.updateTags(config_tags)

    
    def updateMaterialConfigTags(self, config_tags, material_type):
        config_file = MaterialConfigFile(self.template_config_name, self.clone_config_name, material_type)
        config_file.updateTags(config_tags)


    def updateAerosolsConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.AEROSOLS)


    def updateBloodConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.BLOOD)


    def updateCloudConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.CLOUD)


    def updateEarthAtmosphericGasesConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.EARTH_ATMOSPHERIC_GASES)


    def updateFatConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.FAT)


    def updateIceConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.ICE)


    def updateIntralipidConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.INTRALIPID)


    def updateKeratinConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.KERATIN)


    def updateLayerUserSpecifiedConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.LAYER_USER_SPECIFIED)


    def updateLayerUserSpecifiedHGConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.LAYER_USER_SPECIFIED_HG)


    def updateMelanosomesConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.MELANOSOMES)


    def updatePureWaterConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.PURE_WATER)


    def updateSnowConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.SNOW)


    def updateTissueBaseConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.TISSUE_BASE)


    def updateUserSpecifiedConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.USER_SPECIFIED)


    def updateVacuumConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.VACUUM)


    def updateWaterImpurityCCRRConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.WATER_IMPURITY_CCRR)


    def updateWaterImpurityGSMConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.WATER_IMPURITY_GSM)


    def updateWaterParticlesConfigTags(self, config_tags):
        self.updateMaterialConfigTags(config_tags, Material.WATER_PARTICLES)