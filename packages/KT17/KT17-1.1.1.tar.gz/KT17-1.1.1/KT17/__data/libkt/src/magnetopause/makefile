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
	$(CCo) magnetopause.cc -o $(BUILDDIR)/magnetopause.o
	$(CCo) withinmp.cc -o $(BUILDDIR)/withinmp.o

