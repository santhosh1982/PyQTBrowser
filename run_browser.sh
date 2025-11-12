#!/usr/bin/env bash

GCC_LIB=$(gcc --print-file-name=libatomic.so.1 | xargs dirname)

LIB_PATHS="$GCC_LIB"
for pattern in libXtst qt6 xorg mesa systemd gbm; do
    for lib_dir in /nix/store/*-${pattern}-*/lib; do
        if [ -d "$lib_dir" ]; then
            LIB_PATHS="$lib_dir:$LIB_PATHS"
        fi
    done
done

export LD_LIBRARY_PATH="$LIB_PATHS:$LD_LIBRARY_PATH"

python main.py
