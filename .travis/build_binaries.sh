#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then
  pyinstaller --onefile --paths kb/ kb/__main__.py -n kb_${TRAVIS_TAG}_osx
elif [ $TRAVIS_OS_NAME = 'windows' ]; then
  pyinstaller --onefile --paths kb/ kb/__main__.py -n kb_${TRAVIS_TAG}_win
else
  pyinstaller --onefile --paths kb/ kb/__main__.py -n kb_${TRAVIS_TAG}_linux
fi

