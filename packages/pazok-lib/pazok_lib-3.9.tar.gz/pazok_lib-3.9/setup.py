from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    description = f.read()
setup(
name= 'pazok-lib',
version='3.9',
author= 'b_azo',
packages=find_packages(),
install_requires=[
    # Add dependencis here.
    #e.g. 'numpy>=1.11.1'
],
long_description=description,
long_description_content_type="text/markdown",
)