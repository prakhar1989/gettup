#!/usr/bin/env python
# coding: utf-8
import sys
from setuptools import setup, find_packages

requirements = ['requests>=2.0.0']
if sys.version_info < (2, 7):
    requirements.append('argparse>=1.2.1')

setup(name='gettup',
      version='0.3.0',
      description='A command-line file sharing utility for ge.tt',
      long_description=open("README.md").read(),
      keywords="CLI filesharing file sharing upload command-line",
      author='Prakhar Srivastav',
      author_email='prakhar1989@gmail.com',
      url='https://github.com/prakhar1989/gett/',
      license='MIT',
      packages=find_packages(),
      py_modules=["gett"],
      install_requires=requirements,
      entry_points = {
          'console_scripts': [ 'gett = gett:main' ]
      },
      zip_safe=False
     )
