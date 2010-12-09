## Process this file with automake to produce Makefile.in
## Created by Anjuta

## The main script
SUBDIRS = engine sgf library review actors

bin_SCRIPTS = zambogoapp

## Directory where .class files will be installed
zambogodir = $(pythondir)/zambogo

zambogo_PYTHON = \
	__init__.py  \
	util.py \
	dirs.py \
	app.py

dirs.py: dirs.py.in
	sed -e "s|%pkgdatadir%|$(pkgdatadir)|" $< > $@