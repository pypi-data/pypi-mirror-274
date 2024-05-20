import logging

from .FileHandler import FileHandler
from ..domain.Config import Config

class ConfigHandler:
    
    def __init__(self):
        self.fileHandler = FileHandler()

    def read(self, fileNameOrPath):
        logging.debug(f"fileNameOrPath={fileNameOrPath}")

        yamlConfig = self.fileHandler.readConfig(fileNameOrPath) 
        logging.debug(f"YAML config: {yamlConfig}")

        config = Config(yamlConfig)
        logging.debug("Config created: {config}")

        return config
