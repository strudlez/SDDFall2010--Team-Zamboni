## Process this file with automake to produce Makefile.in
## Created by Anjuta

SUBDIRS = data src 

zambogodocdir = ${prefix}/doc/zambogo
zambogodoc_DATA = \
	README\
	COPYING\
	AUTHORS\
	ChangeLog\
	INSTALL\
	NEWS


EXTRA_DIST = $(zambogodoc_DATA)


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(zambogodocdir)
