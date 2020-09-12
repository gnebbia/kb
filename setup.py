#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages


setup(name='kb',
      version='0.1.1',
      description='A knowledge base organizer',
      keywords='kb',
      author='gnc',
      author_email='nebbionegiuseppe@gmail.com',
      url='https://github.com/gnebbia/kb',
      license='GPLv3',
      long_description=io.open(
          './docs/README.rst', 'r', encoding='utf-8').read(),
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   ],
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      install_requires=["colored","toml","attr","attrs"],
      entry_points={
           'console_scripts':[
               'kb = kb.main:main',
           ]
      },
      )
