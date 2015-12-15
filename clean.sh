#!/bin/bash
set -ev # exit with nonzero exit code if anything fails

rm -rf env sources databases gramps*/gramps/* gramps*/addons/*
find . -name "*.stackdump" -exec rm {} +
