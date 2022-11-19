from application.exception import BackorderException
from application.logger import logging
from collections import namedtuple
import numpy as np
import os,sys
from sklearn.metrics import accuracy_score,classification_report


MetricInfoArtifact = namedtuple("MetricInfoArtifact",
                                ["model_name", "model_object", "train_report", "test_report", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])


def evaluate_classification_model(
                        model_list: list,
                        x_train:np.ndarray,
                        y_train:np.array,
                        x_test:np.ndarray,
                        y_test:np.array,
                        base_accuracy: float=0.6) -> MetricInfoArtifact:
    """
    Description:
    This function compare multiple Classification model and return best model
    Params:
    model_list: list of model
    x_train: input feature of Training Dataset
    y_train: target feature of Training Dataset
    x_test: input feature of testing Dataset
    y_test: target feature of testing Dataset
    Return: 
    It returs a named tuple
    MetricInfoArtifact = namedTuple("MetricInfo",['model_name',
                                                  'model_object',
                                                  'train_report',
                                                  'test_report',
                                                  'train_accuracy',
                                                  'test_accuracy',
                                                  'model_accuracy',
                                                  'index_number'])           
    """
    try:
        index_number = 0
        metric_info_artifact = None

        for model in model_list:

            #getting model name based on model object
            model_name = str(model)
            logging.info(f"{'>>'*30} Started evaluating model: [{type(model).__name__}] {'<<'*30}")
            logging.info(f"Index number: {index_number}")
            #getting prediction for Training and Testing Dataset
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            #Calculating accuracy for Training and Testing Dataset
            train_acc = accuracy_score(y_true=y_train,y_pred=y_train_pred)
            test_acc = accuracy_score(y_true=y_test,y_pred=y_test_pred)

            train_report = classification_report(y_train,y_train_pred)
            test_report = classification_report(y_test,y_test_pred)

            #Calculating harmonic mean of train and test accuracy
            model_accuracy = (2*(train_acc*test_acc)/(train_acc+test_acc))
            diff_train_test_acc = abs(test_acc-train_acc)

            logging.info(f"length of y_train: {len(y_train)}")
            logging.info(f"length of y_train_pred: {len(y_train_pred)}")

            logging.info(f"length of y_test: {len(y_test)}")
            logging.info(f"length of y_test_pred: {len(y_test_pred)}")

            #logging all info
            logging.info(f"{'>>'*30} Score {'<<'*30}")
            logging.info(f'Train Score \t\t Test Score \t\t Avg Score')
            logging.info(f'{train_acc} \t\t {test_acc} \t\t {model_accuracy}')

            logging.info(f"{'>>'*30} Loss {'<<'*30}")
            logging.info(f'Difference Test and Train accuracy: [{diff_train_test_acc}]')

            logging.info(f"Train Report: \n{train_report}")
            logging.info(f"Test Report: \n{test_report}")

            logging.info(f"Base accuracy: {base_accuracy}")
            #if model acc is greater than base accuracy and train and test score is within certain threshold
            #we will accept that model as accepted model
            if model_accuracy >= base_accuracy and diff_train_test_acc <= 0.1:
                base_accuracy = model_accuracy

                metric_info_artifact = MetricInfoArtifact(
                    model_name=model_name,
                    model_object=model,
                    train_accuracy=train_acc,
                    test_accuracy=test_acc,
                    model_accuracy=model_accuracy,
                    train_report=train_report,
                    test_report=test_report,
                    index_number=index_number
                )

                logging.info(f"Accepted model found: {metric_info_artifact}")

            index_number+=1

        if metric_info_artifact is None:
            logging.info(f"No model found with higher accuarcy then base accuracy and train test score within certain threshold")
            #raise Exception("Try some other Models")

        return metric_info_artifact

    except Exception as e:
        raise BackorderException(e,sys) from e