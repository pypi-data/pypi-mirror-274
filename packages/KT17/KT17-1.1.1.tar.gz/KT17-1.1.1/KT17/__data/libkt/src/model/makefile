# CFLAGS for CC
CFLAGS=-lm -fPIC -std=c++17 -g -O3 -Wextra

# Compiler
CCo=g++ -c $(CFLAGS)
CC=g++ $(CFLAGS)

# set the build directory
ifndef BUILDDIR 
	BUILDDIR=../../build
endif

all: obj 

obj:
	$(CCo) dipole.cc -o $(BUILDDIR)/dipole.o
	$(CCo) disk.cc -o $(BUILDDIR)/disk.o
	$(CCo) qhsheet.cc -o $(BUILDDIR)/qhsheet.o
	$(CCo) shield.cc -o $(BUILDDIR)/shield.o
	$(CCo) kt14.cc -o $(BUILDDIR)/kt14.o
	$(CCo) kt17.cc -o $(BUILDDIR)/kt17.o
	$(CCo) ktmodel.cc -o $(BUILDDIR)/ktmodel.o
	$(CCo) model.cc -o $(BUILDDIR)/model.o


