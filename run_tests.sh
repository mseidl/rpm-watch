#!/bin/bash
# Martin Seidl
# run rpm_watch tests
date=$(date +'%F-%R')

pyflakes *.py | tee -a pyflakes-"$date".log
pylint *.py | tee -a pylint-"$date".log

python test_rpm_watch.py | tee -a unittest-"$date".log
python -m cProfile test_*.py | tee -a cprofile-"$date".log
