#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then
    pip3 install --upgrade pip
    pip3 install setuptools
    pip3 install -r requirements.txt
    pip3 install .
    pip3 install pyinstaller
elif [ $TRAVIS_OS_NAME = 'windows' ]; then
    python -m pip install --upgrade pip
    python -m pip install setuptools
    python -m pip install -r requirements.txt
    python -m pip install .
    python -m pip install pyinstaller
else
    pip install --upgrade pip
    pip install setuptools
    pip install -r requirements.txt
    pip install .
    pip install pyinstaller
fi

