#!/bin/bash

. ~/.virtualenvs/picampro/bin/activate

export QT_QPA_PLATFORM="eglfs"
export QT_IM_MODULE="qtvirtualkeyboard"

python src/main.py

