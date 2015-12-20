#!/bin/bash

set -ex # exit with nonzero exit code if anything fails

source vars.sh


##############################################
###  4.2
##############################################

$WORKON_42
$PYTHON_42 run_reports.py 42


##############################################
###  5.0
##############################################

$WORKON_50
$PYTHON_50 run_reports.py 50
