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
SCHEMA_FILE_NAME = 'schema.yaml'
SCHEMA_FILE_PATH = os.path.join(
    ROOT_DIR,
    CONFIGRATION_DIR,
    SCHEMA_FILE_NAME)
    
DATASET_SCHEMA_COLUMNS_KEY = 'columns'
NUMERICAL_COLUMN_KEY = 'numerical_columns'
CATEGORICAL_COLUMN_KEY = 'categorical_columns'
TARGET_COLUMN_KEY = 'target_column'
COLUMNS_TO_USE_KEY = 'use_columns'
ACCEPTED_VAIRENCE_KEY = 'accepted_varience'



#Data Transformation related variable
DATA_TRANSFORMATION_CONFIG_KEY ='data_transformation_config'
DATA_TRANSFORMATION_ARTIFACT_DIR = 'data_transformation'
DATA_TRANSFORMATION_DIR_NAME_KEY = 'transformed_dir'
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY = 'transformed_train_dir'
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY = 'transformed_test_dir'
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = 'preprocessed_dir'
DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME = 'preprocessed_object_file_name'


#Model Trainer related variable
MODEL_TRAINER_ARTIFACT_DIR = 'model_trainer'
MODEL_TRAINER_CONFIG_KEY = 'model_trainer_config'
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = 'trained_model_dir'
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = 'model_file_name'
MODEL_TRAINER_BASE_ACCURACY_KEY = 'base_accuracy'
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = 'model_config_dir'
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = 'model_config_file_name'

#model.yaml related varibles
MODEL_FILE_NAME = 'model.yaml'
MODEL_FILE_PATH = os.path.join(
    ROOT_DIR,
    CONFIGRATION_DIR,
    MODEL_FILE_NAME)

GRID_SEARCH_KEY = 'grid_search'
DATASET_BALANCING_KEY = 'dataset_balancing'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY  = 'search_param_grid'
PARAM_KEY = 'params'

#Model Evaluation related variables
MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config'
MODEL_EVALUATION_FILE_NAME_KEY = 'model_evaluation_file_name'
MODEL_EVALUATION_ARTIFACT_KEY = 'model_evaluation'
BEST_MODEL_KEY = 'best_model'
HISTORY_KEY = 'history'
MODEL_PATH_KEY = 'model_path'
MODEL_ACC_KEY = 'model_acc'

#Model Pusher related variables
MODEL_PUSHER_CONFIG_KEY = 'model_pusher_config'
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY = 'model_export_dir'

#Experiment related variables
EXPERIMENT_DIR_KEY = 'experiment'
EXPERIMENT_FILE_NAME = 'experiment.csv'