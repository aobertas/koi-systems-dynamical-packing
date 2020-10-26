#!/bin/bash

iter=0

input1="koi-gaia-initial.txt"
input2="initial_run_lines_sorted"

while IFS= read -r f1 <&3 && read -r f2 <&4
do
    if [ $f2 == $iter ]
    then
        echo a #$f1 $f2 $iter
        ((iter++))
    else
        iter=$f2
        echo b #$f1 $f2 $iter
    fi
    # if [ $f1 == $iter ]
    # then
        # echo $f2 $iter
    # fi
done 3<$input1 4<$input2
