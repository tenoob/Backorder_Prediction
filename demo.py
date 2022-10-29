
from application.logger import logging
from application.component.data_ingestion import DataIngestion
from application.exception import BackorderException
from application.config.configration import Configration
import os,sys

from application.pipeline.pipeline import Pipeline


def main():
    try:
        #config = Configration()
        """data_ingestion_config = Configration().get_data_ingestion_config()
        print(data_ingestion_config)"""

        """"data_ingestion = DataIngestion(data_ingestion_config=Configration().get_data_ingestion_config())
        data_ingestion.initiate_data_ingestion()"""

        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=='__main__':
    main()