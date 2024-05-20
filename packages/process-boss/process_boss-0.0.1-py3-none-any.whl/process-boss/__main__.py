import sys
import logging

from .service.ProcessScheduler import ProcessScheduler
from .util.LogHandler import LogHandler

def main(configPath):
    logging.basicConfig(level=LogHandler.LEVEL, format=LogHandler.FORMAT)
    ProcessScheduler(configPath).loop()

if __name__ == '__main__':
    main(sys.argv[1])
