#!/bin/bash

V_REMOVED=$(tr -d "v" <<< "$TRAVIS_TAG")
RELEASE_VER=$(tr "." "_" <<< "$V_REMOVED")
if [ $TRAVIS_OS_NAME = 'osx' ]; then
  pyinstaller --paths kb/ --onefile kb/__main__.py -n kb_${RELEASE_VER}_osx
elif [ $TRAVIS_OS_NAME = 'windows' ]; then
  pyinstaller --paths kb/ --onefile kb/__main__.py -n kb_${RELEASE_VER}_win
else
  pyinstaller --paths kb/ --onefile kb/__main__.py -n kb_${RELEASE_VER}_linux
fi

