import yaml
from application.exception import BackorderException
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
            return np.load(file_obj)
    except Exception as e:
        raise BackorderException(e,sys) from e
