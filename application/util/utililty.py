import yaml
from application.exception import BackorderException
import os,sys

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



