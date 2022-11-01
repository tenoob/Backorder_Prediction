from collections import namedtuple

TrainingPipelineCongif = namedtuple('TrainingPipelineConfig',['artifact_dir'])

DataIngestionConfig = namedtuple('DataIngestionConfig',
['dataset_download_url','tgz_download_dir','raw_data_dir','ingested_train_dir','ingested_test_dir','train_file_name','test_file_name'])

DataValidationConfig = namedtuple("DataValidationConfig",
['schema_file_path','report_file_path','report_page_file_path'])

DataTransformationConfig = namedtuple("DataTransformation",
["transformed_train_dir","transformed_test_dir","preprocessed_object_file_path"])