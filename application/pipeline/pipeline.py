
from application.component.data_ingestion import DataIngestion
from application.component.data_validation import DataValidation
from application.component.data_transformation import DataTransformation
from application.component.model_trainer import ModelTrainer
from application.component.model_evaluation import ModelEvaluation
from application.component.model_pusher import ModelPusher
from application.constant import *
from application.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact , DataTransformationArtifact , ModelTrainerArtifact , ModelEvaluationArtifact ,ModelPusherArtifact
from application.logger import logging
from application.exception import BackorderException
from application.config.configration import Configration

from collections import namedtuple
from datetime import datetime
from threading import Thread
from typing import List
from flask import Flask

import pandas as pd
import uuid
import os,sys


Experiment = namedtuple("Experiment",
['experiment_id','initialization_timestamp','artifact_time_stamp',
'running_status','start_time','stop_time','execution_time',
'message','experiment_file_path','accuracy','is_model_accepted'])


class Pipeline(Thread):
    experiment: Experiment = Experiment(* ( [None]*11 ) )
    experiment_file_path = None
    
    def __init__(self,config:Configration = Configration()) -> None:
        try:
            os.makedirs(config.training_pipeline_config.artifact_dir,exist_ok=True)

            Pipeline.experiment_file_path = os.path.join(
                config.training_pipeline_config.artifact_dir,
                EXPERIMENT_DIR_KEY,
                EXPERIMENT_FILE_NAME
            )

            super().__init__(daemon=False , name='pipeline')
            
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

    def start_data_transformation(self,
                                data_ingestion_artifact:DataIngestionArtifact,     
                                    data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_artifact = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.config.get_data_transfomation_config())

            return data_transformation_artifact.initate_data_transformation()
        except Exception as e:
            raise BackorderException(e,sys) from e
    
    def start_model_trainer(self,
                            data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config = self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact)
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise BackorderException(e,sys) from e
    
    def start_model_evaluation(self,
                                data_ingestion_artifact: DataIngestionArtifact,
                                data_validation_artifact: DataValidationArtifact,
                                model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_eval = ModelEvaluation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact,
                model_evaluation_config=self.config.get_model_evaluation_config()
            )

            return model_eval.initiate_model_evaluation()
        except Exception as e:
            raise BackorderException(e,sys) from e

    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(
                model_pusher_config=self.config.get_model_pusher_config(),
                model_eval_aritfact=model_eval_artifact
            )

            return model_pusher.initiate_model_pusher()
        except Exception as e:
            raise BackorderException(e,sys) from e

    def save_experiment(self):
        try:
            if Pipeline.experiment.experiment_id is not None:
                experiment = Pipeline.experiment

                experiment_dict = experiment._asdict()
                experiment_dict: dict = {key:[value] for key,value in experiment_dict.items()}

                experiment_dict.update({
                    "created_time_stamp": [datetime.now()],
                    "experiment_file_path" : [os.path.basename(Pipeline.experiment.experiment_file_path)]
                })

                experiment_report = pd.DataFrame(experiment_dict)

                os.makedirs(os.path.dirname(Pipeline.experiment_file_path),exist_ok=True)

                if os.path.exists(Pipeline.experiment_file_path):
                    experiment_report.to_csv(Pipeline.experiment_file_path,index=False,header=False,mode='a')
                else:
                    experiment_report.to_csv(Pipeline.experiment_file_path,mode='w',index=False,header=True)
            else:
                print("First Start Experiment")
                logging.info(f"First Start Experiment")
        except Exception as e:
            raise BackorderException(e,sys)


    def run_pipeline(self):
        try:

            if Pipeline.experiment.running_status:
                logging.info(f"Pipeline is already running")
                return Pipeline.experiment
            
            logging.info(f"Pipeline Starting.")
            Experiment_id = str(uuid.uuid4())

            Pipeline.experiment = Experiment(
                experiment_id=Experiment_id,
                initialization_timestamp=self.config.current_time_stamp,
                artifact_time_stamp=self.config.current_time_stamp,
                running_status=True,
                start_time=datetime.now(),
                execution_time=None,
                experiment_file_path=Pipeline.experiment_file_path,
                is_model_accepted=None,
                message="pipeline has been started",
                accuracy=None,
                stop_time=None
            )

            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()


            #data ingestion 
            data_ingestion_artifact = self.start_data_ingestion()

            #data validation
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            #data transformation
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )

            #model training
            model_training_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            #model evaluation
            model_evaluation_artifact = self.start_model_evaluation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_training_artifact)

            #model pusher
            if model_evaluation_artifact.is_model_accepted:
                model_pusher_artifact = self.start_model_pusher(model_eval_artifact=model_evaluation_artifact)
                logging.info(f"model pusher artifact: {model_pusher_artifact}")
            else:
                logging.info(f"Trained Model Rejected")
            
            logging.info(f"Pipeline Over")

            stop_time = datetime.now()

            Pipeline.experiment = Experiment(
                experiment_id = Pipeline.experiment.experiment_id,
                initialization_timestamp=self.config.current_time_stamp,
                artifact_time_stamp=self.config.current_time_stamp,
                running_status=False,
                start_time=Pipeline.experiment.start_time,
                stop_time= stop_time,
                execution_time= stop_time - Pipeline.experiment.start_time,
                message= "Pipeline has been Completed",
                experiment_file_path=Pipeline.experiment_file_path,
                is_model_accepted= model_evaluation_artifact.is_model_accepted,
                accuracy = model_evaluation_artifact.model_acc
            )

            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()
        except Exception as e:
            raise BackorderException(e,sys) from e


    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise BackorderException(e,sys) from e

    @classmethod
    def get_experiment_status(cls , limit: int=5) -> pd.DataFrame:
        try:
            if os.path.exists(Pipeline.experiment_file_path):
                df = pd.read_csv(Pipeline.experiment_file_path)
                limit = -1*(int(limit))
                return df[limit:].drop(columns=['experiment_file_path','initialization_timestamp'],axis=1)
            else:
                return pd.DataFrame()
        except Exception as e:
            raise BackorderException(e,sys) from e