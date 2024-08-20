#!/bin/bash


user="rmodrak"
repo="greens_cps"
remote="git@github.com:${user}/${repo}.git"
urlbase="https://raw.githubusercontent.com/${user}/${repo}/master"

model="mdj2"
depth_in_m="500"


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
    fullname=$1/$2

    mkdir -p "$dirname"
    curl $urlbase/$fullname --output $fullname
    }


function cps_formatted {
    depth_in_m=$1
    printf "%04d" $((depth_in_m/100))
    }


function main {
    # if download fails, stop immediately
    set -e


    wd="$PWD/greens"

    echo
    echo "Current working directory:"
    echo $wd
    echo

    mkdir -p $wd
    cd $wd


    echo
    echo "Downloading Greens functions"
    echo

    dirname='mdj2'
    filename=$(cps_formatted $depth_in_m).tgz

    download $dirname $filename

    cd $dirname
    tar -xzf $filename

    echo
    echo "Success"
    echo

    }


check_path
main

