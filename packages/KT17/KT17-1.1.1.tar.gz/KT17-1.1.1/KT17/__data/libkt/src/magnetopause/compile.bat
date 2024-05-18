@echo off

echo Compiling magnetopause

g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c magnetopause.cc -o ..\build\magnetopause.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c withinmp.cc -o ..\build\withinmp.o

exit /b 0

:CompileError
echo Compilation error
exit /b 8
