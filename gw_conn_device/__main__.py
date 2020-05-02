# coding=utf-8
# python 3.6

import sys
import os
import time
import platform
import setproctitle
import logging
from logging import handlers
import threading
import requests
import json
from ast import literal_eval
from flask import Flask, jsonify, redirect, url_for, request

import data_model
from config import DEVICE_CONFIG

import history_db

from const import(
    SAMIN747_RETRY_COUNT,
    REQUIRED_PYTHON_VER,
    CONTROL_SUCCESS_CODE,
    CONTROL_FAIL_CODE
)


app = Flask(__name__)

LOG_FILENAME = "gw_log.log"

fmt = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
logFormatter = logging.Formatter(fmt)

fileLogHandler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when='midnight', interval=1, backupCount=0, encoding='utf-8', delay=False, utc=False, atTime=None)
fileLogHandler.setFormatter(logFormatter)
fileLogHandler.setLevel(logging.DEBUG)
fileLogHandler.suffix = "%Y%m%d_%H%M%S"

stmLogHandler = logging.StreamHandler()
stmLogHandler.setLevel(logging.DEBUG)
stmLogHandler.setFormatter(logFormatter)
   
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.addHandler(fileLogHandler)
_LOGGER.addHandler(stmLogHandler)

def dcStatusThread():
    try:
        res = requests.get('http://localhost:8080/dc_check', timeout=5)

    except requests.ConnectionError as msg :
        _LOGGER.error("dc_check connect Fail")

    except Exception as e :
        _LOGGER.error(e)

    task = threading.Timer(DEVICE_CONFIG['polling_time'], dcStatusThread)
    task.setDaemon(True)
    task.start()

def validate_python() -> None:
    """Validate that the right Python version is running."""
    if sys.version_info[:3] < REQUIRED_PYTHON_VER:
        print(
            "Home Assistant requires at least Python {}.{}.{}".format(
                *REQUIRED_PYTHON_VER
            )
        )
        sys.exit(1)
    
def main() -> int:
    validate_python()

    if os.name == 'posix' : #Linux
        setproctitle.setproctitle('gw_conn_device')

    env = sys.argv[1] if len(sys.argv) >= 2 else 'prod'

    if env == 'prod':
        #Todo/Logging system 셋팅
        pass
    elif env == 'test':
        #Todo/Logging system 셋팅
        pass
    elif env == 'dev':
        #Todo/Logging system 셋팅
        pass

    try:
        _LOGGER.info("===== Start Server =====")
        #dcStatusThread()
        app.run(host="localhost", port="8080")
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e :
        print(e)
        sys.exit(0)

if __name__ == '__main__':

    sys.exit(main())