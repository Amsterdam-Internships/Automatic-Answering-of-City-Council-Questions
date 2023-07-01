from setuptools import setup, find_packages

import os
import sys

# Get current directory
current_dir = os.getcwd()
# Get parent directory
parent_dir = os.path.join(current_dir, '..')
# Append parent directory to sys.path
sys.path.append(parent_dir)




setup(
    version='0.1.0',
    author='Natali-Peeva',
    description='This contains all of the packages used for the question annswering pipeline.',
    packages=find_packages(include=['src', 'src.*'])
)