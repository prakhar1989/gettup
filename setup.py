#!/usr/bin/env python
# coding: utf-8

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(name='gett',
      version='0.1',
      description='A command-line file sharing utility for ge.tt',
      author='Prakhar Srivastav',
      author_email='prakhar1989@gmail.com',
      url='https://github.com/prakhar1989/gett/',
      py_modules=['gett'],
      install_requires=['distribute'],
      entry_points = {
          'console_scripts': [
              'gett = gett_uploader:entry_point'
          ]
      }
     )

