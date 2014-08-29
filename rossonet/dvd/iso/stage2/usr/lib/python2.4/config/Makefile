# Generated automatically from Makefile.pre by makesetup.
# Top-level Makefile for Python
#
# As distributed, this file is called Makefile.pre.in; it is processed
# into the real Makefile by running the script ./configure, which
# replaces things like @spam@ with values appropriate for your system.
# This means that if you edit Makefile, your changes get lost the next
# time you run the configure script.  Ideally, you can do:
#
#	./configure
#	make
#	make test
#	make install
#
# If you have a previous version of Python installed that you don't
# want to overwrite, you can use "make altinstall" instead of "make
# install".  Refer to the "Installing" section in the README file for
# additional details.
#
# See also the section "Build instructions" in the README file.

# === Variables set by makesetup ===

MODOBJS=          Modules/threadmodule.o  Modules/signalmodule.o  Modules/posixmodule.o  Modules/errnomodule.o  Modules/pwdmodule.o  Modules/_sre.o  Modules/_codecsmodule.o  Modules/zipimport.o  Modules/symtablemodule.o
MODLIBS=        $(LOCALMODLIBS) $(BASEMODLIBS)

# === Variables set by configure
VERSION=	2.4
srcdir=		.


CC=		gcc -pthread
CXX=		c++ -pthread
LINKCC=		gcc
AR=		ar
RANLIB=		ranlib

# Shell used by make (some versions default to the login shell, which is bad)
SHELL=		/bin/sh

# Use this to make a link between python$(VERSION) and python in $(BINDIR)
LN=		ln

# Portable install script (configure doesn't always guess right)
INSTALL=	/usr/bin/install -p -c
INSTALL_PROGRAM=${INSTALL}
INSTALL_SCRIPT= ${INSTALL}
INSTALL_DATA=	${INSTALL} -m 644
# Shared libraries must be installed with executable mode on some systems;
# rather than figuring out exactly which, we always give them executable mode.
# Also, making them read-only seems to be a good idea...
INSTALL_SHARED= ${INSTALL} -m 555

MAKESETUP=      $(srcdir)/Modules/makesetup

# Compiler options
OPT=		-DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m32 -march=i386 -mtune=generic -fasynchronous-unwind-tables -D_GNU_SOURCE -fPIC
BASECFLAGS=	 -fno-strict-aliasing
CFLAGS=		$(BASECFLAGS) $(OPT)
CPPFLAGS=	-I. -I$(srcdir)/Include
LDFLAGS=	 -L/usr/kerberos/lib  
LDLAST=		
SGI_ABI=	
CCSHARED=	-fPIC
LINKFORSHARED=	-Xlinker -export-dynamic
# Extra C flags added for building the interpreter object files.
CFLAGSFORSHARED=$(CCSHARED)
# C flags used for building the interpreter object files
PY_CFLAGS=	$(CFLAGS) $(CPPFLAGS) $(CFLAGSFORSHARED) -DPy_BUILD_CORE


# Machine-dependent subdirectories
MACHDEP=	linux2

# Install prefix for architecture-independent files
prefix=		/usr

# Install prefix for architecture-dependent files
exec_prefix=	/usr

# Expanded directories
BINDIR=		$(exec_prefix)/bin
LIBDIR=		$(exec_prefix)/lib
MANDIR=		/usr/share/man
INCLUDEDIR=	/usr/include
CONFINCLUDEDIR=	$(exec_prefix)/include
SCRIPTDIR=	$(prefix)/lib

# Detailed destination directories
BINLIBDEST=	$(LIBDIR)/python$(VERSION)
LIBDEST=	$(SCRIPTDIR)/python$(VERSION)
INCLUDEPY=	$(INCLUDEDIR)/python$(VERSION)
CONFINCLUDEPY=	$(CONFINCLUDEDIR)/python$(VERSION)
LIBP=		$(LIBDIR)/python$(VERSION)

# Symbols used for using shared libraries
SO=		.so
LDSHARED=	$(CC) -shared
BLDSHARED=	$(CC) -shared
DESTSHARED=	$(BINLIBDEST)/lib-dynload

# Executable suffix (.exe on Windows and Mac OS X)
EXE=		
BUILDEXE=	

# Short name and location for Mac OS X Python framework
PYTHONFRAMEWORK=	
PYTHONFRAMEWORKDIR=	no-framework
PYTHONFRAMEWORKPREFIX=	
PYTHONFRAMEWORKINSTALLDIR= 
# Deployment target selected during configure, to be checked
# by distutils
CONFIGURE_MACOSX_DEPLOYMENT_TARGET=
# Options to enable prebinding (for fast startup prior to Mac OS X 10.3)
OTHER_LIBTOOL_OPT=

# Environment to run shared python without installed libraries
RUNSHARED=       LD_LIBRARY_PATH=/builddir/build/BUILD/Python-2.4.3:

# Modes for directories, executables and data files created by the
# install process.  Default to user-only-writable for all file types.
DIRMODE=	755
EXEMODE=	755
FILEMODE=	644

# configure script arguments
CONFIG_ARGS=	'--build=i686-redhat-linux-gnu' '--host=i686-redhat-linux-gnu' '--target=i386-redhat-linux-gnu' '--program-prefix=' '--prefix=/usr' '--exec-prefix=/usr' '--bindir=/usr/bin' '--sbindir=/usr/sbin' '--sysconfdir=/etc' '--datadir=/usr/share' '--includedir=/usr/include' '--libdir=/usr/lib' '--libexecdir=/usr/libexec' '--localstatedir=/var' '--sharedstatedir=/usr/com' '--mandir=/usr/share/man' '--infodir=/usr/share/info' '--enable-ipv6' '--enable-unicode=ucs4' '--enable-shared' '--with-valgrind' '--with-system-expat' 'CC=gcc' 'CFLAGS=-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m32 -march=i386 -mtune=generic -fasynchronous-unwind-tables -D_GNU_SOURCE -fPIC -I/usr/kerberos/include  ' 'LDFLAGS= -L/usr/kerberos/lib  ' 'build_alias=i686-redhat-linux-gnu' 'host_alias=i686-redhat-linux-gnu' 'target_alias=i386-redhat-linux-gnu'


# Subdirectories with code
SRCDIRS= 	Parser Grammar Objects Python Modules Mac Mac/Python

# Other subdirectories
SUBDIRSTOO=	Include Lib Misc Demo

# Files and directories to be distributed
CONFIGFILES=	configure configure.in acconfig.h pyconfig.h.in Makefile.pre.in
DISTFILES=	README ChangeLog $(CONFIGFILES)
DISTDIRS=	$(SUBDIRS) $(SUBDIRSTOO) Ext-dummy
DIST=		$(DISTFILES) $(DISTDIRS)


LIBRARY=	libpython$(VERSION).a
LDLIBRARY=      libpython$(VERSION).so
BLDLIBRARY=     -L. -lpython$(VERSION)
DLLLIBRARY=	
LDLIBRARYDIR=   
INSTSONAME=	libpython$(VERSION).so.1.0


LIBS=		-lpthread -ldl  -lutil
LIBM=		-lm
LIBC=		
SYSLIBS=	$(LIBM) $(LIBC)
SHLIBS=		$(LIBS)

MAINOBJ=	python.o
THREADOBJ=	Python/thread.o
DLINCLDIR=	.
DYNLOADFILE=	dynload_shlib.o
MACHDEP_OBJS=	
UNICODE_OBJS=   Objects/unicodeobject.o Objects/unicodectype.o

PYTHON=		python$(EXE)
BUILDPYTHON=	python$(BUILDEXE)

# === Definitions added by makesetup ===

