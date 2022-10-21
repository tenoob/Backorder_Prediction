from distutils.log import INFO
import imp
import logging
import os
from application.constant import LOG_DIR,CURRENT_TIME_STAMP

LOG_FILE_NAME = f'log_{CURRENT_TIME_STAMP}.log'

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format='[%(asctime)s] ^; %(levelname)s ^; %(lineno)s ^; %(filename)s ^; %(funcName)s() ^; %(message)s',
    level=logging.INFO )
 
