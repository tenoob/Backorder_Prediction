
from application.constant import *
from application.logger import logging
from application.exception import BackorderException
from application.entity.config_entity import DataIngestionConfig, DataValidationConfig, TrainingPipelineCongif , DataTransformationConfig , ModelTrainerConfig , ModelEvaluationConfig
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


    def get_data_validation_cofig(self) -> DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir = os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR_NAME,
                self.current_time_stamp)

            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(
                ROOT_DIR,
                data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],
                data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            report_file_path = os.path.join(
                data_validation_artifact_dir,
                data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME])

            report_page_file_path = os.path.join(
                data_validation_artifact_dir,
                data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path)

            logging.info(f"Data Validation Config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            raise BackorderException(e,sys) from e


    def get_data_transfomation_config(self) -> DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_transformation_artifact_dir = os.path.join(
                artifact_dir,
                DATA_TRANSFORMATION_ARTIFACT_DIR,
                self.current_time_stamp)

            data_transformation_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            preprocesses_object_file_path = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME])

            transformed_train_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                data_transformation_config_info[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY])

            transformed_test_dir = os.path.join(
                data_transformation_artifact_dir,
                data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                data_transformation_config_info[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY]
            )

            data_transformation_config = DataTransformationConfig(
                preprocessed_object_file_path=preprocesses_object_file_path,
                transformed_test_dir=transformed_test_dir,
                transformed_train_dir=transformed_train_dir,
                
            )

            logging.info(f"Data Transformation Config: {data_transformation_config}")

            return data_transformation_config
        except Exception as e:
            raise BackorderException(e,sys) from e

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            atrifact_dir = self.training_pipeline_config.artifact_dir

            model_trainer_artifact_dir = os.path.join(
                atrifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR,
                self.current_time_stamp
            )

            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]

            trained_model_file_path = os.path.join(
                model_trainer_artifact_dir,
                model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
                model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY]
            )

            model_config_file_path = os.path.join(
                model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
                model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY]
            )

            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path=trained_model_file_path,
                model_config_file_path=model_config_file_path,
                base_accuracy=base_accuracy
            )

            logging.info(f"Model Trainer Config: {model_trainer_config}")

            return model_trainer_config
        except Exception as e:
            raise BackorderException(e,sys) from e


    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        try:
            model_evaluation_config = self.config_info[MODEL_EVALUATION_CONFIG_KEY]

            artifact_dir = os.path.join(
                self.training_pipeline_config.artifact_dir,
                MODEL_EVALUATION_ARTIFACT_KEY)

            model_evaluation_file_path = os.path.join(
                artifact_dir,
                model_evaluation_config[MODEL_EVALUATION_FILE_NAME_KEY])

            model_evaluation_config = ModelEvaluationConfig(
                model_evaluation_file_path=model_evaluation_file_path,
                time_stamp=self.current_time_stamp)

            logging.info(f"Model Evaluation Config: {model_evaluation_config}")
            return model_evaluation_config
        except Exception as e:
            raise BackorderException(e,sys) from e
    