LOCALMODLIBS=         
BASEMODLIBS=
SHAREDMODS= Modules/readline$(SO) Modules/arraymodule$(SO) Modules/cmathmodule$(SO) Modules/mathmodule$(SO) Modules/structmodule$(SO) Modules/timemodule$(SO) Modules/operator$(SO) Modules/_weakref$(SO) Modules/_testcapimodule$(SO) Modules/_randommodule$(SO) Modules/collectionsmodule$(SO) Modules/itertoolsmodule$(SO) Modules/stropmodule$(SO) Modules/unicodedata$(SO) Modules/_localemodule$(SO) Modules/fcntlmodule$(SO) Modules/grpmodule$(SO) Modules/selectmodule$(SO) Modules/mmapmodule$(SO) Modules/_csv$(SO) Modules/_socketmodule$(SO) Modules/_ssl$(SO) Modules/cryptmodule$(SO) Modules/nismodule$(SO) Modules/termios$(SO) Modules/resource$(SO) Modules/audioop$(SO) Modules/imageop$(SO) Modules/rgbimgmodule$(SO) Modules/md5module$(SO) Modules/shamodule$(SO) Modules/linuxaudiodev$(SO) Modules/timingmodule$(SO) Modules/_tkinter$(SO) Modules/_cursesmodule$(SO) Modules/_curses_panel$(SO) Modules/dlmodule$(SO) Modules/gdbmmodule$(SO) Modules/_bsddb$(SO) Modules/binascii$(SO) Modules/parsermodule$(SO) Modules/cStringIO$(SO) Modules/cPickle$(SO) Modules/zlibmodule$(SO) Modules/_multibytecodecmodule$(SO) Modules/_codecs_cn$(SO) Modules/_codecs_hk$(SO) Modules/_codecs_iso2022$(SO) Modules/_codecs_jp$(SO) Modules/_codecs_kr$(SO) Modules/_codecs_tw$(SO) Modules/xxsubtype$(SO) Modules/shmmodule$(SO)
DBLIB=/usr/lib
DBINC=/usr/include/db4
DBLIBVER=4.3
SSL=/usr/local/ssl
GLHACK=-Dclear=__GLclear
PYTHONPATH=$(COREPYTHONPATH)
COREPYTHONPATH=$(DESTPATH)$(SITEPATH)$(TESTPATH)$(MACHDEPPATH)$(EXTRAMACHDEPPATH)$(TKPATH)
TKPATH=:lib-tk
EXTRAMACHDEPPATH=
MACHDEPPATH=:plat-$(MACHDEP)
TESTPATH=
SITEPATH=
DESTPATH=
MACHDESTLIB=$(BINLIBDEST)
DESTLIB=$(LIBDEST)



##########################################################################
# Modules
MODULE_OBJS=	\
		Modules/config.o \
		Modules/getpath.o \
		Modules/main.o \
		Modules/gcmodule.o

# Used of signalmodule.o is not available
SIGNAL_OBJS=	


##########################################################################
# Grammar
GRAMMAR_H=	$(srcdir)/Include/graminit.h
GRAMMAR_C=	$(srcdir)/Python/graminit.c
GRAMMAR_INPUT=	$(srcdir)/Grammar/Grammar


##########################################################################
# Parser
PGEN=		Parser/pgen$(EXE)

POBJS=		\
		Parser/acceler.o \
		Parser/grammar1.o \
		Parser/listnode.o \
		Parser/node.o \
		Parser/parser.o \
		Parser/parsetok.o \
		Parser/bitset.o \
		Parser/metagrammar.o \
		Parser/firstsets.o \
		Parser/grammar.o \
		Parser/pgen.o

PARSER_OBJS=	$(POBJS) Parser/myreadline.o Parser/tokenizer.o

PGOBJS=		\
		Objects/obmalloc.o \
		Python/mysnprintf.o \
		Parser/tokenizer_pgen.o \
		Parser/printgrammar.o \
		Parser/pgenmain.o

PGENOBJS=	$(PGENMAIN) $(POBJS) $(PGOBJS)


##########################################################################
# Python
PYTHON_OBJS=	\
		Python/bltinmodule.o \
		Python/exceptions.o \
		Python/ceval.o \
		Python/compile.o \
		Python/codecs.o \
		Python/errors.o \
		Python/frozen.o \
		Python/frozenmain.o \
		Python/future.o \
		Python/getargs.o \
		Python/getcompiler.o \
		Python/getcopyright.o \
		Python/getmtime.o \
		Python/getplatform.o \
		Python/getversion.o \
		Python/graminit.o \
		Python/import.o \
		Python/importdl.o \
		Python/marshal.o \
		Python/modsupport.o \
		Python/mystrtoul.o \
		Python/mysnprintf.o \
		Python/pyfpe.o \
		Python/pystate.o \
		Python/pythonrun.o \
		Python/structmember.o \
		Python/symtable.o \
		Python/sysmodule.o \
		Python/traceback.o \
		Python/getopt.o \
		Python/pystrtod.o \
		Python/$(DYNLOADFILE) \
		$(MACHDEP_OBJS) \
		$(THREADOBJ)


##########################################################################
# Objects
OBJECT_OBJS=	\
		Objects/abstract.o \
		Objects/boolobject.o \
		Objects/bufferobject.o \
		Objects/cellobject.o \
		Objects/classobject.o \
		Objects/cobject.o \
		Objects/complexobject.o \
		Objects/descrobject.o \
		Objects/enumobject.o \
		Objects/genobject.o \
		Objects/fileobject.o \
		Objects/floatobject.o \
		Objects/frameobject.o \
		Objects/funcobject.o \
		Objects/intobject.o \
		Objects/iterobject.o \
		Objects/listobject.o \
		Objects/longobject.o \
		Objects/dictobject.o \
		Objects/methodobject.o \
		Objects/moduleobject.o \
		Objects/object.o \
		Objects/obmalloc.o \
		Objects/rangeobject.o \
                Objects/setobject.o \
		Objects/sliceobject.o \
		Objects/stringobject.o \
		Objects/structseq.o \
		Objects/tupleobject.o \
		Objects/typeobject.o \
		Objects/weakrefobject.o \
		$(UNICODE_OBJS)


##########################################################################
# objects that get linked into the Python library
LIBRARY_OBJS=	\
		Modules/getbuildinfo.o \
		$(PARSER_OBJS) \
		$(OBJECT_OBJS) \
		$(PYTHON_OBJS) \
		$(MODULE_OBJS) \
		$(SIGNAL_OBJS) \
		$(MODOBJS)

#########################################################################
# Rules

# Default target
all:		$(BUILDPYTHON) oldsharedmods sharedmods

# Build the interpreter
$(BUILDPYTHON):	Modules/$(MAINOBJ) $(LIBRARY) $(LDLIBRARY)
		$(LINKCC) $(CFLAGS) $(LDFLAGS) $(LINKFORSHARED) -o $@ \
			Modules/$(MAINOBJ) \
			$(BLDLIBRARY) $(LIBS) $(MODLIBS) $(SYSLIBS) $(LDLAST)

platform: $(BUILDPYTHON)
	$(RUNSHARED) ./$(BUILDPYTHON) -E -c 'import sys ; from distutils.util import get_platform ; print get_platform()+"-"+sys.version[0:3]' >platform


# Build the shared modules
sharedmods: $(BUILDPYTHON)
	case $$MAKEFLAGS in \
	*-s*) $(RUNSHARED) CC='$(CC)' LDSHARED='$(BLDSHARED)' OPT='$(OPT)' ./$(BUILDPYTHON) -E $(srcdir)/setup.py -q build;; \
	*) $(RUNSHARED) CC='$(CC)' LDSHARED='$(BLDSHARED)' OPT='$(OPT)' ./$(BUILDPYTHON) -E $(srcdir)/setup.py build;; \
	esac

# buildno should really depend on something like LIBRARY_SRC
buildno: $(PARSER_OBJS) \
		$(OBJECT_OBJS) \
		$(PYTHON_OBJS) \
		$(MODULE_OBJS) \
		$(SIGNAL_OBJS) \
		$(MODOBJS) \
		$(srcdir)/Modules/getbuildinfo.c
	if test -f buildno; then \
		expr `cat buildno` + 1 >buildno1; \
		mv -f buildno1 buildno; \
	else echo 1 >buildno; fi

# Build static library
# avoid long command lines, same as LIBRARY_OBJS
$(LIBRARY): $(LIBRARY_OBJS)
	-rm -f $@
	$(AR) cr $@ Modules/getbuildinfo.o
	$(AR) cr $@ $(PARSER_OBJS)
	$(AR) cr $@ $(OBJECT_OBJS)
	$(AR) cr $@ $(PYTHON_OBJS)
	$(AR) cr $@ $(MODULE_OBJS) $(SIGNAL_OBJS)
	$(AR) cr $@ $(MODOBJS)
	$(RANLIB) $@

libpython$(VERSION).so: $(LIBRARY_OBJS)
	if test $(INSTSONAME) != $(LDLIBRARY); then \
		$(LDSHARED) -Wl,-h$(INSTSONAME) -o $(INSTSONAME) $(LIBRARY_OBJS) $(SHLIBS) $(LIBC) $(LIBM); \
		$(LN) -f $(INSTSONAME) $@; \
	else\
		$(LDSHARED) -o $@ $(LIBRARY_OBJS) $(SHLIBS) $(LIBC) $(LIBM); \
	fi

libpython$(VERSION).sl: $(LIBRARY_OBJS)
	$(LDSHARED) -o $@ $(LIBRARY_OBJS) $(LIBC) $(LIBM)

