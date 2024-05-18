@echo off

where /q gcc
if %ERRORLEVEL% neq 0 (
	echo GCC wasn't found
	exit /b 6
)

echo Compiling libkt...

cd magnetopause
call compile.bat
cd ..

cd model
call compile.bat
cd ..

cd trace
call compile.bat
cd ..


g++ -fPIC -c -lm -fopenmp -std=c++17 -Wextra -O3 libkt.cc -o -o ..\build\libkt.o
if %ERRORLEVEL% neq 0 (goto CompileError)

g++ -lm -fopenmp -fPIC -std=c++17 -Wextra -O3 -shared -o libkt.dll  ..\build\*.o ..\lib\libspline\build\*.o
if %ERRORLEVEL% neq 0 (goto CompileError)


echo Done


exit /b 0

:CompileError
echo Compilation error
exit /b 8
