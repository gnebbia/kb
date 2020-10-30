#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages


setup(name='kb-manager',
      version='0.1.5',
      description='A minimalist knowledge base manager',
      keywords='kb', 
      author='gnc',
      author_email='nebbionegiuseppe@gmail.com',
      url='https://github.com/gnebbia/kb',
      download_url='https://github.com/gnebbia/kb/archive/v0.1.5.tar.gz',
      license='GPLv3',
      platforms='any',
      zip_safe=False,
      classifiers=['Programming Language :: Python',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Programming Language :: Python :: 3.8',
                    'Operating System :: OS Independent',
                   ],
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      install_requires=["toml", "attr", "attrs", "flask", "flask-httpauth"],
      python_requires='>=3.6',
      entry_points={
           'console_scripts': [
               'kb = kb.main:main',
           ]
      },
      ) 
