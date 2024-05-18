@echo off

echo Compiling model

g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c dipole.cc -o ..\build\dipole.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c disk.cc -o ..\build\disk.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c qhsheet.cc -o ..\build\qhsheet.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c shield.cc -o ..\build\shield.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c kt14.cc -o ..\build\kt14.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c kt17.cc -o ..\build\kt17.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c ktmodel.cc -o ..\build\ktmodel.o
g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -c model.cc -o ..\build\model.o

exit /b 0

:CompileError
echo Compilation error
exit /b 8
