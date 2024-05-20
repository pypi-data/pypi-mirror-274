import yaml
import json
import os
from pathlib import Path
import logging

class FileHandler:

    def getRootDir(self):
        thisFilePath = os.path.realpath(__file___) 
        libDir = os.path.dirname(thisFilePath)
        srcDir = os.path.dirname(libDir)
        rootDir = os.path.dirname(srcDir)
        return rootDir

    def isFile(self, filePath):
        return Path(filePath).is_file()

    def readFile(self, filePath): 
        with open(filePath) as f: 
            return f.read()

    # def readJson(self, filePath):
    #   return json.loads(self.readFile(filePath))

    def readYaml(self, filePath):
        return yaml.safe_load(self.readFile(filePath))

    def readConfig(self, fileNameOrPath):
        if not self.isFile(fileNameOrPath):
            fileNameOrPath = os.path.join(self.getRootDir(), fileNameOrPath)
        
        return self.readYaml(fileNameOrPath)
    
    def writeFile(self, filePath, content): 
        dirPath = os.path.dirname(filePath) 
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        
        with open(filePath, "w") as f: 
            f.write(content)
