#!/usr/bin/env python

import os
import re
import shutil
import sys
import yaml

from os.path import abspath, isdir, exists, join


def read_pysep(input_file, output_dir='.'):
    try:
         dict = read_yaml(input_file)
    except:
        raise Exception('Badly formatted YAML file: %s' % input_file)
     
    if 'event_tag' not in dict:
        raise ValueError('Missing from PySEP file: event_tag')

    if 'origin_time' not in dict:
        raise ValueError('Missing from PySEP file: origin_time')

    if 'event_latitude' not in dict:
        raise ValueError('Missing from PySEP file: event_latitude')

    if 'event_longitude' not in dict:
        raise ValueError('Missing from PySEP file: event_longitude')

    if 'event_depth_km' not in dict:
        raise ValueError('Missing from PySEP file: event_depth_km')

    if 'data_path' not in dict:
        dict['path_data'] = _abspath(output_dir, 'SAC/*.BH[ZRT].sac')

    if 'weight_path' not in dict:
        dict['path_weights'] = _abspath(output_dir, 'weights.dat')

    return dict


def read_yaml(filename):
    with open(filename) as stream:
        dict = yaml.safe_load(stream)
    return dict


def is_url(path_or_url):
    try:
        # python2
        from urlparse import urlparse
    except ModuleNotFoundError:
        # python3
        from urllib.parse import urlparse

    try:
        result = urlparse(path_or_url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False

    # More robust, but requires django
    #from django.core.validators import URLValidator
    #from django.core.exceptions import ValidationError
    #try:
    #    URLValidator()(path_or_url)
    #    return True
    #except ValidationError:
    #    return False


def _abspath(base, *args):
    return join(abspath(base), *args)



