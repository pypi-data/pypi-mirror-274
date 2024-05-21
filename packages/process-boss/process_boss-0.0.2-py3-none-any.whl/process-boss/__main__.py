import sys
import logging

from .service.ProcessScheduler import ProcessScheduler
from .util.LogHandler import LogHandler

def main():
    logging.basicConfig(level=LogHandler.LEVEL, format=LogHandler.FORMAT)

    if len(sys.argv) < 2:
        logging.error("Missing CLI argument: Configuration File Path")
        logging.error("")
        logging.error("USAGE:")
        logging.error("    $> python -m process-boss c:\\Users\\kristof\\config.yaml")
        logging.error("")
        sys.exit(1)
    
    configPath = sys.argv[1]
    logging.info(f"Using configuration file: \"{configPath}\"")

    ProcessScheduler(configPath).loop()

if __name__ == '__main__':
    main()
