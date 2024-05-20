import json
import shlex
import logging

class Config:

    def __init__(self, config):
        logging.debug(f"config={config}")

        self.loopRefreshSeconds = config['loopRefreshSeconds']
        self.maxWorkers = config['maxWorkers']
        self.schedulerLogDir = config['schedulerLogDir']
        self.processLogDir = config['processLogDir']
        self.processesConfig = ProcessesConfig(config['processes'])

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'Config': {
                'loopRefreshSeconds': self.loopRefreshSeconds, 
                'maxWorkers': self.maxWorkers,
                'schedulerLogDir': self.schedulerLogDir, 
                'processLogDir': self.processLogDir,
                **self.processesConfig.toDict()
            }
        }


class ProcessesConfig:

    def __init__(self, config):
        self.processList = []
        for c in config:
            self.processList.append( ProcessConfig(c))

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'ProcessesConfig': [t.toDict() for t in self.processList]
        }


class ProcessConfig:
    
    def __init__(self, config):
        self.id = config['id']
        self.cron = config['cron']
        self.command = config['command']
        self.runAtStartup = config['runAtStartup'] if 'runAtStartup' in config else False
        
    # def splitCommandToList(self, command):
    #   return shlex.split(command, posix=False) # False keeps quotes

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'ProcessConfig': {
                'id': self.id,
                'cron': self.cron,
                'command': self.command,
                'runAtStartup': self.runAtStartup
            }
        }
