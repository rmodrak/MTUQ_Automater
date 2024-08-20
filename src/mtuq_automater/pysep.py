#!/usr/bin/env python

import os
import re
import shutil
import sys
import yaml

from glob import glob
from obspy import UTCDateTime
from os.path import abspath, isdir, exists, join
from mtuq_automater.utils import AttribDict


def parse_event(pysep_dict):
    event = AttribDict()
     
    if 'event_latitude' not in pysep_dict:
        raise ValueError('Missing from PySEP file: event_latitude')

    event.latitude = pysep_dict['event_latitude']


    if 'event_longitude' not in pysep_dict:
        raise ValueError('Missing from PySEP file: event_longitude')

    event.longitude = pysep_dict['event_longitude']

    if 'event_depth_km' not in pysep_dict:
        raise ValueError('Missing from PySEP file: event_depth_km')

    event.depth_in_m = 1000.*pysep_dict['event_depth_km']


    if 'origin_time' not in pysep_dict:
        raise ValueError('Missing from PySEP file: origin_time')

    print(pysep_dict['origin_time'])
    try:
        origin_time = UTCDateTime(pysep_dict['origin_time'])
    except:
        print('Badly formatted origin_time in PySEP file')
        raise Exception()

    event.origin_time = origin_time
    event.origin_time_str = _formatted(origin_time)


    if 'event_magnitude' in pysep_dict:
        event.magnitude = pysep_dict['event_magnitude']
    else:
        print('Missing from PySEP file: event_magnitude')
        event.magnitude = None

    if 'event_tag' in pysep_dict:
        event.id = pysep_dict['event_tag']
    else:
        event.id = _event_id(origin_time, event.latitude, event.longitude)

    return event


def parse_paths(dirname):
    paths = AttribDict()

    paths.data = join(dirname, 'SAC/*sac')

    paths.weights = join(dirname, 'weights.dat')

    if len(glob(paths.data)) == 0:
        print(f'Warning: wildcard unmatched: {paths.data}')

    if not exists(paths.weights):
        print(f'Warning: file not found: {paths.weights}')

    return paths


def read_yaml(filename):
    with open(filename) as stream:
        pysep_dict = yaml.safe_load(stream)
    return pysep_dict


def _abspath(base, *args):
    return join(abspath(base), *args)


def _formatted(datetime):
    yyyymmdd = '%04d-%02d-%02d' % (datetime.year, datetime.month, datetime.day)
    hhmmss = '%02d:%02d:%02d' % (datetime.hour, datetime.minute, datetime.second)
    return f'{yyyymmdd}T{hhmmss}Z'


def _event_id(datetime):
    yyyymmdd = '%04d-%02d-%02d' % (datetime.year, datetime.month, datetime.day)
    hhmmss = '%02d-%02d-%02d' % (datetime.hour, datetime.minute, datetime.second)
    return f'{yyyymmdd}T{hhmmss}-REGION'

