from application.constant import COLUMNS_TO_USE_KEY, SCHEMA_FILE_PATH ,DATASET_SCHEMA_COLUMNS_KEY , DATASET_RAW_INPUT_COLUMNS
from application.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from application.entity.config_entity import DataValidationConfig
from application.logger import logging
from application.exception import BackorderException
import os,sys
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json
import pandas as pd

from application.util.utililty import read_yaml_file

class DataValidation:

    def __init__(self,data_validation_config: DataValidationConfig,
                    data_ingestion_artifact: DataIngestionArtifact) -> None:
        try:
            logging.info(f"\n{'>'*20} Data Validation Log Started. {'<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise BackorderException(e,sys) from e

    def is_train_test_file_exists(self) -> bool:
        try:
            logging.info(f"Checking Storage for Training and Testing files")

            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist

            logging.info(f"Training and Testing files found in Storage ? -> {is_available}")

            if not is_available:
                message = f"""Training file: [ {train_file_path} ] or
                Testing file: [ {test_file_path} ] is NOT PRESENT"""

                raise Exception(message)

            return is_available
        except Exception as e:
            raise BackorderException(e,sys) from e

    def check_dtype(self,df_col,schema_col) -> bool:
        try:
            if df_col != schema_col:
                return False
        except Exception as e:
            raise BackorderException(e,sys)
    
    def check_columns(self,df,schema) -> bool:
        try:
            column_present = True
            dtype_check = True
            cols = schema[COLUMNS_TO_USE_KEY]

            for col in cols:
                if col in df.columns:
                    logging.info(f"\N{check mark} [ {col} ] is present in Dataset ")
                    dtype = self.check_dtype(
                                    df_col=df[col].dtype,
                                    schema_col= schema[DATASET_RAW_INPUT_COLUMNS][col])
                    
                    if dtype is False:
                        dtype_check=False
                        logging.info(f'[ {col} ] should be {schema[DATASET_RAW_INPUT_COLUMNS][col]} but is {df[col].dtype}')
                    else:
                        logging.info(f'[ {col} ] Datatype is correct')

                else:
                    logging.info(f"\N{cross mark} [ {col} ] is not present in Dataset ")
                    column_present = False
            
            # return true if both column_present and dtype_check are true
            if column_present and dtype_check:
                return True

            return False 
        except Exception as e:
            raise BackorderException(e,sys)
    
    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False

            #Work in progress
            schema_file = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path,nrows=1000)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path,nrows=1000)

            #checking for column in train_df
            check_train = self.check_columns(df=train_df,schema=schema_file)
            check_test = self.check_columns(df=test_df,schema=schema_file)


            if check_train and check_test:
                validation_status = True

            return validation_status
        except Exception as e:
            raise BackorderException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            schema_file = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path,usecols=schema_file[COLUMNS_TO_USE_KEY])
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path,usecols=schema_file[COLUMNS_TO_USE_KEY])

            return train_df,test_df
        except Exception as e:
            raise BackorderException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            logging.info("started get_and_save_data_drift_report")

            profile = Profile(sections=[DataDriftProfileSection()])

            logging.info("before train test")

            train_df,test_df = self.get_train_and_test_df()

            logging.info("before cal test")

            profile.calculate(train_df,test_df)

            logging.info("before cal test")

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path

            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)

            logging.info(f"Report saved as Json at: [ {report_file_path} ]")
            return report
        except Exception as e:
            raise BackorderException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            logging.info("started save_data_drift_report_page")

            dashboard = Dashboard(tabs=[DataDriftTab()])

            logging.info("before train test")

            train_df,test_df = self.get_train_and_test_df()
            logging.info("before cal")

            dashboard.calculate(train_df,test_df)

            logging.info("after cal")

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
            logging.info(f"Report page saved at: [ {report_page_file_path} ]")
        except Exception as e:
            raise BackorderException(e,sys) from e

    def is_data_drift_found(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report()

            self.save_data_drift_report_page()
            return True

        except Exception as e:
            raise BackorderException(e,sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            logging.info("started validate")
            self.validate_dataset_schema()
            logging.info("started is_data_drift_found")

            self.is_data_drift_found()
            
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed Successfully")
            
            
            return data_validation_artifact
        except Exception as e:
            raise BackorderException(e,sys) from e


    def __del__(self):
        logging.info(f"\n{'>'*20} Data Validation Log Completed. {'<'*20}\n")
