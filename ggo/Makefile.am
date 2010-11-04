## Process this file with automake to produce Makefile.in
## Created by Anjuta

SUBDIRS = src 

ggodocdir = ${prefix}/doc/ggo
ggodoc_DATA = \
	README\
	COPYING\
	AUTHORS\
	ChangeLog\
	INSTALL\
	NEWS


EXTRA_DIST = $(ggodoc_DATA)


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(ggodocdir)
