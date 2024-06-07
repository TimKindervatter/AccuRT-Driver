class ConfigFile:
    def __init__(self, template_config_name, clone_config_name) -> None:
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
    def __init__(self, template_config_name, clone_config_name) -> None:
        ConfigFile.__init__(self, template_config_name, clone_config_name)


class MaterialConfigFile(ConfigFile):
    def __init__(self, template_config_name, clone_config_name, material_enum) -> None:
            ConfigFile.__init__(self, template_config_name, clone_config_name)
            self.material_enum = material_enum

            self.template_name = self.template_name + "Materials/" + self.material_enum.value
            self.clone_name    = self.clone_name + "Materials/" + self.material_enum.value