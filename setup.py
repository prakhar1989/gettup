#!/usr/bin/env python
# coding: utf-8
import sys
from setuptools import setup, find_packages

requirements = ['requests']
if sys.version_info < (2, 7):
    requirements.append('argparse')

setup(name='gettup',
      version='0.1',
      description='A command-line file sharing utility for ge.tt',
      keywords="CLI filesharing file sharing upload command-line"
      author='Prakhar Srivastav',
      author_email='prakhar1989@gmail.com',
      url='https://github.com/prakhar1989/gett/',
      license='MIT',
      packages=find_packages(),
      #py_modules=['gett'],
      install_requires=['requests'],
      entry_points = {
          'console_scripts': [ 'gett = gett:main' ]
      },
      zip_safe=False
     )

