# CFLAGS for CC
CFLAGS=-lm -fPIC -std=c++17 -g -O3 -Wextra

# Compiler
CCo=g++ -c $(CFLAGS)
CC=g++ $(CFLAGS)

ifndef BUILDDIR 
	BUILDDIR=.
endif

OS=$(shell uname -s)
ifeq ($(OS),Linux)
	LDFLAGS=-lm -lstdc++ -L../lib -lspline -Wl,-rpath='$$ORIGIN/../lib'
	LIBFILE=libkt.so
else
	LDFLAGS=-lm -lstdc++ -L../lib -lspline
	LIBFILE=libkt.dylib
endif

all: obj lib

obj:
	cd magnetopause; make all
	cd model; make all
	cd trace; make all
	$(CCo) libkt.cc -o $(BUILDDIR)/libkt.o

lib:
	$(CC) -shared $(BUILDDIR)/*.o \
			-o ../lib/$(LIBFILE)  $(LDFLAGS)
	
