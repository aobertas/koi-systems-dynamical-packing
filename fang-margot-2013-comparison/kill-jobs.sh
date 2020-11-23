#!/bin/bash



# for f in simulation-archives/koi-gaia/integrated-archives/1e9-orbits/*
# for f in simulation-archives/q1-q6/integrated-archives/1e9-orbits/*
# do
#     qsub -v filename=$f,inttype="orbit",i=$iter sunnyvale-qsub-script
#     ((iter++))
# done

input="jobs-to-kill"

while IFS= read -r id
do
    qdel $id
done < "$input"