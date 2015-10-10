
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST))/..)
PYTHON_42=$(MAKEFILE_PATH)/env/gramps42/bin/python
PYTHON_50=$(MAKEFILE_PATH)/env/gramps50/bin/python
VARS50:=
VARS50:=$(VARS50) GRAMPSHOME=$(MAKEFILE_PATH)/databases/db50
VARS50:=$(VARS50) GRAMPS_RESOURCES=$(MAKEFILE_PATH)/sources/gramps50
VARS50:=$(VARS50) GRAMPS_REPORTS=$(MAKEFILE_PATH)/gramps50
VARS50:=$(VARS50) PYTHONPATH=$(MAKEFILE_PATH)/sources/gramps50
VARS50:=$(VARS50) LANG=en_US.UTF-8
VARS50:=$(VARS50) LANGUAGE=en_US
#SUDO=sudo
SUDO=


all: all42 all50

env: env42 env50

clone: clone42 clone50 clone_addons

copy_addons: copy_addons42 copy_addons50

run_reports.: run_reports42 run_reports50

clean:
	rm -rf env sources databases

############################################## 4.2

all42: env42 clone42 copy_addons run_reports42

env42:
	#todo

clone42: clone_addons
	# todo

copy_addons42:
	# todo

run_reports42:
	# todo

############################################## 5.0

all50: env50 clone50 copy_addons50 run_reports50

env50:
	if [ ! -d "env" ]; then mkdir env; fi
	if [ ! -d "env/gramps50" ]; then \
		virtualenv --system-site-packages --python=python3.4 env/gramps50; \
	fi

pip50:
	env/gramps50/bin/pip3 install Django==1.7
	env/gramps50/bin/pip3 install pyicu==1.8
	env/gramps50/bin/pip3 install cffi
	env/gramps50/bin/pip3 install cairosvg
	env/gramps50/bin/pip install Pillow

clone50:
	if [ ! -d "sources" ]; then mkdir sources; fi
	if [ ! -e "sources/gramps50/.gitignore" ]; then \
		git clone --depth=1 --branch=master git://github.com/gramps-project/gramps.git sources/gramps50; \
		cd sources/gramps50; $(PYTHON_50) setup.py build; \
	fi

copy_addons50: clone_addons
	if [ ! -d "databases/db50/gramps/gramps50/plugins" ]; then \
		mkdir -p databases/db50/gramps/gramps50/plugins; \
		for archive in `ls sources/addons/gramps50/download/*.tgz`; do \
			tar -xzf $$archive -C databases/db50/gramps/gramps50/plugins; \
		done; \
	fi

run_reports50: clone50 copy_addons50
	if [ ! -d "gramps50/gramps" ]; then mkdir -p gramps50/gramps; fi
	if [ ! -d "gramps50/addons" ]; then mkdir -p gramps50/addons; fi
	$(VARS50) $(PYTHON_50) run_reports50.py

############################################## Common

clone_addons: sources/addons/.gitignore
sources/addons/.gitignore:
	if [ ! -d "sources" ]; then mkdir sources; fi
	git clone --depth=1 --branch=master git://github.com/gramps-project/addons.git sources/addons
	touch sources/addons/.gitignore
