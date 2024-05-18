#!/bin/bash
CWD=$(pwd)
declare -a libgits=("https://github.com/mattkjames7/libspline.git")
declare -a libdirs=("lib/libspline" )
for i in "${!libdirs[@]}"
do
    echo $i ${libdirs[$i]} ${libgits[$i]}
    cd ${libdirs[$i]}
    git stash
    git pull origin main
    cd ${CWD}
done