# This rule is here for OPENSTEP/Rhapsody/MacOSX. It builds a temporary
# minimal framework (not including the Lib directory and such) in the current
# directory.
RESSRCDIR=$(srcdir)/Mac/OSXResources/framework
$(PYTHONFRAMEWORKDIR)/Versions/$(VERSION)/$(PYTHONFRAMEWORK): \
		$(LIBRARY) \
		$(RESSRCDIR)/Info.plist \
                $(RESSRCDIR)/version.plist \
                $(RESSRCDIR)/English.lproj/InfoPlist.strings
	$(INSTALL) -d -m $(DIRMODE) $(PYTHONFRAMEWORKDIR)/Versions/$(VERSION)
	libtool -o $(LDLIBRARY) -dynamic $(OTHER_LIBTOOL_OPT) $(LIBRARY) \
		
	$(INSTALL) -d -m $(DIRMODE)  \
		$(PYTHONFRAMEWORKDIR)/Versions/$(VERSION)/Resources/English.lproj
	$(INSTALL_DATA) $(RESSRCDIR)/Info.plist \
		$(PYTHONFRAMEWORKDIR)/Versions/$(VERSION)/Resources/Info.plist
	$(INSTALL_DATA) $(RESSRCDIR)/version.plist \
		$(PYTHONFRAMEWORKDIR)/Versions/$(VERSION)/Resources/version.plist
	$(INSTALL_DATA) $(RESSRCDIR)/English.lproj/InfoPlist.strings \
		$(PYTHONFRAMEWORKDIR)/Versions/$(VERSION)/Resources/English.lproj/InfoPlist.strings
	$(LN) -fsn $(VERSION) $(PYTHONFRAMEWORKDIR)/Versions/Current
	$(LN) -fsn Versions/Current/$(PYTHONFRAMEWORK) $(PYTHONFRAMEWORKDIR)/$(PYTHONFRAMEWORK)
	$(LN) -fsn Versions/Current/Headers $(PYTHONFRAMEWORKDIR)/Headers
	$(LN) -fsn Versions/Current/Resources $(PYTHONFRAMEWORKDIR)/Resources

# This rule builds the Cygwin Python DLL and import library if configured
# for a shared core library; otherwise, this rule is a noop.
$(DLLLIBRARY) libpython$(VERSION).dll.a: $(LIBRARY_OBJS)
	if test -n "$(DLLLIBRARY)"; then \
		$(LDSHARED) -Wl,--out-implib=$@ -o $(DLLLIBRARY) $^ \
			$(LIBS) $(MODLIBS) $(SYSLIBS); \
	else true; \
	fi


oldsharedmods: $(SHAREDMODS)


Makefile Modules/config.c: Makefile.pre \
				$(srcdir)/Modules/config.c.in \
				$(MAKESETUP) \
				Modules/Setup.config \
				Modules/Setup \
				Modules/Setup.local
	$(SHELL) $(MAKESETUP) -c $(srcdir)/Modules/config.c.in \
				-s Modules \
				Modules/Setup.config \
				Modules/Setup.local \
				Modules/Setup
	@mv config.c Modules
	@echo "The Makefile was updated, you may need to re-run make."


Modules/Setup: $(srcdir)/Modules/Setup.dist
	@if test -f Modules/Setup; then \
		echo "-----------------------------------------------"; \
		echo "Modules/Setup.dist is newer than Modules/Setup;"; \
		echo "check to make sure you have all the updates you"; \
		echo "need in your Modules/Setup file."; \
		echo "Usually, copying Setup.dist to Setup will work."; \
		echo "-----------------------------------------------"; \
	fi

############################################################################
# Special rules for object files

Modules/getbuildinfo.o: $(srcdir)/Modules/getbuildinfo.c buildno
	$(CC) -c $(PY_CFLAGS) -DBUILD=`cat buildno` -o $@ $(srcdir)/Modules/getbuildinfo.c

Modules/getpath.o: $(srcdir)/Modules/getpath.c Makefile
	$(CC) -c $(PY_CFLAGS) -DPYTHONPATH='"$(PYTHONPATH)"' \
		-DPREFIX='"$(prefix)"' \
		-DEXEC_PREFIX='"$(exec_prefix)"' \
		-DVERSION='"$(VERSION)"' \
		-DVPATH='"$(VPATH)"' \
		-o $@ $(srcdir)/Modules/getpath.c

Modules/ccpython.o: $(srcdir)/Modules/ccpython.cc
	$(CXX) -c $(PY_CFLAGS) -o $@ $(srcdir)/Modules/ccpython.cc


$(GRAMMAR_H) $(GRAMMAR_C): $(PGEN) $(GRAMMAR_INPUT)
		-$(PGEN) $(GRAMMAR_INPUT) $(GRAMMAR_H) $(GRAMMAR_C)

$(PGEN):	$(PGENOBJS)
		$(CC) $(OPT) $(LDFLAGS) $(PGENOBJS) $(LIBS) -o $(PGEN)

Parser/grammar.o:	$(srcdir)/Parser/grammar.c \
				$(srcdir)/Include/token.h \
				$(srcdir)/Include/grammar.h
Parser/metagrammar.o:	$(srcdir)/Parser/metagrammar.c

Parser/tokenizer_pgen.o:	$(srcdir)/Parser/tokenizer.c


Python/compile.o Python/symtable.o: $(GRAMMAR_H)

Python/getplatform.o: $(srcdir)/Python/getplatform.c
		$(CC) -c $(PY_CFLAGS) -DPLATFORM='"$(MACHDEP)"' -o $@ $(srcdir)/Python/getplatform.c

Python/importdl.o: $(srcdir)/Python/importdl.c
		$(CC) -c $(PY_CFLAGS) -I$(DLINCLDIR) -o $@ $(srcdir)/Python/importdl.c

Objects/unicodectype.o:	$(srcdir)/Objects/unicodectype.c \
				$(srcdir)/Objects/unicodetype_db.h

############################################################################
# Header files

PYTHON_HEADERS= \
		Include/Python.h \
		Include/abstract.h \
		Include/boolobject.h \
		Include/bufferobject.h \
		Include/ceval.h \
		Include/classobject.h \
		Include/cobject.h \
		Include/codecs.h \
		Include/compile.h \
		Include/complexobject.h \
		Include/descrobject.h \
		Include/dictobject.h \
		Include/enumobject.h \
		Include/genobject.h \
		Include/fileobject.h \
		Include/floatobject.h \
		Include/funcobject.h \
		Include/import.h \
		Include/intobject.h \
		Include/intrcheck.h \
		Include/iterobject.h \
		Include/listobject.h \
		Include/longobject.h \
		Include/methodobject.h \
		Include/modsupport.h \
		Include/moduleobject.h \
		Include/object.h \
		Include/objimpl.h \
		Include/patchlevel.h \
		Include/pydebug.h \
		Include/pyerrors.h \
		Include/pyfpe.h \
		Include/pymem.h \
		Include/pyport.h \
		Include/pystate.h \
		Include/pythonrun.h \
		Include/rangeobject.h \
                Include/setobject.h \
		Include/sliceobject.h \
		Include/stringobject.h \
		Include/structseq.h \
		Include/structmember.h \
		Include/symtable.h \
		Include/sysmodule.h \
		Include/traceback.h \
		Include/tupleobject.h \
		Include/unicodeobject.h \
		Include/weakrefobject.h \
		pyconfig.h

$(LIBRARY_OBJS) $(MODOBJS) Modules/$(MAINOBJ): $(PYTHON_HEADERS)


######################################################################

# Test the interpreter (twice, once without .pyc files, once with)
# In the past, we've had problems where bugs in the marshalling or
# elsewhere caused bytecode read from .pyc files to behave differently
# than bytecode generated directly from a .py source file.  Sometimes
# the bytecode read from a .pyc file had the bug, somtimes the directly
# generated bytecode.  This is sometimes a very shy bug needing a lot of
# sample data.

TESTOPTS=	-l $(EXTRATESTOPTS)
TESTPROG=	$(srcdir)/Lib/test/regrtest.py
TESTPYTHON=	$(RUNSHARED) ./$(BUILDPYTHON) -E -tt
test:		all platform
		-find $(srcdir)/Lib -name '*.py[co]' -print | xargs rm -f
		-$(TESTPYTHON) $(TESTPROG) $(TESTOPTS)
		$(TESTPYTHON) $(TESTPROG) $(TESTOPTS)

testall:	all platform
		-find $(srcdir)/Lib -name '*.py[co]' -print | xargs rm -f
		-$(TESTPYTHON) $(TESTPROG) $(TESTOPTS) -uall
		$(TESTPYTHON) $(TESTPROG) $(TESTOPTS) -uall

# Like testall, but with a single pass only
buildbottest:	all platform
		$(TESTPYTHON) $(TESTPROG) $(TESTOPTS) -uall -rw

QUICKTESTOPTS=	$(TESTOPTS) -x test_thread test_signal test_strftime \
		test_unicodedata test_re test_sre test_select test_poll \
		test_linuxaudiodev test_struct test_sunaudiodev test_zlib
