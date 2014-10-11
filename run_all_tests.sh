#!/bin/bash


cd test

for file in `ls *_ut.py`; do
    echo "run file: $file"
    python2 $file || break
    
done
