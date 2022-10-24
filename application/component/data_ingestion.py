from application.logging import logging
from application.exception import BackorderException
from application.entity.artifact_entity import DataIngestionArtifact
from application.entity.config_entity import DataIngestionConfig
import os,sys
from six.moves import urllib



class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig) -> None:
        try:
            logging.info(f"{'>'*20} Data Ingestion Log Started. {'<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise BackorderException(e,sys) from e

    def download_data(self) -> str:
        try:
            #extracting url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #save location of the downloaded .rar file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            os.makedirs(tgz_download_dir,exist_ok=True)

            dataset_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir,dataset_file_name)

            logging.info(f"Downloading File from: [ {download_url} ] into: [ {tgz_file_path} ]")
            urllib.request.urlretrieve(download_url,tgz_file_path)
            logging.info(f'File: [ {tgz_file_path} has been Downloaded Successfully]')
            return tgz_file_path
        except Exception as e:
            raise BackorderException(e,sys) from e


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_data()
            print(tgz_file_path)
        except Exception as e:
            raise BackorderException(e,sys) from e