quicktest:	all platform
		-find $(srcdir)/Lib -name '*.py[co]' -print | xargs rm -f
		-$(TESTPYTHON) $(TESTPROG) $(QUICKTESTOPTS)
		$(TESTPYTHON) $(TESTPROG) $(QUICKTESTOPTS)

MEMTESTOPTS=    $(QUICKTESTOPTS) -x test_dl test___all__ test_fork1 \
		test_longexp
memtest:	all platform
		-rm -f $(srcdir)/Lib/test/*.py[co]
		-$(TESTPYTHON) $(TESTPROG) $(MEMTESTOPTS)
		$(TESTPYTHON) $(TESTPROG) $(MEMTESTOPTS)

# Install everything
install:	altinstall bininstall maninstall

# Install almost everything without disturbing previous versions
altinstall:	altbininstall libinstall inclinstall libainstall \
                sharedinstall oldsharedinstall

# Install shared libraries enabled by Setup
DESTDIRS=	$(exec_prefix) $(LIBDIR) $(BINLIBDEST) $(DESTSHARED)

oldsharedinstall: $(DESTSHARED) $(SHAREDMODS)
		@for i in X $(SHAREDMODS); do \
		  if test $$i != X; then \
		    echo $(INSTALL_SHARED) $$i $(DESTSHARED)/`basename $$i`; \
		    $(INSTALL_SHARED) $$i $(DESTDIR)$(DESTSHARED)/`basename $$i`; \
		  fi; \
		done

$(DESTSHARED):
		@for i in $(DESTDIRS); \
		do \
			if test ! -d $(DESTDIR)$$i; then \
				echo "Creating directory $$i"; \
				$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$i; \
			else    true; \
			fi; \
		done


# Install the interpreter (by creating a hard link to python$(VERSION))
bininstall:	altbininstall
	-if test -f $(DESTDIR)$(BINDIR)/$(PYTHON) -o -h $(DESTDIR)$(BINDIR)/$(PYTHON); \
	then rm -f $(DESTDIR)$(BINDIR)/$(PYTHON); \
	else true; \
	fi
	(cd $(DESTDIR)$(BINDIR); $(LN) python$(VERSION)$(EXE) $(PYTHON))

# Install the interpreter with $(VERSION) affixed
# This goes into $(exec_prefix)
altbininstall:	$(BUILDPYTHON)
	@if test "$(PYTHONFRAMEWORKDIR)" != no-framework; then \
		if test ! -f $(DESTDIR)$(PYTHONFRAMEWORKINSTALLDIR)/Versions/Current/Resources/Info.plist; then \
			echo 'Framework build: use "make frameworkinstall" in stead of "make install"'; \
			exit 1; \
		fi; \
	fi
	@for i in $(BINDIR) $(LIBDIR); \
	do \
		if test ! -d $(DESTDIR)$$i; then \
			echo "Creating directory $$i"; \
			$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$i; \
		else	true; \
		fi; \
	done
	$(INSTALL_PROGRAM) $(BUILDPYTHON) $(DESTDIR)$(BINDIR)/python$(VERSION)$(EXE)
	if test -f libpython$(VERSION)$(SO); then \
		if test "$(SO)" = .dll; then \
			$(INSTALL_SHARED) libpython$(VERSION)$(SO) $(DESTDIR)$(BINDIR); \
		else \
			$(INSTALL_SHARED) libpython$(VERSION)$(SO) $(DESTDIR)$(LIBDIR)/$(INSTSONAME); \
			if test libpython$(VERSION)$(SO) != $(INSTSONAME); then \
				(cd $(DESTDIR)$(LIBDIR); $(LN) -sf $(INSTSONAME) libpython$(VERSION)$(SO)); \
			fi \
		fi; \
	else	true; \
	fi

# Install the manual page
maninstall:
	@for i in $(MANDIR) $(MANDIR)/man1; \
	do \
		if test ! -d $(DESTDIR)$$i; then \
			echo "Creating directory $$i"; \
			$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$i; \
		else	true; \
		fi; \
	done
	$(INSTALL_DATA) $(srcdir)/Misc/python.man \
		$(DESTDIR)$(MANDIR)/man1/python.1

# Install the library
PLATDIR=	plat-$(MACHDEP)
EXTRAPLATDIR= 
EXTRAMACHDEPPATH=
MACHDEPS=	$(PLATDIR) $(EXTRAPLATDIR)
XMLLIBSUBDIRS=  xml xml/dom xml/parsers xml/sax
PLATMACDIRS= plat-mac plat-mac/Carbon plat-mac/lib-scriptpackages \
	plat-mac/lib-scriptpackages/_builtinSuites \
	plat-mac/lib-scriptpackages/CodeWarrior \
	plat-mac/lib-scriptpackages/Explorer \
	plat-mac/lib-scriptpackages/Finder \
	plat-mac/lib-scriptpackages/Netscape \
	plat-mac/lib-scriptpackages/StdSuites \
	plat-mac/lib-scriptpackages/SystemEvents \
	plat-mac/lib-scriptpackages/Terminal
PLATMACPATH=:plat-mac:plat-mac/lib-scriptpackages
LIBSUBDIRS=	lib-old lib-tk site-packages test test/output test/data \
		test/decimaltestdata \
		encodings email email/test email/test/data compiler hotshot \
		logging bsddb bsddb/test csv idlelib idlelib/Icons \
		distutils distutils/command distutils/tests $(XMLLIBSUBDIRS) \
		curses $(MACHDEPS)
libinstall:	$(BUILDPYTHON) $(srcdir)/Lib/$(PLATDIR)
	@for i in $(SCRIPTDIR) $(LIBDEST); \
	do \
		if test ! -d $(DESTDIR)$$i; then \
			echo "Creating directory $$i"; \
			$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$i; \
		else	true; \
		fi; \
	done
	@for d in $(LIBSUBDIRS); \
	do \
		a=$(srcdir)/Lib/$$d; \
		if test ! -d $$a; then continue; else true; fi; \
		b=$(LIBDEST)/$$d; \
		if test ! -d $(DESTDIR)$$b; then \
			echo "Creating directory $$b"; \
			$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$b; \
		else	true; \
		fi; \
	done
	@for i in $(srcdir)/Lib/*.py $(srcdir)/Lib/*.doc; \
	do \
		if test -x $$i; then \
			$(INSTALL_SCRIPT) $$i $(DESTDIR)$(LIBDEST); \
			echo $(INSTALL_SCRIPT) $$i $(LIBDEST); \
		else \
			$(INSTALL_DATA) $$i $(DESTDIR)$(LIBDEST); \
			echo $(INSTALL_DATA) $$i $(LIBDEST); \
		fi; \
	done
	@for d in $(LIBSUBDIRS); \
	do \
		a=$(srcdir)/Lib/$$d; \
		if test ! -d $$a; then continue; else true; fi; \
		b=$(LIBDEST)/$$d; \
		for i in $$a/*; \
		do \
			case $$i in \
			*CVS) ;; \
			*.py[co]) ;; \
			*.orig) ;; \
			*~) ;; \
			*) \
				if test -d $$i; then continue; fi; \
				if test -x $$i; then \
				    echo $(INSTALL_SCRIPT) $$i $$b; \
				    $(INSTALL_SCRIPT) $$i $(DESTDIR)$$b; \
				else \
				    echo $(INSTALL_DATA) $$i $$b; \
				    $(INSTALL_DATA) $$i $(DESTDIR)$$b; \
				fi;; \
			esac; \
		done; \
	done
	$(INSTALL_DATA) $(srcdir)/LICENSE $(DESTDIR)$(LIBDEST)/LICENSE.txt
	PYTHONPATH=$(DESTDIR)$(LIBDEST)  $(RUNSHARED) \
		./$(BUILDPYTHON) -Wi -tt $(DESTDIR)$(LIBDEST)/compileall.py \
		-d $(LIBDEST) -f \
		-x 'badsyntax|site-packages' $(DESTDIR)$(LIBDEST)
	PYTHONPATH=$(DESTDIR)$(LIBDEST) $(RUNSHARED) \
		./$(BUILDPYTHON) -Wi -tt -O $(DESTDIR)$(LIBDEST)/compileall.py \
		-d $(LIBDEST) -f \
		-x 'badsyntax|site-packages' $(DESTDIR)$(LIBDEST)
	-PYTHONPATH=$(DESTDIR)$(LIBDEST)  $(RUNSHARED) \
		./$(BUILDPYTHON) -Wi -t $(DESTDIR)$(LIBDEST)/compileall.py \
		-d $(LIBDEST)/site-packages -f \
		-x badsyntax $(DESTDIR)$(LIBDEST)/site-packages
	-PYTHONPATH=$(DESTDIR)$(LIBDEST) $(RUNSHARED) \
		./$(BUILDPYTHON) -Wi -t -O $(DESTDIR)$(LIBDEST)/compileall.py \
		-d $(LIBDEST)/site-packages -f \
		-x badsyntax $(DESTDIR)$(LIBDEST)/site-packages

# Create the PLATDIR source directory, if one wasn't distributed..
$(srcdir)/Lib/$(PLATDIR):
	mkdir $(srcdir)/Lib/$(PLATDIR)
	cp $(srcdir)/Lib/plat-generic/regen $(srcdir)/Lib/$(PLATDIR)/regen
	export PATH; PATH="`pwd`:$$PATH"; \
	export PYTHONPATH; PYTHONPATH="`pwd`/Lib"; \
	export DYLD_FRAMEWORK_PATH; DYLD_FRAMEWORK_PATH="`pwd`"; \
	export EXE; EXE="$(BUILDEXE)"; \
	cd $(srcdir)/Lib/$(PLATDIR); ./regen

# Install the include files
INCLDIRSTOMAKE=$(INCLUDEDIR) $(CONFINCLUDEDIR) $(INCLUDEPY) $(CONFINCLUDEPY)
inclinstall:
	@for i in $(INCLDIRSTOMAKE); \
	do \
		if test ! -d $(DESTDIR)$$i; then \
			echo "Creating directory $$i"; \
			$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$i; \
		else	true; \
		fi; \
	done
	@for i in $(srcdir)/Include/*.h; \
	do \
		echo $(INSTALL_DATA) $$i $(INCLUDEPY); \
		$(INSTALL_DATA) $$i $(DESTDIR)$(INCLUDEPY); \
	done
	$(INSTALL_DATA) pyconfig.h $(DESTDIR)$(CONFINCLUDEPY)/pyconfig.h

# Install the library and miscellaneous stuff needed for extending/embedding
# This goes into $(exec_prefix)
LIBPL=		$(LIBP)/config
libainstall:	all
	@for i in $(LIBDIR) $(LIBP) $(LIBPL); \
	do \
		if test ! -d $(DESTDIR)$$i; then \
			echo "Creating directory $$i"; \
			$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$i; \
		else	true; \
		fi; \
	done
	@if test -d $(LIBRARY); then :; else \
		if test "$(PYTHONFRAMEWORKDIR)" = no-framework; then \
			if test "$(SO)" = .dll; then \
				$(INSTALL_DATA) $(LDLIBRARY) $(DESTDIR)$(LIBPL) ; \
			else \
				$(INSTALL_DATA) $(LIBRARY) $(DESTDIR)$(LIBPL)/$(LIBRARY) ; \
				$(RANLIB) $(DESTDIR)$(LIBPL)/$(LIBRARY) ; \
			fi; \
		else \
			echo Skip install of $(LIBRARY) - use make frameworkinstall; \
		fi; \
	fi
	$(INSTALL_DATA) Modules/config.c $(DESTDIR)$(LIBPL)/config.c
	$(INSTALL_DATA) Modules/$(MAINOBJ) $(DESTDIR)$(LIBPL)/$(MAINOBJ)
	$(INSTALL_DATA) $(srcdir)/Modules/config.c.in $(DESTDIR)$(LIBPL)/config.c.in
	$(INSTALL_DATA) Makefile $(DESTDIR)$(LIBPL)/Makefile
	$(INSTALL_DATA) Modules/Setup $(DESTDIR)$(LIBPL)/Setup
	$(INSTALL_DATA) Modules/Setup.local $(DESTDIR)$(LIBPL)/Setup.local
	$(INSTALL_DATA) Modules/Setup.config $(DESTDIR)$(LIBPL)/Setup.config
	$(INSTALL_SCRIPT) $(srcdir)/Modules/makesetup $(DESTDIR)$(LIBPL)/makesetup
	$(INSTALL_SCRIPT) $(srcdir)/install-sh $(DESTDIR)$(LIBPL)/install-sh
	@if [ -s Modules/python.exp -a \
		"`echo $(MACHDEP) | sed 's/^\(...\).*/\1/'`" = "aix" ]; then \
		echo; echo "Installing support files for building shared extension modules on AIX:"; \
		$(INSTALL_DATA) Modules/python.exp		\
				$(DESTDIR)$(LIBPL)/python.exp;		\
		echo; echo "$(LIBPL)/python.exp";		\
		$(INSTALL_SCRIPT) $(srcdir)/Modules/makexp_aix	\
				$(DESTDIR)$(LIBPL)/makexp_aix;		\
		echo "$(LIBPL)/makexp_aix";			\
		$(INSTALL_SCRIPT) $(srcdir)/Modules/ld_so_aix	\
				$(DESTDIR)$(LIBPL)/ld_so_aix;		\
		echo "$(LIBPL)/ld_so_aix";			\
		echo; echo "See Misc/AIX-NOTES for details.";	\
	else true; \
	fi
	@case "$(MACHDEP)" in beos*) \
		echo; echo "Installing support files for building shared extension modules on BeOS:"; \
		$(INSTALL_DATA) Misc/BeOS-NOTES $(DESTDIR)$(LIBPL)/README;	\
		echo; echo "$(LIBPL)/README";			\
		$(INSTALL_SCRIPT) Modules/ar_beos $(DESTDIR)$(LIBPL)/ar_beos; \
		echo "$(LIBPL)/ar_beos";			\
		$(INSTALL_SCRIPT) Modules/ld_so_beos $(DESTDIR)$(LIBPL)/ld_so_beos; \
		echo "$(LIBPL)/ld_so_beos";			\
		echo; echo "See Misc/BeOS-NOTES for details.";	\
		;; \
	esac

