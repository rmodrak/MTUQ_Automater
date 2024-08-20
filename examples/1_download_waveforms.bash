#!/bin/bash


user="rmodrak"
repo="waveforms_fdsn"
remote="git@github.com:${user}/${repo}.git"
urlbase="https://raw.githubusercontent.com/${user}/${repo}"


function check_path { 
    if ! command -v curl &> /dev/null
    then
        echo
        echo "Not found on path: curl"
        echo
        echo "(Install curl using package manager and try again?)"
        echo 
        exit 1
    fi
    }

function download {
    dirname=$1
    filename=$2
    filetype=$3
    fullname=$1/$2.$3

    curl "$urlbase/$fullname" --output "${dirname}.${filetype}"
    }


function main {

    # if downloads fail, stop immediately
    set -e

    check_path


    wd="$PWD/waveforms"

    echo
    echo "Current working directory:"
    echo $wd
    echo

    mkdir -p $wd
    cd $wd


    echo
    echo "Downloading waveforms"
    echo

    for event in \
        "2017-09-03T03-30-01-NORTH_KOREA"\
        "2017-11-15T05-29-32-SOUTH_KOREA"\

    do
        echo $event

        download $event "resample=1Hz,remove_response=True" yaml
        download $event "resample=1Hz,remove_response=True" tgz

        tar -xzf "${event}.tgz"
        mv "resample=1Hz,remove_response=True" ${event}

        echo

    done

    echo
    echo "Success"
    echo

    }

main
