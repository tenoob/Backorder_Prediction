from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from application.constant import CATEGORICAL_COLUMN_KEY, DATA_TRANSFORMATION_ACCEPTED_VAIRENCE_KEY, NUMERICAL_COLUMN_KEY
from application.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact 
from application.entity.config_entity import DataTransformationConfig
from application.util.utililty import *
from application.logger import logging
from application.exception import BackorderException
import os,sys
import numpy as np


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

            logging.info(f"Loading Training and Testing Data as DataFrame.")

            train_df= load_data(file_path=train_file_path,
                                schema_file_path=schema_file_path)

            test_df = load_data(file_path=test_file_path,
                                schema_file_path=schema_file_path)
            
            schema = read_yaml_file(schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]

            logging.info(f"Splitting Data into Input and Target feature for Trainng and Testing Dataframes.")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[[target_column_name]]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[[target_column_name]]

            logging.info(f"Applying Pre-Processing object on Training Dataframes.")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            logging.info(f"Applying Pre-Processing object on Testing Dataframe")
            input_frature_test_arr =preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_frature_test_arr,np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir,
                                                train_file_name)

            transformed_test_file_path = os.path.join(transformed_test_dir,
                                                test_file_name)

            logging.info(f"Saving Transformed Training Array.")
            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info(f"Saving Pre-Processing Object.")
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(
                is_transformed=True,
                message="Data Transformation Successfull.",
                transformed_test_file_path=transformed_test_file_path,
                transformed_train_file_path=transformed_test_file_path,
                preprocessed_object_file_path=preprocessing_obj_file_path
            )

            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact    
        except Exception as e:
            raise BackorderException(e,sys) from e