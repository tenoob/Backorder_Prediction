from application.logger import logging
from application.exception import BackorderException
from application.entity.artifact_entity import DataIngestionArtifact
from application.entity.config_entity import DataIngestionConfig
import os,sys
from six.moves import urllib
#import urllib.request
from shutil import copy
import pandas as pd
import patoolib
from pyunpack import Archive





class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig) -> None:
        try:
            logging.info(f"\n{'>'*20} Data Ingestion Log Started. {'<'*20}")
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

            logging.info(f'File: [ {tgz_file_path} ] has been Downloaded Successfully')
            return tgz_file_path
        except Exception as e:
            raise BackorderException(e,sys) from e

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting: [ {tgz_file_path} ] into Directory: [ {raw_data_dir} ]")
            """with tarfile.open(tgz_file_path) as raw_tgz_file_obj:
                raw_tgz_file_obj.extractall(path=raw_data_dir)"""

            #rar_file_name = os.path.basename(tgz_file_path)
            #patoolib.extract_archive(tgz_file_path,outdir=raw_data_dir)
            Archive(tgz_file_path).extractall(raw_data_dir)
            logging.info("Extraction Successfull.")
        except Exception as e:
            raise BackorderException(e,sys) from e

    def saving_data_into_ingested(self):
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            train_file_path = None
            test_file_path = None

            for filename in os.listdir(raw_data_dir):

                src_file = os.path.join(raw_data_dir,filename)

                if filename == self.data_ingestion_config.train_file_name:

                    dest_file = self.data_ingestion_config.ingested_train_dir
                    os.makedirs(dest_file,exist_ok=True)
                    
                    copy(src_file,dest_file)

                    train_file_path = os.path.join(dest_file,filename)
                    logging.info(f"Exported Training file into file: [ {dest_file} ]")

                elif filename == self.data_ingestion_config.test_file_name:
                    dest_file = self.data_ingestion_config.ingested_test_dir
                    os.makedirs(dest_file,exist_ok=True)
                    
                    copy(src_file,dest_file)
                    test_file_path = os.path.join(dest_file,filename)
                    logging.info(f"Exported Testing file into file: [ {dest_file} ]")

                else:
                    logging.info(f" [ {filename} is Not Utilized")

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message="Data Ingestion Artifact has been created with 2 sepate files for train and test")

            logging.info(f"Data Ingestion Artifact: [ {data_ingestion_artifact} ]")
            return data_ingestion_artifact

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            #print(tgz_file_path)

            return self.saving_data_into_ingested()

        except Exception as e:
            raise BackorderException(e,sys) from e
            

    def __del__(self):
        logging.info(f"\n{'>'*20} Data Ingestion Log Completed. {'<'*20}\n")

