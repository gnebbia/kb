#!/bin/bash

if [ $TRAVIS_OS_NAME = 'windows' ]; then
    PYTHON="py"
else
    PYTHON="python3"
fi

$PYTHON -m pip install --upgrade pip setuptools
$PYTHON -m pip install -r requirements-dev.txt
$PYTHON -m pip install .
