from distutils.command.config import config
from application import logging
from application.component.data_ingestion import DataIngestion
from application.exception import BackorderException
from application.config.configration import Configration
import os,sys


def main():
    try:
        #config = Configration()
        """data_ingestion_config = Configration().get_data_ingestion_config()
        print(data_ingestion_config)"""

        data_ingestion = DataIngestion(data_ingestion_config=Configration().get_data_ingestion_config())
        data_ingestion.initiate_data_ingestion()
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=='__main__':
    main()