# Install the dynamically loadable modules
# This goes into $(exec_prefix)
sharedinstall:
	$(RUNSHARED) ./$(BUILDPYTHON) -E $(srcdir)/setup.py install \
	   	--prefix=$(prefix) \
		--install-scripts=$(BINDIR) \
		--install-platlib=$(DESTSHARED) \
		--root=/$(DESTDIR)

# Here are a couple of targets for MacOSX again, to install a full
# framework-based Python. frameworkinstall installs everything, the
# subtargets install specific parts. Much of the actual work is offloaded to
# the Makefile in Mac/OSX
#
frameworkinstall: frameworkinstallframework \
	frameworkinstallapps frameworkinstallunixtools

# On install, we re-make the framework
# structure in the install location, /Library/Frameworks/ or the argument to
# --enable-framework. If --enable-framework has been specified then we have
# automatically set prefix to the location deep down in the framework, so we
# only have to cater for the structural bits of the framework.

frameworkinstallframework: frameworkinstallstructure install frameworkinstallmaclib

frameworkinstallstructure:	$(LDLIBRARY)
	@if test "$(PYTHONFRAMEWORKDIR)" = no-framework; then \
		echo Not configured with --enable-framework; \
		exit 1; \
	else true; \
	fi
	@for i in $(prefix)/Resources/English.lproj $(prefix)/lib; do\
		if test ! -d $(DESTDIR)$$i; then \
			echo "Creating directory $(DESTDIR)$$i"; \
			$(INSTALL) -d -m $(DIRMODE) $(DESTDIR)$$i; \
		else	true; \
		fi; \
	done
	$(LN) -fsn include/python$(VERSION) $(DESTDIR)$(prefix)/Headers
	$(INSTALL_DATA) $(RESSRCDIR)/Info.plist $(DESTDIR)$(prefix)/Resources/Info.plist
	$(INSTALL_DATA) $(RESSRCDIR)/version.plist $(DESTDIR)$(prefix)/Resources/version.plist
	$(INSTALL_DATA) $(RESSRCDIR)/English.lproj/InfoPlist.strings \
		$(DESTDIR)$(prefix)/Resources/English.lproj/InfoPlist.strings
	$(LN) -fsn $(VERSION) $(DESTDIR)$(PYTHONFRAMEWORKINSTALLDIR)/Versions/Current
	$(LN) -fsn Versions/Current/Python $(DESTDIR)$(PYTHONFRAMEWORKINSTALLDIR)/Python
	$(LN) -fsn Versions/Current/Headers $(DESTDIR)$(PYTHONFRAMEWORKINSTALLDIR)/Headers
	$(LN) -fsn Versions/Current/Resources $(DESTDIR)$(PYTHONFRAMEWORKINSTALLDIR)/Resources
	$(INSTALL_SHARED) $(LDLIBRARY) $(DESTDIR)$(PYTHONFRAMEWORKPREFIX)/$(LDLIBRARY)

# This installs Mac/Lib into the framework
frameworkinstallmaclib:
	$(MAKE) -f $(srcdir)/Mac/OSX/Makefile installmacsubtree \
		$(RUNSHARED) BUILDPYTHON=./$(BUILDPYTHON) DIRMODE=$(DIRMODE) FILEMODE=$(FILEMODE) \
		srcdir=$(srcdir) builddir=. prefix=$(prefix) LIBDEST=$(LIBDEST) \
		DESTDIR=$(DESTDIR)

