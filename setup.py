from setuptools import setup,find_packages
from typing import List
import os

#declaring variables
PROJECT_NAME = 'backorder_prediction'
VERSION = '0.0.2'
AUTHOR = 'n00b'
DESCRIPTION = ''
PACKAGES = find_packages()
REQUIREMENT_FILE_NAME = 'requirement.txt'
HYPHeN_E_DOT = "-e ."

def get_requirements_list() -> list[str]:
    """
    Description: This function is going to return list of
    requrement mention in requirements.txt

    return: This function is going to return a list which
    contain name of librarires mentioned in requirement.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace('\n',"") for requirement_name in requirement_list]
        if HYPHeN_E_DOT in requirement_list:
            requirement_list.remove(HYPHeN_E_DOT)
        return requirement_list

setup(
    name=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    packages=find_packages(),
    install_requires = get_requirements_list()
)