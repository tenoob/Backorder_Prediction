from application import logging
from application.exception import BackorderException
from application.config.configration import Configration
import os,sys


def main():
    try:
        data_ingestion_config = Configration().get_data_ingestion_config()
        print(data_ingestion_config)
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=='__main__':
    main()