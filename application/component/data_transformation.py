from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from application.constant import CATEGORICAL_COLUMN_KEY, NUMERICAL_COLUMN_KEY , ACCEPTED_VAIRENCE_KEY
from application.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact 
from application.entity.config_entity import DataTransformationConfig
from application.util.utililty import *
from application.entity.model_factory import ModelFactory
from application.util.col_dim_reduction import CustomTransformer
from application.logger import logging
from application.exception import BackorderException
from imblearn.combine import SMOTETomek,SMOTEENN
from collections import Counter
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
            target_column_name = dataset_schema[TARGET_COLUMN_KEY]

            accepted_componets = dataset_schema[ACCEPTED_VAIRENCE_KEY]
            logging.info(f"Accepted Varience: {accepted_componets}")
            
            numerical_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy='median')),
                ('scaler',StandardScaler()),
                ])

            #accepted_componets=accepted_componets*100

            categorical_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False)),
                ])

            target_pipeline = Pipeline(steps=[
                ('one_hot_encoder',OneHotEncoder())
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            separete_preprocess = ColumnTransformer(
                transformers=[
                ('numerical_pipeline',numerical_pipeline,numerical_columns),
                ('categorical_pipeline',categorical_pipeline,categorical_columns)
            ])


            preprocess = Pipeline([
                ("part1",separete_preprocess),
                ('pca',PCA(n_components=accepted_componets)),
            ])

            return preprocess
        except Exception as e:
            raise BackorderException(e,sys) from e

    def dataset_scaling(self,x,y) -> pd.DataFrame:
        try:
            logging.info(f"Original Dataset shape: {x.shape} \n Targer values: {y.shape}")


            schema = read_yaml_file(file_path=self.data_validation_artifact.schema_file_path)
            numerical_columns = schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = schema[CATEGORICAL_COLUMN_KEY]

            #reading the model.yaml file for dataset_balancing
            model_file = read_yaml_file(MODEL_FILE_PATH)
            balancer = model_file[DATASET_BALANCING_KEY]
            class_name = balancer[CLASS_KEY]
            modeule_name = balancer[MODULE_KEY]
            params = balancer[PARAM_KEY]


            obj = ModelFactory.class_for_name(module_name=modeule_name,class_name=class_name)

            model = obj()

            model = ModelFactory.update_propery_of_class(model,params)

            X_res ,y_res = model.fit_resample(x,y)


            logging.info(f"Reshaped Dataset shape:{x.shape} \n Targer values: {y_res.value_counts()}")
            return X_res,y_res
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

            train_df = load_data(file_path=train_file_path,
                                schema_file_path=schema_file_path)

            test_df = load_data(file_path=test_file_path,
                                schema_file_path=schema_file_path)
            
            schema = read_yaml_file(schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]
            

            #droping rows with Nan in target column
            logging.info(f"Droping Rows with Target Column as Nan")
            train_df = train_df[train_df[target_column_name].notna()]
            logging.info(f"Training File shape: {train_df.shape}")
            test_df = test_df[test_df[target_column_name].notna()]
            logging.info(f"Training File shape: {test_df.shape}")


            logging.info(f"Splitting Data into Input and Target feature for Trainng and Testing Dataframes.")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = pd.get_dummies(train_df[target_column_name],drop_first=True)
            logging.info(f"Data type of Training Target column: {target_feature_train_df.dtypes}")
            target_feature_train_df.astype(int)
            logging.info(f"Data type of Training Target column changed to: {target_feature_train_df.dtypes}")

            #train_df[[target_column_name]]

            #Dataset Balancing
            input_feature_train_df,target_feature_train_df = self.dataset_scaling(
                                                                x=input_feature_train_df,
                                                                y=target_feature_train_df,
                                                                )

            
            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = pd.get_dummies(test_df[target_column_name],drop_first=True)
            logging.info(f"Data type of Testing Target column: {target_feature_test_df.dtypes}")
            target_feature_test_df.astype(int)
            logging.info(f"Data type of Testing Target column: {target_feature_test_df.dtypes}")


            logging.info(f"Training Dataframe Columns: {input_feature_train_df.columns}")
            logging.info(f"Testing Dataframe Columns: {input_feature_test_df.columns}")


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
                transformed_train_file_path=transformed_train_file_path,
                preprocessed_object_file_path=preprocessing_obj_file_path
            )

            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            return data_transformation_artifact    
        except Exception as e:
            raise BackorderException(e,sys) from e


    def __del__(self):
        logging.info(f"\n{'>'*20} Data Transformation Log Completed. {'<'*20}\n")
