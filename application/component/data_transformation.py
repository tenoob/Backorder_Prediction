from signal import raise_signal
from tempfile import TemporaryFile
from tkinter import E
from token import EXACT_TOKEN_TYPES

from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from application.constant import CATEGORICAL_COLUMN_KEY, DATA_TRANSFORMATION_ACCEPTED_VAIRENCE_KEY, NUMERICAL_COLUMN_KEY
from application.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact 
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

            accepted_componets = self.data_transformation_config[DATA_TRANSFORMATION_ACCEPTED_VAIRENCE_KEY]
            
            numerical_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='median')),
                ('scaler',StandardScaler()),
                ('pca',PCA(n_components=accepted_componets))
            ])

            categorical_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False)),
                ('pca',PCA(n_components=accepted_componets))
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocess = ColumnTransformer([
                ('numerical_pipeline',numerical_pipeline,numerical_columns),
                ('categorical_pipeline',categorical_pipeline,categorical_columns)
            ])

            return preprocess
        except Exception as e:
            raise BackorderException(e,sys) from e


    def initate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"Obtaining Pre-Processing Object.")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info(f"Obtaining Training and Testing file path")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            
        except Exception as e:
            raise BackorderException(e,sys) from e