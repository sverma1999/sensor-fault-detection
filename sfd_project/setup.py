# find_packages() will automatically find all the packages in the project, from the root directory.
from setuptools import find_packages, setup
from typing import List


# Declaring variables for setup functions
COLLECTION_NAME = "sensor"
VERSION = "0.0.1"
AUTHOR = "Shubham Verma"
EMAIL = "vshubhamkam05@gmail.com"

REQUIREMENT_FILE_NAME = "requirements.txt"

HYPHEN_E_DOT = "-e ."


def get_requirements() -> List[str]:
    """
    Description: This function is going to return list of requirement
    mention in requirements.txt file
    return This function is going to return a list which contain name
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [
            requirement_name.replace("\n", "") for requirement_name in requirement_list
        ]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list


# setup() function will take all the details from setup.py file and create this project as a package.
setup(
    name=COLLECTION_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    packages=find_packages(),
    install_requires=get_requirements(),
)
