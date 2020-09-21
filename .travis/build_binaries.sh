#!/bin/bash

if [ $TRAVIS_OS_NAME = 'osx' ]; then
  pyinstaller --paths kb/ --onefile kb/__main__.py -n kb_${TRAVIS_TAG}_osx
elif [ $TRAVIS_OS_NAME = 'windows' ]; then
  pyinstaller --paths kb/ --onefile kb/__main__.py -n kb_${TRAVIS_TAG}_win
else
  pyinstaller --paths kb/ --onefile kb/__main__.py -n kb_${TRAVIS_TAG}_linux
fi

