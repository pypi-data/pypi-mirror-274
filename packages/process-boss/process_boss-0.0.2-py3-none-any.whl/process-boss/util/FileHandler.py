import yaml
import os
import sys
from pathlib import Path
import logging

class FileHandler:

    def isFile(self, filePath):
        return Path(filePath).is_file()

    def readFile(self, filePath): 
        with open(filePath) as f: 
            return f.read()

    def readYaml(self, filePath):
        return yaml.safe_load(self.readFile(filePath))

    def readConfig(self, filePath):
        if not self.isFile(filePath):
            logging.error(f"Configuration file not found: \"{filePath}\"")
            sys.exit(1)
        
        return self.readYaml(filePath)
    
    def writeFile(self, filePath, content): 
        dirPath = os.path.dirname(filePath) 
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        
        with open(filePath, "w") as f: 
            f.write(content)
