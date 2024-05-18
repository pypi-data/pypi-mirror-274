@echo off

echo Compiling trace

g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c conttrace.cc -o ..\build\conttrace.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c interptraceclosestpos.cc -o ..\build\interptraceclosestpos.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c latlt.cc -o ..\build\latlt.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c fieldlinernorm.cc -o ..\build\fieldlinernorm.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c trace.cc -o ..\build\trace.o
	
exit /b 0

:CompileError
echo Compilation error
exit /b 8