# This installs the IDE, the Launcher and other apps into /Applications
frameworkinstallapps:
	$(MAKE) -f $(srcdir)/Mac/OSX/Makefile installapps \
		$(RUNSHARED) BUILDPYTHON=./$(BUILDPYTHON) DIRMODE=$(DIRMODE) FILEMODE=$(FILEMODE) \
		srcdir=$(srcdir) builddir=. DESTDIR=$(DESTDIR) prefix=$(prefix)

# This install the unix python and pythonw tools in /usr/local/bin
frameworkinstallunixtools:
	$(MAKE) -f $(srcdir)/Mac/OSX/Makefile installunixtools \
		DIRMODE=$(DIRMODE) FILEMODE=$(FILEMODE) \
		srcdir=$(srcdir) builddir=. DESTDIR=$(DESTDIR) prefix=$(prefix)

# This installs the Demos and Tools into the applications directory.
# It is not part of a normal frameworkinstall
frameworkinstallextras:
	$(MAKE) -f $(srcdir)/Mac/OSX/Makefile installextras \
		$(RUNSHARED) BUILDPYTHON=./$(BUILDPYTHON) DIRMODE=$(DIRMODE) FILEMODE=$(FILEMODE) \
		srcdir=$(srcdir) builddir=. DESTDIR=$(DESTDIR)

# This installs a few of the useful scripts in Tools/scripts
scriptsinstall:
	SRCDIR=$(srcdir) $(RUNSHARED) \
	./$(BUILDPYTHON) $(srcdir)/Tools/scripts/setup.py install \
	--prefix=$(prefix) \
	--install-scripts=$(BINDIR) \
	--root=/$(DESTDIR)

# Build the toplevel Makefile
Makefile.pre: Makefile.pre.in config.status
	CONFIG_FILES=Makefile.pre CONFIG_HEADERS= $(SHELL) config.status
	$(MAKE) -f Makefile.pre Makefile

# Run the configure script.
config.status:	$(srcdir)/configure
	$(SHELL) $(srcdir)/configure $(CONFIG_ARGS)

.PRECIOUS: config.status $(BUILDPYTHON) Makefile Makefile.pre

# Some make's put the object file in the current directory
.c.o:
	$(CC) -c $(PY_CFLAGS) -o $@ $<

# Rerun configure with the same options as it was run last time,
# provided the config.status script exists
recheck:
	$(SHELL) config.status --recheck
	$(SHELL) config.status

# Rebuild the configure script from configure.in; also rebuild pyconfig.h.in
autoconf:
	(cd $(srcdir); autoconf)
	(cd $(srcdir); autoheader)

