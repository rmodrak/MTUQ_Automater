#!/bin/bash

MPIRUN=mpirun


if [[ $# -eq 0 ]]
then
   MPI_ENV="False"

elif [[ $# -eq 1 ]]
then
    if ! command -v $MPIRUN &> /dev/null
    then
        echo
        echo "Not found on path: $MPIRUN"
        echo
        echo "Setting MPI_ENV = False"
        echo
       MPI_ENV="False"
    else
       MPI_ENV="True"
       NPROC=$1
    fi
fi


wd="$PWD/output"

echo
echo "Current working directory:"
echo $wd
echo

mkdir -p $wd
cd $wd


for script in \
    "2017-09-03T03-30-01-NORTH_KOREA-FullMomentTensor.SurfaceWaves.py"\
    "2017-11-15T05-29-32-SOUTH_KOREA-FullMomentTensor.SurfaceWaves.py"\

do
    if [ "$MPI_ENV" = "True" ]
    then
        $MPIRUN -n $NPROC python ../scripts/$script
    else
        python ../scripts/$script
    fi

done

