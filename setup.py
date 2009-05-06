from setuptools import setup, find_packages
import sys,os

setup(name='motmot.fview_periodic_trigger',
      description='periodic trigger plugin for FView',
      version='0.0.1',
      packages = find_packages(),
      author='Andrew Straw',
      author_email='strawman@astraw.com',
      url='http://code.astraw.com/projects/motmot',
      entry_points = {
    'motmot.fview.plugins':'fview_periodic_trigger = motmot.fview_periodic_trigger.fview_periodic_trigger:FviewPeriodicTrigger',
    },
      install_requires = ['motmot.fview>=0.5.3'],
      )
