from datetime import datetime
import os

ROOT_DIR = os.getcwd()

LOG_DIR = 'logs'
CURRENT_TIME_STAMP = f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'

CONFIGRATION_DIR = 'ConfigrationFiles'
CONFIGRATION_FILE_NAME = 'configration.yaml'
CONFIGRATION_FILE_PATH = os.path.join(
    ROOT_DIR,
    CONFIGRATION_DIR,
    CONFIGRATION_FILE_NAME)

#Training pipeline related variable
TRAINING_PIPELINE_CONFIG_KEY = 'training_'
