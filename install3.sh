#!/bin/bash

set -ev # exit with nonzero exit code if anything fails

source vars.sh


##############################################
###  Python3 environment
##############################################

mkdir -v -p env
virtualenv --system-site-packages --python=$ENV_PYTHON3_VERSION env/gramps50;

$WORKON_50
echo "Running python environment:"
which python$PYTHON3_SUFFIX
# which pip$PYTHON3_SUFFIX
$PIP_50 install Django\<1.8
$PIP_50 install pyicu\<1.9
$PIP_50 install cffi
$PIP_50 install cairosvg
$PIP_50 install Pillow


##############################################
###  Clone GITHUB addons
##############################################

mkdir -v -p sources/addons
git clone --depth=1 --branch=master https://github.com/$ADDONS_REPO_SLUG.git sources/addons


##############################################
###  4.2
##############################################

$WORKON_42
### clone
mkdir -v -p $GRAMPS_RESOURCES
git clone --depth=1 --branch=maintenance/gramps42 https://github.com/$GRAMPS_REPO_SLUG.git $GRAMPS_RESOURCES
cd $GRAMPS_RESOURCES
$PYTHON_42 setup.py build
cd $MY_PATH

## Copy addons
mkdir -v -p $GRAMPS_PLUGINS
if [ -z "$(ls -A $GRAMPS_PLUGINS)" ]
then
	for archive in $(ls $GRAMPS_ADDONS_SOURCE/download/*.tgz); do
		tar -xzf $archive -C $GRAMPS_PLUGINS
	done
fi


##############################################
###  5.0
##############################################

$WORKON_50
### clone
mkdir -v -p $GRAMPS_RESOURCES
git clone --depth=1 --branch=master https://github.com/$GRAMPS_REPO_SLUG.git $GRAMPS_RESOURCES
cd $GRAMPS_RESOURCES
$PYTHON_50 setup.py build
cd $MY_PATH

## Copy addons
mkdir -v -p $GRAMPS_PLUGINS
if [ -z "$(ls -A $GRAMPS_PLUGINS)" ]
then
	for archive in $(ls $GRAMPS_ADDONS_SOURCE/download/*.tgz); do
		tar -xzf $archive -C $GRAMPS_PLUGINS
	done
fi


##############################################
###  Clone gramps-example-reports/gh-pages
##############################################

mkdir -v -p gh-pages
git clone --depth=1 --branch=gh-pages https://github.com/$EXAMPLES_REPO_SLUG.git ./gh-pages

# Update gh-pages with master files
cp -r -f ./site/* ./gh-pages
