#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages


setup(name='kb-manager',
      version='0.1.2',
      description='A minimalist knowledge base manager',
      keywords='kb',
      author='gnc',
      author_email='nebbionegiuseppe@gmail.com',
      url='https://github.com/gnebbia/kb',
      download_url='https://github.com/gnebbia/kb/archive/v0.1.2.tar.gz',
      license='GPLv3',
      long_description=io.open(
          './docs/README.md', 'r', encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[ 'Programming Language :: Python',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Programming Language :: Python :: 3.8',
                    'Operating System :: OS Independent',
                   ],
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      install_requires=["colored","toml","attr","attrs"],
      python_requires='>=3.6',
      entry_points={
           'console_scripts':[
               'kb = kb.main:main',
           ]
      },
      )
