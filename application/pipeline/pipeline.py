from tempfile import TemporaryFile
from tkinter import E
from application.component.data_ingestion import DataIngestion
from application.component.data_validation import DataValidation
from application.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from application.logger import logging
from application.exception import BackorderException
from application.config.configration import Configration
import os,sys

class Pipeline():
    
    def __init__(self,config:Configration = Configration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise BackorderException(e,sys) from e


    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())

            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise  BackorderException(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(
                data_validation_config=self.config.get_data_validation_cofig(),
                data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_data_validation()
        except Exception as e:
            raise BackorderException(e,sys) from e

    def run_pipeline(self):
        try:
            #data ingestion 
            data_ingestion_artifact = self.start_data_ingestion()

            #data validation
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise BackorderException(e,sys) from e