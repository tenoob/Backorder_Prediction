import shutil
from application.entity.config_entity import  ModelPusherConfig
from application.entity.artifact_entity import ModelEvaluationArtifact , ModelPusherArtifact
from application.logger import logging
from application.exception import BackorderException
import os,sys

class ModelPusher:
    def __init__(self,
                 model_pusher_config: ModelPusherConfig,
                 model_eval_aritfact: ModelEvaluationArtifact) -> None:
        try:
            logging.info(f"\n{'>'*20} Model Pusher Log Started. {'<'*20}")
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_aritfact
        except Exception as e:
            raise BackorderException(e,sys) from e

    def export_model(self):
        try:
            evaluated_model_file_path = self.model_eval_artifact.evaluted_model_path

            export_dir = self.model_pusher_config.export_dir_path

            model_file_name = os.path.basename(evaluated_model_file_path)

            export_model_file_path = os.path.join(
                export_dir,
                model_file_name
            )

            logging.info(f"Exported Model File: {export_model_file_path}")
            os.makedirs(export_model_file_path,exist_ok=True)

            shutil.copy(src=evaluated_model_file_path , dst= export_model_file_path)

            #space to save file in db

            logging.info(f"Trained model: {evaluated_model_file_path} is copyed in Export Dir: {export_model_file_path}")

            model_pusher_artifact = ModelPusherArtifact(
                is_model_pushed=True,
                export_model_file_path=export_model_file_path
            )

            logging.info(f"Model Pusher Artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise BackorderException(e,sys) from e


    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            return self.export_model()
        except Exception as e:
            raise BackorderException(e,sys)
        

    def __del__(self):
        logging.info(f"\n{'>'*20} Model Pusher Log Completed. {'<'*20}\n")
