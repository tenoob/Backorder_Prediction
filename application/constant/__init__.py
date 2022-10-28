from datetime import datetime
import os

ROOT_DIR = os.getcwd()

LOG_DIR = 'logs'
CURRENT_TIME_STAMP = f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}'

CONFIGRATION_DIR = 'ConfigrationFiles'
CONFIGRATION_FILE_NAME = 'configration.yaml'
CONFIGRATION_FILE_PATH = os.path.join(
    ROOT_DIR,
    CONFIGRATION_DIR,
    CONFIGRATION_FILE_NAME)

#Training pipeline related variable
TRAINING_PIPELINE_CONFIG_KEY = 'training_pipeline_config'
TRAINING_PIPELINE_NAME_KEY = 'pipeline_name'
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = 'artifact_dir'

#Data Ingestion related variable
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion'
DATA_INGESTION_RAW_DATA_DIR_KEY = 'raw_data_dir'
DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY = 'dataset_download_url'
DATA_INTESTION_TGZ_DOWNLOAD_KEY = 'tgz_download_dir'
DATA_INGESTION_INGESTED_DIR_KEY = 'ingested_dir'
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY = 'ingested_train_dir'
DATA_INGESTION_INGESTED_TEST_DIR_KEY = 'ingested_test_dir'
DATA_INGESTION_TRAIN_FILE_NAME_KEY = 'train_file_name'
DATA_INGESTION_TEST_FILE_NAME_KEY = 'test_file_name'


#Data Validation related variable
DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = 'schema_file_name'
DATA_VALIDATION_SCHEMA_DIR_KEY = 'schema_dir'
DATA_VALIDATION_REPORT_FILE_NAME = 'report_file_name'
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = 'report_page_file_name'
DATA_VALIDATION_ARTIFACT_DIR_NAME = 'data_validation'

#schema.yaml related variable
DATASET_SCHEMA_COLUMNS_KEY = 'columns'
NUMERICAL_COLUMN_KEY = 'numerical_columns'
CATEGORICAL_COLUMN_KEY = 'categorical_columns'
TARGET_COLUMN_KEY = 'target_column'