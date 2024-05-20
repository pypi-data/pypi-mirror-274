import json

class State:

    def __init__(self):
        self.processIdToProcessStateDict = {}

    def get(self, processId):
        if not processId in self.processIdToProcessStateDict: 
            return False
        
        return self.processIdToProcessStateDict[ processId ]

    def set(self, processConfig, startDatetime, future): 
        self.processIdToProcessStateDict[ processConfig.id ] = ProcessState(
            processConfig, startDatetime, future
        )

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'State': {p : self.processIdToProcessStateDict[p].toDict() for p in self.processIdToProcessStateDict}
        }


class ProcessState:

    def __init__(self, processConfig, startDatetime, future):
        self.processConfig = processConfig
        self.startDatetime = startDatetime
        self.future = future

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'ProcessConfig': self.processConfig.toDict(), 
            'startDatetime': str(self.startDatetime),
            'future': str(self.future),
        }
