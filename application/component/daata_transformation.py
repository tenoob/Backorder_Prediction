from signal import raise_signal
from tkinter import E

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from application.constant import CATEGORICAL_COLUMN_KEY, NUMERICAL_COLUMN_KEY
from application.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact 
from application.entity.config_entity import DataTransformationConfig
from application.util.utililty import read_yaml_file
from application.logger import logging
from application.exception import BackorderException
import os,sys


class DataTransformation:

    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                    data_validation_artifact: DataValidationArtifact,
                    data_transformation_config: DataTransformationConfig) -> None:
        try:                                        
            logging.info(f"\n{'>'*20} Data Transformation Log Started. {'<'*20}")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise BackorderException(e,sys) from e

    def get_data_transformer_object(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)
            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

            numerical_pipeline = Pipeline
        except Exception as e:
            raise BackorderException(e,sys) from e