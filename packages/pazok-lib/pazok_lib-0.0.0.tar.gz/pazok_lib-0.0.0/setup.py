import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
name= 'pazok-lib',
author= 'b_azo',
description= 'test',
packages=setuptools.find_packages(),
classifiers=[
"Programming Language :: Python :: 3.9",
"Operating System :: OS Independent",
"License :: OSI Approved :: MIT License"
]
)