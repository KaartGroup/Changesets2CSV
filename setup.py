#!/usr/bin/env python3

from setuptools import setup

setup(name='changesets2CSV',
      version='0.4.0',
      description='OSM Changesets CSV writer',
      url='https://github.com/KaartGroup/Changesets2CSV',
      author='Kaart',
      maintainer='Zack LaVergne',
      maintainer_email='zack@kaartgroup.com',
      license='MIT',
      python_requires='>3.6.0',
      scripts=['changesets2CSV/changesets2CSV'],
      install_requires=[
            'XlsxWriter>=1.1.7',
            'CacheControl>=0.12.0',
            'requests>=2.21.0'
      ])
