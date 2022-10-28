from collections import namedtuple

TrainingPipelineCongif = namedtuple('TrainingPipelineConfig',['artifact_dir'])

DataIngestionConfig = namedtuple('DataIngestionConfig',
['dataset_download_url','tgz_download_dir','raw_data_dir','ingested_train_dir','ingested_test_dir','train_file_name','test_file_name'])