#!/bin/bash

iter=0

input1="initial_run_lines_sorted"
input2="koi-gaia-initial.txt"

while IFS= read -r f1 <&3 && read -r f2 <&4
do
    echo $f1 $f2 $iter
    # if [ $f1 == $iter ]
    # then
        # echo $f2 $iter
    # fi

    ((iter++))
done 3<$input1 4<$input2
