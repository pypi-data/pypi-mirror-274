from setuptools import setup, find_packages
setup(
name='ezsmtp',
version='0.0.1',
author='rephy',
author_email='rapmanayon@gmail.com',
description='Makes sending emails via SMTP so much easier!',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3'
)