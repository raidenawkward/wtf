#!/bin/bash

PYTHON=python3
SCRIPT_PATH=`dirname $0`
TARGET=console.py

cd $SCRIPT_PATH

$PYTHON $TARGET $@
