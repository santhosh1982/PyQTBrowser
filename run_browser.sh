#!/usr/bin/env bash

GCC_LIB=$(gcc --print-file-name=libatomic.so.1 | xargs dirname)
export LD_LIBRARY_PATH=$GCC_LIB:$LD_LIBRARY_PATH

for lib_path in /nix/store/*-libXtst-*/lib /nix/store/*-qt6-*/lib /nix/store/*xorg-*/lib; do
    if [ -d "$lib_path" ]; then
        export LD_LIBRARY_PATH=$lib_path:$LD_LIBRARY_PATH
    fi
done

python main.py
