from collections import namedtuple

TrainingPipelineCongif = namedtuple('TrainingPipelineConfig',['artifact_dir'])

DataIngestionConfig = namedtuple('DataIngestionConfig',
['dataset_download_url','tgx_download_dir','raw_data_dir','ingested_train_dir','ingested_test_dir'])