import yaml
from application.exception import BackorderException
from application.logger import logging
from application.constant import *
import os,sys
import pandas as pd
import numpy as np
import dill

def read_yaml_file(file_path:str ) -> dict:
    """
    Read YAML file and  return its content as dict
    file_path: str
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise BackorderException(e,sys) from e


def load_data(file_path:str , schema_file_path:str) -> pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(schema_file_path)

        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe = pd.read_csv(file_path,usecols=dataset_schema[COLUMNS_TO_USE_KEY])


        #droping rows which has target as nan
        logging.info(f"Shape of the File: {dataframe.shape}")
        


        errror_message = ""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                errror_message = f"{errror_message} \nColumn: [ {column} ] is not in the schema"
        
        if len(errror_message)>0:
            raise Exception(errror_message)

        return dataframe
    except Exception as e:
        raise BackorderException(e,sys) from e

    
def save_numpy_array_data(file_path:str , array:np.array):
    """
    Save numpy array to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)

    except Exception as e:
        raise BackorderException(e,sys) from e


def save_object(file_path:str, obj):
    """
    file_path: str
    pbj: any Sort of object
    """
    try:
        dir_path =os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    
    except Exception as e:
        raise BackorderException(e,sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj,allow_pickle=True)
    except Exception as e:
        raise BackorderException(e,sys) from e


def get_sample_model_config_yaml_file(export_dir:str):
    try:
        model_config = {
            GRID_SEARCH_KEY:{
                MODULE_KEY: 'sklearn.model_selection',
                CLASS_KEY: 'GridSearchCV',
                PARAM_KEY: {
                    'cv':5,
                    'verbose':2
                }
            },
            MODEL_SELECTION_KEY: {
                'module_0':{
                    MODULE_KEY:'module_of_model',
                    CLASS_KEY: 'ModelClassName',
                    PARAM_KEY:
                    {
                        'param_name1': 'value1',
                        'param_name2':'value2',
                    },
                    SEARCH_PARAM_GRID_KEY:
                    {
                        'param_name':['param_value1','param_value2']
                    }
                },
            }
        }

        os.makedirs(export_dir,exist_ok=True)
        export_file_path = os.path.join(export_dir,"model.yaml")
        with open(export_file_path,'w') as file:
            yaml.dump(model_config,file)
        return export_file_path
    except Exception as e:
        raise BackorderException(e,sys) from e


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise BackorderException(e,sys) from e

def write_yaml_file(file_path:str , data:dict = None):
    """
    Create yaml file
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise BackorderException(e,sys) from e