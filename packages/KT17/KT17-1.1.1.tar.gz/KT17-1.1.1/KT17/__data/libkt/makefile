# CFLAGS for CC
ifdef DEBUG
	CFLAGS=-lm -std=c++17 -Wextra -ggdb3 -no-pie 
else 
	CFLAGS=-lm -std=c++17 -Wextra
endif 


# Compilers - the mingw ones allow us to compile for Windows using Linux
CCo=g++ -fPIC -c $(CFLAGS)
CC=g++ -fPIC $(CFLAGS)
CCWo=x86_64-w64-mingw32-g++-win32 -c $(CFLAGS)
CCW=x86_64-w64-mingw32-g++-win32 $(CFLAGS)


export BUILDDIR=$(shell pwd)/build
ifeq ($(OS),Windows_NT)
#windows stuff here
	MD=mkdir
	LIBFILE=libkt.dll
else
#linux and mac here
	OS=$(shell uname -s)
	ifeq ($(OS),Linux)
		LIBFILE=libkt.so
	else
		LIBFILE=libkt.dylib
	endif
	MD=mkdir -p
endif


ifeq ($(PREFIX),)
#install path
	PREFIX=/usr/local
endif

.PHONY: all lib clean header test spline obj install uninstall  windows

all: spline
	$(MD) $(BUILDDIR)
	$(MD) lib
	cd src; make all

spline:
	cd lib/libspline; make all
	cp -v lib/libspline/lib/libspline.* lib/

obj:
	$(MD) $(BUILDDIR)
	cd src; make obj

lib:
	cd src; make lib

header:
	cd src; make header
# ifneq (,$(shell which python3))
# 	python3 generateheader.py
# else
# 	@echo "python3 command doesn't appear to exist - skipping header regeneration..."
# endif

windows:
#this should build the library for Windows using mingw
	$(MD) $(BUILDDIR)
	cd lib/libspline; make winobj
	cd src; make winobj
	$(MD) lib/libkt
	cd src; make winlib

test:
	cd test; make all

install:
	cp -v include/kt.h $(PREFIX)/include
	cp -v lib/$(LIBFILE) $(PREFIX)/lib
	chmod 0775 $(PREFIX)/lib/$(LIBFILE)
ifeq ($(OS),Linux)
	ldconfig
endif

uninstall:
	rm -v $(PREFIX)/include/kt.h
	rm -v $(PREFIX)/lib/$(LIBFILE)
ifeq ($(OS),Linux)
	ldconfig
endif

clean:
	cd lib/libspline; make clean
	-rm -vfr build
	rm -v lib/$(LIBFILE)