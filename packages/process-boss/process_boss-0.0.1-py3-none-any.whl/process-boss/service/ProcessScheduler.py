import json
import sys
import time
import os
import pytz
import logging
from subprocess import Popen, PIPE, STDOUT
from croniter import croniter
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from ..util.ConfigHandler import ConfigHandler 
from ..util.LogHandler import LogHandler 
from ..domain.State import State

class ProcessScheduler:

    def __init__(self, configPath):
        logging.debug(f"configPath={configPath}")

        self.configPath = configPath
        self.startupDatetime = datetime.now(pytz.timezone('Europe/London'))
        self.configHandler = ConfigHandler()
        self.logHandler = LogHandler()
        self.state = State()

    def loop(self):
        while(True):
            logging.info("Starting new loop")
            logging.debug(self.state)

            config = self.configHandler.read(self.configPath)
            self.runAll(config)
            self.wait(config.loopRefreshSeconds)
            
    def runAll(self, config):
        logging.debug(f"config={config}")

        with ThreadPoolExecutor (max_workers=config.maxWorkers) as executor:
            for processConfig in config.processesConfig.processList:
                slog = self.logHandler.createSchedulerLogger (processConfig, config.schedulerLogDir) 
                slog.info(f"[{processConfig.id}] processConfig={processConfig}")

                processRegistered = self.state.get(processConfig.id) != False
                processFinished = processRegistered and self.state.get(processConfig.id).future.done()
                slog.debug(f"[{processConfig.id}] processRegistered={processRegistered}, processFinished={processFinished}")

                if processRegistered:
                    if not processFinished:
                        slog.info(f"[{processConfig.id}] Process is still running. Skipping...")
                        continue
                    else:
                        nextRunBaseDate = self.state.get(processConfig.id).startDatetime 
                        slog.info(f"[{processConfig.id}] Process ran before: {nextRunBaseDate}")
                else:
                    nextRunBaseDate = self.startupDatetime
                    slog.info(f"[{processConfig.id}] Process has not run before")

                slog.debug(f"[{processConfig.id}] nextRunBaseDate={nextRunBaseDate}")

                nextRunTimestamp = croniter (processConfig.cron, nextRunBaseDate).get_next() 
                nowDatetime = datetime.now(pytz.timezone('Europe/London'))
                nowTimestamp = nowDatetime.timestamp()
                scheduledToRun = nextRunTimestamp < nowTimestamp
                slog.debug(f"[{processConfig.id}] scheduledToRun={scheduledToRun}, processConfig.runAtStartup={processConfig.runAtStartup}")

                if (scheduledToRun or (not processRegistered and processConfig.runAtStartup)):
                    slog.info(f"[{processConfig.id}] Process is scheduled to run NOW: {datetime.fromtimestamp (nowTimestamp)}")
                    self.state.set( processConfig, nowDatetime, executor.submit(self.run, processConfig, config.processLogDir, nowDatetime) )
                else:
                    slog.info(f"[{processConfig.id}] Process is scheduled to run on: {datetime.fromtimestamp (nextRunTimestamp)}")

    def run(self, processConfig, processLogDir, nowDatetime):
        plog = self.logHandler.createProcessLogger(processConfig, processLogDir, nowDatetime)
        plog.debug(f"processConfig={processConfig}, processLogDir={processLogDir}, nowDatetime={nowDatetime}")

        with Popen(
            processConfig.command,
            stdout=PIPE,
            stderr=STDOUT
        ) as p:
            for line in iter (p.stdout.readline, b""):
                plog.info(f"[{processConfig.id}] ... {line.decode(sys.stdout.encoding).rstrip()}")

    def wait(self, loopRefreshSeconds):
        logging.info(f"Waiting for: {loopRefreshSeconds} seconds")

        time.sleep(loopRefreshSeconds)
