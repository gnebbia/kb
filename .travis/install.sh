#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then
    pip3 install --upgrade pip
    pip3 install --upgrade setuptools
    pip3 install -r requirements.txt
    pip3 install .
    pip3 install --upgrade pyinstaller
elif [ $TRAVIS_OS_NAME = 'windows' ]; then
    python -m pip install --upgrade pip
    python -m pip install --upgrade setuptools
    python -m pip install -r requirements.txt
    python -m pip install .
    python -m pip install --upgrade pyinstaller
else
    pip install --upgrade pip
    pip install --upgrade setuptools
    pip install -r requirements.txt
    pip install .
    pip install --upgrade pyinstaller
fi

