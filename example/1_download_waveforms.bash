#!/bin/bash


user="rmodrak"
repo="waveforms_fdsn"
remote="git@github.com:${user}/${repo}.git"
urlbase="https://raw.githubusercontent.com/${user}/${repo}"


# if download fails, stop immediately
set -e

function download {
    if ! command -v curl &> /dev/null
    then
        echo "curl not found"
        exit 1
    fi

    dirname=$1
    filename=$2
    fullname=$1/$2

    mkdir -p "$dirname"
    curl $urlbase/$fullname --output $fullname
    }

wd="$PWD/waveforms"

echo
echo Working directory: $wd
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

    git clone --branch $event $remote $event

    # faster alternative?
    #download $event "resample=1Hz,remove_response=True.tgz"
    #download $event "resample=1Hz,remove_response=True.yaml"
done

echo
echo "Success"
echo

