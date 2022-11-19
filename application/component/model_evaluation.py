from application.entity.config_entity import ModelEvaluationConfig
from application.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,ModelTrainerArtifact, ModelEvaluationArtifact
from application.entity.model_eval import evaluate_classification_model
from application.util.utililty import *
from application.logger import logging
from application.exception import BackorderException
import os,sys

class ModelEvaluation:

    def __init__(self,
                 model_evaluation_config:ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact) -> None:
        try:
            logging.info(f"\n{'>'*20} Model Evaluation Log Started. {'<'*20}")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise BackorderException(e,sys) from e

    def get_best_model(self):
        try:
            model = None

            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path)
                return model

            model_eval_file_content = read_yaml_file(file_path=model_evaluation_file_path)
            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                return model
            
            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            logging.info(f"Best model: {model}")
            return model
        except Exception as e:
            raise BackorderException(e,sys) from e

    def update_evaluation_report(self,model_eval_artifact: ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path

            model_eval_content = read_yaml_file(file_path=eval_file_path)

            model_eval_content = dict() if model_eval_content is None else model_eval_content

            current_deployed_model = None
            if BEST_MODEL_KEY in model_eval_content:
                current_deployed_model = model_eval_content[BEST_MODEL_KEY]
            
            logging.info(f"Previous Evaluation Report: {current_deployed_model}")

            eval_result = {
                BEST_MODEL_KEY:{
                    MODEL_PATH_KEY: model_eval_artifact.evaluted_model_path
                }
            }

            if current_deployed_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: current_deployed_model}

                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY:model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated Evaluation Report: {model_eval_content}")
            write_yaml_file(file_path=eval_file_path,data=model_eval_content)
        except Exception as e:
            raise BackorderException(e,sys) from e


    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path
            train_dataframe = load_data(
                file_path=train_file_path,
                schema_file_path=schema_file_path)

            test_dataframe = load_data(
                file_path=test_file_path,
                schema_file_path=schema_file_path)

            schema_content = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema_content[TARGET_COLUMN_KEY]

            #separating target column from df
            logging.info(f"One Hot Encoding and Converting target column into numpy array")
            train_target_arr = pd.get_dummies(train_dataframe[target_column_name],drop_first=True)
            train_target_arr = np.array(train_target_arr)

            test_target_arr = pd.get_dummies(test_dataframe[target_column_name],drop_first=True)
            test_target_arr = np.array(test_target_arr)
            logging.info(f"Conversion of Target column into numpy array Completed")

            #dropping target from df
            logging.info(f"Dropping Target column from Dataframe")
            train_dataframe.drop(target_column_name,axis=1,inplace=True)
            test_dataframe.drop(target_column_name,axis=1,inplace=True)
            logging.info(f'Dropping of Target column from dataframe Completed')

            current_best_model = self.get_best_model()
            logging.info(f"Current best model: {current_best_model}")

            if current_best_model is None:
                logging.info(f"No Existing Model Found hence Accepted Trained Model")
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=True,
                    evaluted_model_path=trained_model_file_path)

                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")
                return model_evaluation_artifact
            
            model_list = [current_best_model,trained_model_object]

            metric_info_artifact = evaluate_classification_model(
                model_list=model_list,
                x_train=train_dataframe,
                y_train=train_target_arr,
                x_test=test_dataframe,
                y_test=test_target_arr,
                base_accuracy=self.model_trainer_artifact.model_accuracy
            )

            logging.info(f"Model Evaluation Completed. Model Metric Artifact: {metric_info_artifact}")

            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(
                    is_model_accepted=False,
                    evaluted_model_path=trained_model_file_path
                )
                logging.info(metric_info_artifact)
                return response
            
            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=True,
                    evaluted_model_path=trained_model_file_path
                )
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model Accepted. Model Evaluation Artifact: {model_evaluation_artifact} created")
            else:
                logging.info(f"Trained model is not better then existing model hence NOT ACCEPTED")
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=False,
                    evaluted_model_path=trained_model_file_path
                )
                
            return model_evaluation_artifact
        except Exception as e:
            raise BackorderException(e,sys) from e

    def __del__(self):
        logging.info(f"\n{'>'*20} Model Evaluation Log Completed. {'<'*20}\n")


        