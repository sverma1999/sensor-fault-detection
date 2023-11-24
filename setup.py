from setuptools import find_packages, setup
from typing import List


def get_requirements() -> List[str]:
    """
    This function will return list of requirements
    """
    requirement_list: List[str] = []

    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    return requirement_list


# this setup function will take all the details from above and package the code.
# setup function will add the dependencies in the package, you can verify it by looking at the egg file.
# you can find the egg file in the dist folder. PKG-INFO file will have all the details about the package.
# "-e ." is equivalent of using "find_packages()" in setup.py file.
# Note: find_requirements() function will find list of dependencies from requirements.txt file.
setup(
    name="sensor",
    version="0.0.1",
    author="Shubham Verma",
    author_email="vshubhamkam05@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
