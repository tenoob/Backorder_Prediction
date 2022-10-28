from application.constant import *
from application.logger import logging
from application.exception import BackorderException
from application.entity.config_entity import DataIngestionConfig, TrainingPipelineCongif
from application.entity.artifact_entity import DataIngestionArtifact
from application.util.utililty import read_yaml_file
from urllib import response
import os,sys

class Configration:
    def __init__(self,config_file_path:str=CONFIGRATION_FILE_PATH,
                 current_time_stamp:str=CURRENT_TIME_STAMP) -> None:
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.current_time_stamp = current_time_stamp
        except Exception as e:
            raise BackorderException(e,sys) from e

    def get_training_pipeline_config(self) -> TrainingPipelineCongif:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(
                ROOT_DIR,
                training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])


            training_pipeline_config = TrainingPipelineCongif(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise BackorderException(e,sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
                                                        DATA_INGESTION_ARTIFACT_DIR,
                                                        self.current_time_stamp)

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY]
            
            tgz_download_url = os.path.join(data_ingestion_artifact_dir,
                                    data_ingestion_info[DATA_INTESTION_TGZ_DOWNLOAD_KEY])

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                                    data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_INGESTED_DIR_KEY])

            ingested_train_dir = os.path.join(ingested_data_dir,
                                        data_ingestion_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY])

            ingested_test_dir = os.path.join(ingested_data_dir,
                                        data_ingestion_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY])

            train_file_name = data_ingestion_info[DATA_INGESTION_TRAIN_FILE_NAME_KEY]

            test_file_name = data_ingestion_info[DATA_INGESTION_TEST_FILE_NAME_KEY]

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                tgz_download_dir=tgz_download_url,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir,
                train_file_name=train_file_name,
                test_file_name=test_file_name
            )

            logging.info(f"Data Ingestion Config: {data_ingestion_config}")
            return data_ingestion_config

        except Exception as e:
            raise BackorderException(e,sys) from e
    