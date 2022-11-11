from application.logger import logging
from application.exception import BackorderException
from application.util.utililty import read_yaml_file
from application.constant import *
import os,sys,importlib
from collections import namedtuple
from typing import List


InitializedModelDetail = namedtuple('InitializedModelDetail',
['model_serial_number','model','param_grid_search','model_name'])

GridSearchBestModel = namedtuple('GridSearchBestModel',
['model_serial_number','model','best_model','best_parameters','best_score'])

BestModel = namedtuple('BestModel',
['model_serial_number','model','best_model','best_parameters','best_score'])

MetricInfoAritfact = namedtuple('MetricInfoArtifact',
['model_name','model_object','train_rmse','test_rmse','train_accuracy','test_accuracy','model_accuracy','index_number'])

class ModelFactory:
    def __init__(self,model_config_path:str = None) -> None:
        try:
            self.config:dict = read_yaml_file(file_path=model_config_path)
            self.grid_search_cv_module :str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_class_name:str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data: dict = dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])

            self.model_initialization_config: dict = dict(self.config[MODEL_SELECTION_KEY])

            self.initialization_model_list = None
            self.grid_searched_best_model_list = None
        except Exception as e:
            raise BackorderException(e,sys) from e

    @staticmethod
    def class_for_name(module_name:str , class_name:str):
        try:
            
            #loading the module, otherwise raise [ImportError: Module not found] 
            module = importlib.import_module(module_name)

            #getting the class, otherwise raise [AttribureError: class cannot be found]
            logging.info(f"Executing Command: from {module} import {class_name}")
            class_ref = getattr(module,class_name)
            return class_ref
        except Exception as e:
            raise BackorderException(e,sys) from e
    

    @staticmethod
    def update_propery_of_class(instance_ref:object, property_data:dict):
        try:
            if not isinstance(property_data,dict):
                raise Exception('Property_data parameter required in Dictionary')
            print(property_data)

            for key,value in property_data.items():
                logging.info(f"Executing:$ {str(instance_ref)}.{key}={value}")
                setattr(instance_ref,key,value)
            
            return instance_ref
        except Exception as e:
            raise BackorderException(e,sys) from e

    
    def get_initialied_model_list(self) -> List[InitializedModelDetail]:
        """
        This Function returns a list of model details
        return List[ModelDetail]
        """
        try:
            initialized_model_list = []
            for model_serial_number in self.model_initialization_config.keys():
                model_initialization_config = self.model_initialization_config[model_serial_number]
                
                #importing the class
                model_obj_ref = ModelFactory.class_for_name(
                    module_name=model_initialization_config[MODULE_KEY],
                    class_name=model_initialization_config[CLASS_KEY])

                model = model_obj_ref()

                if PARAM_KEY in model_initialization_config:

                    #get all the params of the model
                    model_obj_property_data = dict(model_initialization_config[PARAM_KEY])

                    model = ModelFactory.update_propery_of_class(
                        instance_ref=model,
                        property_data=model_obj_property_data)
                    
                param_grid_search = model_initialization_config[SEARCH_PARAM_GRID_KEY]
                model_name = f"{model_initialization_config[MODULE_KEY]}.{model_initialization_config[CLASS_KEY]}"

                model_initialization_config = InitializedModelDetail(
                        model_serial_number=model_serial_number,
                        model=model,
                        param_grid_search=param_grid_search,
                        model_name=model_name)

                logging.info(f"Initalized model: {model_initialization_config}")

                initialized_model_list.append(model_initialization_config)

            self.initialization_model_list = initialized_model_list
            return self.initialization_model_list
        except Exception as e:
            raise BackorderException(e,sys) from e


    def execute_grid_search_operation(
                            self,
                            initialized_model: InitializedModelDetail,
                            input_feature , output_feature) -> GridSearchBestModel:
        """
        execute_grid_search_opeartion(): function will perform parameter search opearation and 
        it will return the best optimistic model with best parameter
        """
        try:
            
            #instantiating GridSearchCV class
            grid_search_cv_ref = ModelFactory.class_for_name(
                module_name=self.grid_search_cv_module,
                class_name=self.grid_search_class_name)

            grid_search_cv = grid_search_cv_ref(estimator=initialized_model.model,
                                                param_grid = initialized_model.param_grid_search)

            grid_search_cv = ModelFactory.update_propery_of_class(
                                                    grid_search_cv,
                                                    self.grid_search_property_data)

              
            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__} Started." {"<<"*30}'
            logging.info(message)

            grid_search_cv.fit(input_feature, output_feature)

            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__}" completed {"<<"*30}'
            grid_searched_best_model = GridSearchBestModel(model_serial_number=initialized_model.model_serial_number,
                                                             model=initialized_model.model,
                                                             best_model=grid_search_cv.best_estimator_,
                                                             best_parameters=grid_search_cv.best_params_,
                                                             best_score=grid_search_cv.best_score_)
            
            return grid_searched_best_model

        except Exception as e:
            raise BackorderException(e,sys) from e
    
    
    def initiate_best_parameter_search_for_initialized_model(
                            self,
                            initialized_model: InitializedModelDetail,
                            input_feature,output_feature) -> GridSearchBestModel:
        """
        Initiate_best_parameter_search_for_initialized_model(): function will perform parameter search opearation
        and it will return the best optimistic model with best parameter.
        """
        try:
            return self.execute_grid_search_operation(
                initialized_model=initialized_model,
                input_feature=input_feature,
                output_feature=output_feature)
        except Exception as e:
            raise BackorderException(e,sys) from e
    
    def initiate_best_parameter_search_for_initialized_models_list(
                            self,
                            initialized_model_list:List [InitializedModelDetail],
                            input_feature, output_feature ) -> List[GridSearchBestModel]:
        try:
            self.grid_searched_best_model_list = []

            for initialized_model in initialized_model_list:
                
                #Do grid gearch and return best parameter for each model
                grid_search_best_model = self.initiate_best_parameter_search_for_initialized_model(
                    initialized_model=initialized_model,
                    input_feature=input_feature,
                    output_feature=output_feature
                )

                logging.info("grid_seach_best_model")
                self.grid_searched_best_model_list.append(grid_search_best_model)
            
            logging.info(f"grid_search_best_model_list: {self.grid_searched_best_model_list}")
            return self.grid_searched_best_model_list

        except Exception as e:
            raise BackorderException(e,sys) from e


    @staticmethod
    def get_best_model_from_grid_searched_best_model_list(
                    grid_searched_best_model_list: List[GridSearchBestModel],
                    base_accuracy=0.6) -> BestModel:
        try:
            best_model = None
            for grid_searched_best_model in grid_searched_best_model_list:
                if base_accuracy < grid_searched_best_model.best_score:
                    logging.info(f"Acceptable model found:{grid_searched_best_model}")
                    base_accuracy = grid_searched_best_model.best_score

                    best_model = grid_searched_best_model
            if not best_model:
                raise Exception(f"None of Model has base accuracy: {base_accuracy}")
            logging.info(f"Best model: {best_model}")
            return best_model
        except Exception as e:
            raise BackorderException(e,sys) from e


    def get_best_model(self,x,y,base_accuracy=0.6) -> BestModel:
        try:
            logging.info(f"Started Initializing Model from Config file.")

            initialized_model_list = self.get_initialied_model_list()
            logging.info(f"List of all Initialized Models: {initialized_model_list}")

            grid_searched_best_model_list = self.initiate_best_parameter_search_for_initialized_models_list(
                initialized_model_list=initialized_model_list,
                input_feature=x,
                output_feature=y
            )

            return ModelFactory.get_best_model_from_grid_searched_best_model_list(
                grid_searched_best_model_list=grid_searched_best_model_list,
                base_accuracy=base_accuracy)

        except Exception as e:
            raise BackorderException(e,sys) from e

    