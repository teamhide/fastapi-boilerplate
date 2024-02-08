#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m' # Reset color

DIR=".venv"

# Checking python version
if [[ $(python3 --version 2>&1) =~ Python\ 3\.[0-9]+\.[0-9]+ ]]; then
    echo -e "$GREEN  [Info]Python 3 is installed."
else
    echo -e "$RED  [Error]Python 3 is not installed. Terminating..."
    exit
fi

# Delete first
rm -rf "$DIR"

if [ -d "$DIR" ]; then
  # Take action if $DIR exists. #
  echo -e "$GREEN [Info]Virtual environemnt is already existed: ${DIR}, ignored installation process."
  exit
fi

echo -e "$GREEN  [Info]Creating venv folder..."
python3 -m venv "$DIR"

if [ ! -d "$DIR" ]; then
  # Take action if $DIR exists. #
  echo -e "$RED  [Error]Unable to create $DIR folder!"
  echo -e "$RED  [Error]Terminating..."
  exit
fi


# Created successfully
source ./.venv/bin/activate
ls -la

echo -e "$GREEN  [Info] Installing project needed dependencies with pip... !!!"

echo -e "$RESET"
python -m pip install poetry

echo -e "$GREEN  [Info]Update pip !!!"
pip install --upgrade pip

echo -e "$GREEN  [Info]Installing poetry packages !!!"
poetry install  --no-root

echo -e "$GREEN [Info]Install debugger"
pip install debugpy
poetry add debugpy

echo -e "$GREEN  [Info]Finished !!!"