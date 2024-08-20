#!/bin/bash

function check_path () {
    if ! command -v script_generator &> /dev/null
    then
        echo
        echo "Not found on path: script_generator"
        echo
        echo "(Add mtuq_automater bin/ to path and try again?)"
        echo
        exit 1
    fi
    }

check_path


for event in \
    "2017-09-03T03-30-01-NORTH_KOREA"\
    "2017-11-15T05-29-32-SOUTH_KOREA"\

do

    input_file="waveforms/${event}.yaml"
    input_dir="waveforms/${event}"
    output_dir="$PWD/scripts"

    mkdir -p $output_dir
    script_generator $input_file $input_dir $output_dir

done

