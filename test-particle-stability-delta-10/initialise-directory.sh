#!/bin/bash


while getopts ":a:n:" opt; do
  case $opt in
    a) ic_name="$OPTARG"
    ;;
    n) nsys="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

module load gcc/7.3.0
source /mnt/raid-cita/obertas/opt/python/venv-py-3.6.4-rebound-3.10.1/bin/activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/python/3.6.4/lib

cd generate-and-run-systems
python generate_initial_conditions.py $ic_name
cd ../spock-stability
./submit-all-jobs -a$ic_name -n$nsys