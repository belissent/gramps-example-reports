#!/bin/bash

# Get absolute current path
pushd $(dirname $0) > /dev/null
export MY_PATH=$(pwd -P)
popd > /dev/null


if [ "$OS" = "Windows_NT" ]
then
	export ENV_PATH=Scripts
	export PYTHON3_SUFFIX=
	export ENV_PYTHON3_VERSION=3
else
	export ENV_PATH=bin
	export PYTHON3_SUFFIX=3
	export ENV_PYTHON3_VERSION=python3
fi

if [ "$EXAMPLES_REPO_SLUG" = "" ]
then
	export EXAMPLES_REPO_SLUG=gramps-project/gramps-example-reports
	export GRAMPS_REPO_SLUG=gramps-project/gramps
	export ADDONS_REPO_SLUG=gramps-project/addons
fi

export VARS_50="export GRAMPSHOME=$MY_PATH/databases/dbgramps50"
export VARS_50="$VARS_50; export GRAMPS_RESOURCES=$MY_PATH/sources/gramps50"
export VARS_50="$VARS_50; export GRAMPS_REPORTS=$MY_PATH/site/gramps50"
export VARS_50="$VARS_50; export GRAMPS_ADDONS_SOURCE=$MY_PATH/sources/addons/gramps50"
export VARS_50="$VARS_50; export PYTHONPATH=$MY_PATH/sources/gramps50"
export VARS_50="$VARS_50; export LANG=en_US.UTF-8"
export VARS_50="$VARS_50; export LANGUAGE=en_US"

export ENV_50=$MY_PATH/env/gramps50/$ENV_PATH/activate
export PYTHON_50="python$PYTHON3_SUFFIX"
export PIP_50="pip$PYTHON3_SUFFIX"
export WORKON_50="eval $VARS_50; source $ENV_50"

export VARS_42=${VARS_50//gramps50/gramps42}
export ENV_42=$MY_PATH/env/gramps50/$ENV_PATH/activate
export PYTHON_42="python$PYTHON3_SUFFIX"
export PIP_42="pip$PYTHON3_SUFFIX"
export WORKON_42="eval $VARS_42; source $ENV_42"

# ifneq (${wildcard }(ICU_INSTALL_DIR)),)
	# export PIP_ICU_INCLUDE=--global-option=build_ext --global-option="-I$ICU_INSTALL_DIR/include"
# else
	# export PIP_ICU_INCLUDE=
# endif
