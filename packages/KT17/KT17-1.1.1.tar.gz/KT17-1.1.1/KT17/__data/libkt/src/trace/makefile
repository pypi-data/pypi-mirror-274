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
	$(CCo) conttrace.cc -o $(BUILDDIR)/conttrace.o
	$(CCo) interptraceclosestpos.cc -o $(BUILDDIR)/interptraceclosestpos.o
	$(CCo) latlt.cc -o $(BUILDDIR)/latlt.o
	$(CCo) fieldlinernorm.cc -o $(BUILDDIR)/fieldlinernorm.o
	$(CCo) trace.cc -o $(BUILDDIR)/trace.o