# Create a tags file for vi
tags::
	cd $(srcdir); \
	ctags -w -t Include/*.h; \
	for i in $(SRCDIRS); do ctags -w -t -a $$i/*.[ch]; \
	done; \
	sort -o tags tags

# Create a tags file for GNU Emacs
TAGS::
	cd $(srcdir); \
	etags Include/*.h; \
	for i in $(SRCDIRS); do etags -a $$i/*.[ch]; done

# Sanitation targets -- clean leaves libraries, executables and tags
# files, which clobber removes those as well

clean:
	find . -name '*.o' -exec rm -f {} ';'
	find . -name '*.s[ol]' -exec rm -f {} ';'
	find $(srcdir) -name '*.py[co]' -exec rm -f {} ';'

clobber: clean
	-rm -f $(BUILDPYTHON) $(PGEN) $(LIBRARY) $(LDLIBRARY) $(DLLLIBRARY) \
		tags TAGS \
		config.cache config.log pyconfig.h Modules/config.c
	-rm -rf build platform
	-rm -rf $(PYTHONFRAMEWORKDIR)

# Make things extra clean, before making a distribution:
# remove all generated files, even Makefile[.pre]
distclean: clobber
	-rm -f core Makefile Makefile.pre buildno config.status \
		Modules/Setup Modules/Setup.local Modules/Setup.config
	find $(srcdir) '(' -name '*.fdc' -o -name '*~' \
			   -o -name '[@,#]*' -o -name '*.old' \
			   -o -name '*.orig' -o -name '*.rej' \
			   -o -name '*.bak' ')' \
			   -exec rm -f {} ';'

# Check for smelly exported symbols (not starting with Py/_Py)
smelly: all
	nm -p $(LIBRARY) | \
		sed -n "/ [TDB] /s/.* //p" | grep -v "^_*Py" | sort -u; \

# Find files with funny names
funny:
	find $(DISTDIRS) -type d \
		-o -name '*.[chs]' \
		-o -name '*.py' \
		-o -name '*.doc' \
		-o -name '*.sty' \
		-o -name '*.bib' \
		-o -name '*.dat' \
		-o -name '*.el' \
		-o -name '*.fd' \
		-o -name '*.in' \
		-o -name '*.tex' \
		-o -name '*,[vpt]' \
		-o -name 'Setup' \
		-o -name 'Setup.*' \
		-o -name README \
		-o -name Makefile \
		-o -name ChangeLog \
		-o -name Repository \
		-o -name Root \
		-o -name Entries \
		-o -name Tag \
		-o -name tags \
		-o -name TAGS \
		-o -name .cvsignore \
		-o -name MANIFEST \
		-o -print

# Dependencies

Python/thread.o:  $(srcdir)/Python/thread_atheos.h $(srcdir)/Python/thread_beos.h $(srcdir)/Python/thread_cthread.h $(srcdir)/Python/thread_foobar.h $(srcdir)/Python/thread_lwp.h $(srcdir)/Python/thread_nt.h $(srcdir)/Python/thread_os2.h $(srcdir)/Python/thread_pth.h $(srcdir)/Python/thread_pthread.h $(srcdir)/Python/thread_sgi.h $(srcdir)/Python/thread_solaris.h $(srcdir)/Python/thread_wince.h

# Declare targets that aren't real files
.PHONY: all sharedmods oldsharedmods test quicktest memtest
.PHONY: install altinstall oldsharedinstall bininstall altbininstall
.PHONY: maninstall libinstall inclinstall libainstall sharedinstall
.PHONY: frameworkinstall frameworkinstallframework frameworkinstallstructure
.PHONY: frameworkinstallmaclib frameworkinstallapps frameworkinstallunixtools
.PHONY: recheck autoconf clean clobber distclean smelly funny

# IF YOU PUT ANYTHING HERE IT WILL GO AWAY

# Rules appended by makedepend

Modules/threadmodule.o: $(srcdir)/Modules/threadmodule.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/threadmodule.c -o Modules/threadmodule.o
Modules/threadmodule$(SO):  Modules/threadmodule.o; $(LDSHARED)  Modules/threadmodule.o   -o Modules/threadmodule$(SO)
Modules/signalmodule.o: $(srcdir)/Modules/signalmodule.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/signalmodule.c -o Modules/signalmodule.o
Modules/signalmodule$(SO):  Modules/signalmodule.o; $(LDSHARED)  Modules/signalmodule.o   -o Modules/signalmodule$(SO)
Modules/posixmodule.o: $(srcdir)/Modules/posixmodule.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/posixmodule.c -o Modules/posixmodule.o
Modules/posixmodule$(SO):  Modules/posixmodule.o; $(LDSHARED)  Modules/posixmodule.o   -o Modules/posixmodule$(SO)
Modules/errnomodule.o: $(srcdir)/Modules/errnomodule.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/errnomodule.c -o Modules/errnomodule.o
Modules/errnomodule$(SO):  Modules/errnomodule.o; $(LDSHARED)  Modules/errnomodule.o   -o Modules/errnomodule$(SO)
Modules/pwdmodule.o: $(srcdir)/Modules/pwdmodule.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/pwdmodule.c -o Modules/pwdmodule.o
Modules/pwdmodule$(SO):  Modules/pwdmodule.o; $(LDSHARED)  Modules/pwdmodule.o   -o Modules/pwdmodule$(SO)
Modules/_sre.o: $(srcdir)/Modules/_sre.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/_sre.c -o Modules/_sre.o
Modules/_sre$(SO):  Modules/_sre.o; $(LDSHARED)  Modules/_sre.o   -o Modules/_sre$(SO)
Modules/_codecsmodule.o: $(srcdir)/Modules/_codecsmodule.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/_codecsmodule.c -o Modules/_codecsmodule.o
Modules/_codecsmodule$(SO):  Modules/_codecsmodule.o; $(LDSHARED)  Modules/_codecsmodule.o   -o Modules/_codecsmodule$(SO)
Modules/zipimport.o: $(srcdir)/Modules/zipimport.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/zipimport.c -o Modules/zipimport.o
Modules/zipimport$(SO):  Modules/zipimport.o; $(LDSHARED)  Modules/zipimport.o   -o Modules/zipimport$(SO)
Modules/symtablemodule.o: $(srcdir)/Modules/symtablemodule.c; $(CC) $(PY_CFLAGS)  -c $(srcdir)/Modules/symtablemodule.c -o Modules/symtablemodule.o
Modules/_symtablemodule$(SO):  Modules/symtablemodule.o; $(LDSHARED)  Modules/symtablemodule.o   -o Modules/_symtablemodule$(SO)
Modules/readline.o: $(srcdir)/Modules/readline.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/readline.c -o Modules/readline.o
Modules/readline$(SO):  Modules/readline.o; $(LDSHARED)  Modules/readline.o  -lreadline -ltermcap  -o Modules/readline$(SO)
Modules/arraymodule.o: $(srcdir)/Modules/arraymodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/arraymodule.c -o Modules/arraymodule.o
Modules/arraymodule$(SO):  Modules/arraymodule.o; $(LDSHARED)  Modules/arraymodule.o   -o Modules/arraymodule$(SO)
Modules/cmathmodule.o: $(srcdir)/Modules/cmathmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cmathmodule.c -o Modules/cmathmodule.o
Modules/cmathmodule$(SO):  Modules/cmathmodule.o; $(LDSHARED)  Modules/cmathmodule.o   -o Modules/cmathmodule$(SO)
Modules/mathmodule.o: $(srcdir)/Modules/mathmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/mathmodule.c -o Modules/mathmodule.o
Modules/mathmodule$(SO):  Modules/mathmodule.o; $(LDSHARED)  Modules/mathmodule.o   -o Modules/mathmodule$(SO)
Modules/structmodule.o: $(srcdir)/Modules/structmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/structmodule.c -o Modules/structmodule.o
Modules/structmodule$(SO):  Modules/structmodule.o; $(LDSHARED)  Modules/structmodule.o   -o Modules/structmodule$(SO)
Modules/timemodule.o: $(srcdir)/Modules/timemodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/timemodule.c -o Modules/timemodule.o
Modules/timemodule$(SO):  Modules/timemodule.o; $(LDSHARED)  Modules/timemodule.o   -o Modules/timemodule$(SO)
Modules/operator.o: $(srcdir)/Modules/operator.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/operator.c -o Modules/operator.o
Modules/operator$(SO):  Modules/operator.o; $(LDSHARED)  Modules/operator.o   -o Modules/operator$(SO)
Modules/_weakref.o: $(srcdir)/Modules/_weakref.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/_weakref.c -o Modules/_weakref.o
Modules/_weakref$(SO):  Modules/_weakref.o; $(LDSHARED)  Modules/_weakref.o   -o Modules/_weakref$(SO)
Modules/_testcapimodule.o: $(srcdir)/Modules/_testcapimodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/_testcapimodule.c -o Modules/_testcapimodule.o
Modules/_testcapimodule$(SO):  Modules/_testcapimodule.o; $(LDSHARED)  Modules/_testcapimodule.o   -o Modules/_testcapimodule$(SO)
Modules/_randommodule.o: $(srcdir)/Modules/_randommodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/_randommodule.c -o Modules/_randommodule.o
Modules/_randommodule$(SO):  Modules/_randommodule.o; $(LDSHARED)  Modules/_randommodule.o   -o Modules/_randommodule$(SO)
Modules/collectionsmodule.o: $(srcdir)/Modules/collectionsmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/collectionsmodule.c -o Modules/collectionsmodule.o
Modules/collectionsmodule$(SO):  Modules/collectionsmodule.o; $(LDSHARED)  Modules/collectionsmodule.o   -o Modules/collectionsmodule$(SO)
Modules/itertoolsmodule.o: $(srcdir)/Modules/itertoolsmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/itertoolsmodule.c -o Modules/itertoolsmodule.o
Modules/itertoolsmodule$(SO):  Modules/itertoolsmodule.o; $(LDSHARED)  Modules/itertoolsmodule.o   -o Modules/itertoolsmodule$(SO)
Modules/stropmodule.o: $(srcdir)/Modules/stropmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/stropmodule.c -o Modules/stropmodule.o
Modules/stropmodule$(SO):  Modules/stropmodule.o; $(LDSHARED)  Modules/stropmodule.o   -o Modules/stropmodule$(SO)
Modules/unicodedata.o: $(srcdir)/Modules/unicodedata.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/unicodedata.c -o Modules/unicodedata.o
Modules/unicodedata$(SO):  Modules/unicodedata.o; $(LDSHARED)  Modules/unicodedata.o   -o Modules/unicodedata$(SO)
Modules/_localemodule.o: $(srcdir)/Modules/_localemodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/_localemodule.c -o Modules/_localemodule.o
Modules/_localemodule$(SO):  Modules/_localemodule.o; $(LDSHARED)  Modules/_localemodule.o   -o Modules/_localemodule$(SO)
Modules/fcntlmodule.o: $(srcdir)/Modules/fcntlmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/fcntlmodule.c -o Modules/fcntlmodule.o
Modules/fcntlmodule$(SO):  Modules/fcntlmodule.o; $(LDSHARED)  Modules/fcntlmodule.o   -o Modules/fcntlmodule$(SO)
Modules/grpmodule.o: $(srcdir)/Modules/grpmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/grpmodule.c -o Modules/grpmodule.o
Modules/grpmodule$(SO):  Modules/grpmodule.o; $(LDSHARED)  Modules/grpmodule.o   -o Modules/grpmodule$(SO)
Modules/selectmodule.o: $(srcdir)/Modules/selectmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/selectmodule.c -o Modules/selectmodule.o
Modules/selectmodule$(SO):  Modules/selectmodule.o; $(LDSHARED)  Modules/selectmodule.o   -o Modules/selectmodule$(SO)
Modules/mmapmodule.o: $(srcdir)/Modules/mmapmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/mmapmodule.c -o Modules/mmapmodule.o
Modules/mmapmodule$(SO):  Modules/mmapmodule.o; $(LDSHARED)  Modules/mmapmodule.o   -o Modules/mmapmodule$(SO)
Modules/_csv.o: $(srcdir)/Modules/_csv.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/_csv.c -o Modules/_csv.o
Modules/_csv$(SO):  Modules/_csv.o; $(LDSHARED)  Modules/_csv.o   -o Modules/_csv$(SO)
Modules/socketmodule.o: $(srcdir)/Modules/socketmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/socketmodule.c -o Modules/socketmodule.o
Modules/_socketmodule$(SO):  Modules/socketmodule.o; $(LDSHARED)  Modules/socketmodule.o   -o Modules/_socketmodule$(SO)
Modules/_ssl.o: $(srcdir)/Modules/_ssl.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl -c $(srcdir)/Modules/_ssl.c -o Modules/_ssl.o
Modules/_ssl$(SO):  Modules/_ssl.o; $(LDSHARED)  Modules/_ssl.o  -L$(SSL)/lib -lssl -lcrypto  -o Modules/_ssl$(SO)
Modules/cryptmodule.o: $(srcdir)/Modules/cryptmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cryptmodule.c -o Modules/cryptmodule.o
Modules/cryptmodule$(SO):  Modules/cryptmodule.o; $(LDSHARED)  Modules/cryptmodule.o  -lcrypt  -o Modules/cryptmodule$(SO)
Modules/nismodule.o: $(srcdir)/Modules/nismodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/nismodule.c -o Modules/nismodule.o
Modules/nismodule$(SO):  Modules/nismodule.o; $(LDSHARED)  Modules/nismodule.o  -lnsl  -o Modules/nismodule$(SO)
Modules/termios.o: $(srcdir)/Modules/termios.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/termios.c -o Modules/termios.o
Modules/termios$(SO):  Modules/termios.o; $(LDSHARED)  Modules/termios.o   -o Modules/termios$(SO)
Modules/resource.o: $(srcdir)/Modules/resource.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/resource.c -o Modules/resource.o
Modules/resource$(SO):  Modules/resource.o; $(LDSHARED)  Modules/resource.o   -o Modules/resource$(SO)
Modules/audioop.o: $(srcdir)/Modules/audioop.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/audioop.c -o Modules/audioop.o
Modules/audioop$(SO):  Modules/audioop.o; $(LDSHARED)  Modules/audioop.o   -o Modules/audioop$(SO)
Modules/imageop.o: $(srcdir)/Modules/imageop.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/imageop.c -o Modules/imageop.o
Modules/imageop$(SO):  Modules/imageop.o; $(LDSHARED)  Modules/imageop.o   -o Modules/imageop$(SO)
Modules/rgbimgmodule.o: $(srcdir)/Modules/rgbimgmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/rgbimgmodule.c -o Modules/rgbimgmodule.o
Modules/rgbimgmodule$(SO):  Modules/rgbimgmodule.o; $(LDSHARED)  Modules/rgbimgmodule.o   -o Modules/rgbimgmodule$(SO)
Modules/md5module.o: $(srcdir)/Modules/md5module.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/md5module.c -o Modules/md5module.o
Modules/md5c.o: $(srcdir)/Modules/md5c.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/md5c.c -o Modules/md5c.o
Modules/md5module$(SO):  Modules/md5module.o Modules/md5c.o; $(LDSHARED)  Modules/md5module.o Modules/md5c.o   -o Modules/md5module$(SO)
Modules/shamodule.o: $(srcdir)/Modules/shamodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/shamodule.c -o Modules/shamodule.o
Modules/shamodule$(SO):  Modules/shamodule.o; $(LDSHARED)  Modules/shamodule.o   -o Modules/shamodule$(SO)
Modules/linuxaudiodev.o: $(srcdir)/Modules/linuxaudiodev.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/linuxaudiodev.c -o Modules/linuxaudiodev.o
Modules/linuxaudiodev$(SO):  Modules/linuxaudiodev.o; $(LDSHARED)  Modules/linuxaudiodev.o   -o Modules/linuxaudiodev$(SO)
Modules/timingmodule.o: $(srcdir)/Modules/timingmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/timingmodule.c -o Modules/timingmodule.o
Modules/timingmodule$(SO):  Modules/timingmodule.o; $(LDSHARED)  Modules/timingmodule.o   -o Modules/timingmodule$(SO)
Modules/_tkinter.o: $(srcdir)/Modules/_tkinter.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -DWITH_APPINIT -DWITH_TIX -c $(srcdir)/Modules/_tkinter.c -o Modules/_tkinter.o
Modules/tkappinit.o: $(srcdir)/Modules/tkappinit.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -DWITH_APPINIT -DWITH_TIX -c $(srcdir)/Modules/tkappinit.c -o Modules/tkappinit.o
Modules/_tkinter$(SO):  Modules/_tkinter.o Modules/tkappinit.o; $(LDSHARED)  Modules/_tkinter.o Modules/tkappinit.o  -ltix -ltk -ltcl -lX11  -o Modules/_tkinter$(SO)
Modules/_cursesmodule.o: $(srcdir)/Modules/_cursesmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/_cursesmodule.c -o Modules/_cursesmodule.o
Modules/_cursesmodule$(SO):  Modules/_cursesmodule.o; $(LDSHARED)  Modules/_cursesmodule.o  -lcurses -ltermcap  -o Modules/_cursesmodule$(SO)
Modules/_curses_panel.o: $(srcdir)/Modules/_curses_panel.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/_curses_panel.c -o Modules/_curses_panel.o
Modules/_curses_panel$(SO):  Modules/_curses_panel.o; $(LDSHARED)  Modules/_curses_panel.o  -lpanel -lncurses  -o Modules/_curses_panel$(SO)
Modules/dlmodule.o: $(srcdir)/Modules/dlmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/dlmodule.c -o Modules/dlmodule.o
Modules/dlmodule$(SO):  Modules/dlmodule.o; $(LDSHARED)  Modules/dlmodule.o   -o Modules/dlmodule$(SO)
Modules/gdbmmodule.o: $(srcdir)/Modules/gdbmmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -I/usr/local/include -c $(srcdir)/Modules/gdbmmodule.c -o Modules/gdbmmodule.o
Modules/gdbmmodule$(SO):  Modules/gdbmmodule.o; $(LDSHARED)  Modules/gdbmmodule.o  -L/usr/local/lib -lgdbm  -o Modules/gdbmmodule$(SO)
Modules/_bsddb.o: $(srcdir)/Modules/_bsddb.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -I$(DBINC) -c $(srcdir)/Modules/_bsddb.c -o Modules/_bsddb.o
Modules/_bsddb$(SO):  Modules/_bsddb.o; $(LDSHARED)  Modules/_bsddb.o  -L$(DBLIB) -ldb-$(DBLIBVER)  -o Modules/_bsddb$(SO)
Modules/binascii.o: $(srcdir)/Modules/binascii.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/binascii.c -o Modules/binascii.o
Modules/binascii$(SO):  Modules/binascii.o; $(LDSHARED)  Modules/binascii.o   -o Modules/binascii$(SO)
Modules/parsermodule.o: $(srcdir)/Modules/parsermodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/parsermodule.c -o Modules/parsermodule.o
Modules/parsermodule$(SO):  Modules/parsermodule.o; $(LDSHARED)  Modules/parsermodule.o   -o Modules/parsermodule$(SO)
Modules/cStringIO.o: $(srcdir)/Modules/cStringIO.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cStringIO.c -o Modules/cStringIO.o
Modules/cStringIO$(SO):  Modules/cStringIO.o; $(LDSHARED)  Modules/cStringIO.o   -o Modules/cStringIO$(SO)
Modules/cPickle.o: $(srcdir)/Modules/cPickle.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cPickle.c -o Modules/cPickle.o
Modules/cPickle$(SO):  Modules/cPickle.o; $(LDSHARED)  Modules/cPickle.o   -o Modules/cPickle$(SO)
Modules/zlibmodule.o: $(srcdir)/Modules/zlibmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -I$(prefix)/include -c $(srcdir)/Modules/zlibmodule.c -o Modules/zlibmodule.o
Modules/zlibmodule$(SO):  Modules/zlibmodule.o; $(LDSHARED)  Modules/zlibmodule.o  -L$(exec_prefix)/lib -lz  -o Modules/zlibmodule$(SO)
Modules/multibytecodec.o: $(srcdir)/Modules/cjkcodecs/multibytecodec.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cjkcodecs/multibytecodec.c -o Modules/multibytecodec.o
Modules/_multibytecodecmodule$(SO):  Modules/multibytecodec.o; $(LDSHARED)  Modules/multibytecodec.o   -o Modules/_multibytecodecmodule$(SO)
Modules/_codecs_cn.o: $(srcdir)/Modules/cjkcodecs/_codecs_cn.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cjkcodecs/_codecs_cn.c -o Modules/_codecs_cn.o
Modules/_codecs_cn$(SO):  Modules/_codecs_cn.o; $(LDSHARED)  Modules/_codecs_cn.o   -o Modules/_codecs_cn$(SO)
Modules/_codecs_hk.o: $(srcdir)/Modules/cjkcodecs/_codecs_hk.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cjkcodecs/_codecs_hk.c -o Modules/_codecs_hk.o
Modules/_codecs_hk$(SO):  Modules/_codecs_hk.o; $(LDSHARED)  Modules/_codecs_hk.o   -o Modules/_codecs_hk$(SO)
Modules/_codecs_iso2022.o: $(srcdir)/Modules/cjkcodecs/_codecs_iso2022.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cjkcodecs/_codecs_iso2022.c -o Modules/_codecs_iso2022.o
Modules/_codecs_iso2022$(SO):  Modules/_codecs_iso2022.o; $(LDSHARED)  Modules/_codecs_iso2022.o   -o Modules/_codecs_iso2022$(SO)
Modules/_codecs_jp.o: $(srcdir)/Modules/cjkcodecs/_codecs_jp.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cjkcodecs/_codecs_jp.c -o Modules/_codecs_jp.o
Modules/_codecs_jp$(SO):  Modules/_codecs_jp.o; $(LDSHARED)  Modules/_codecs_jp.o   -o Modules/_codecs_jp$(SO)
Modules/_codecs_kr.o: $(srcdir)/Modules/cjkcodecs/_codecs_kr.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cjkcodecs/_codecs_kr.c -o Modules/_codecs_kr.o
Modules/_codecs_kr$(SO):  Modules/_codecs_kr.o; $(LDSHARED)  Modules/_codecs_kr.o   -o Modules/_codecs_kr$(SO)
Modules/_codecs_tw.o: $(srcdir)/Modules/cjkcodecs/_codecs_tw.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/cjkcodecs/_codecs_tw.c -o Modules/_codecs_tw.o
Modules/_codecs_tw$(SO):  Modules/_codecs_tw.o; $(LDSHARED)  Modules/_codecs_tw.o   -o Modules/_codecs_tw$(SO)
Modules/xxsubtype.o: $(srcdir)/Modules/xxsubtype.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/xxsubtype.c -o Modules/xxsubtype.o
Modules/xxsubtype$(SO):  Modules/xxsubtype.o; $(LDSHARED)  Modules/xxsubtype.o   -o Modules/xxsubtype$(SO)
Modules/shmmodule.o: $(srcdir)/Modules/shmmodule.c; $(CC) $(CCSHARED) $(CFLAGS) $(CPPFLAGS)  -c $(srcdir)/Modules/shmmodule.c -o Modules/shmmodule.o
Modules/shmmodule$(SO):  Modules/shmmodule.o; $(LDSHARED)  Modules/shmmodule.o   -o Modules/shmmodule$(SO)
