
import obspy
import pandas as pd
import sys

from copy import deepcopy
from os.path import join

from mtuq_automater import pkg_dir
from mtuq_automater.utils import flinn_engdahl
from mtuq_automater.utils.datetime import UTCDateTime, _super
from mtuq_automater.yaml import read_yaml



def event_namer(
    datetime=None,
    latitude=None,
    longitude=None,
    depth_in_km=None,
    magnitude=None,
    ):

    parts = [
        _super(datetime).format_custom(),
        flinn_engdahl(latitude, longitude),
        ]

    # returns 'YYYY-MM-DD--HH-MM-SS__REGION'
    return '__'.join(parts)


def default_header():
    return ('datetime','latitude','longitude','depth_in_km','magnitude')

def default_config():
    return join(pkg_dir(), 'templates', 'config.yaml')



#
# for pulling waveforms (bin/pull*)
#

def config_parser(
    datetime=None,
    latitude=None,
    longitude=None,
    depth_in_km=None,
    magnitude=None, 
    name='',
    namer=event_namer,
    defaults=None,
    verbose=0,
    ):

    if datetime is None:
        raise Exception('Required input: datetime')

    if latitude is None:
        raise Exception('Required input: latitude')

    if longitude is None:
        raise Exception('Required input: longitude')

    if depth_in_km is None:
        raise Exception('Required input: depth_in_km')

    if not isinstance(datetime, UTCDateTime):
        datetime = _super(datetime)

    if not (-90. < latitude < +90.):
        raise ValueError(f'Invalid latitude')

    if not (-180. < longitude < 180.):
        raise ValueError(f'Invalid longitude')

    if depth_in_km < 0:
        print('Warning: unexpected event depth')


    # construct event string
    if not name:
        try:
            assert callable(namer)
            name = namer(datetime, latitude, longitude)
            print(name)
        except:
            raise ValueError('config_parser failed: invalid name/namer')

    if verbose:
        print(f'Parsing event: {name}')


    if defaults is None:
        defaults = read_yaml(default_config())
    event = deepcopy(defaults)

    for key, val in [
        ['event_tag', name],
        ['event_latitude', latitude],
        ['event_longitude', longitude],
        ['event_depth_km', depth_in_km],
        ['event_magnitude', magnitude],
        ['origin_time', datetime.format_iris()],
        ]:

        event.update({key: val})

        if verbose > 1:
            print('  key, val:', key, val)

    return event


#
# for generating scripts (bin/setup*)
#


#
# for processing multiple events (bin/batch*)
#


def parse_header(filename):
    """ Parses single-line header from text file
    """
    with open(filename, 'r') as file:
        line = file.readline()

    # expects a single line beginning with #
    if line.startswith('#'):
        return line[1:].split()
    else:
        return default_header()


def check_header(names):
    if 'datetime' not in names:
        print(
            f'Missing from header: datetime'
            )
        raise Exception

    if 'latitude' not in names:
        print(
            f'Missing from header: latitude'
            )
        raise Exception

    if 'longitude' not in names:
        print(
            f'Missing from header: longitude'
            )
        raise Exception
    if 'depth_in_m' not in names and\
       'depth_in_km' not in names:
        print(
            f'Header must include of the following:'
            f'depth_in_m, depth_in_km'
            )
        raise Exception


def read_events(filename, names=None, **kwargs):
    """ Reads origin times and locations from text file
    """
    defaults = {'comment':'#', 'sep':r'\s+'}
    defaults.update(**kwargs)


    # ignore pandas header keyword argument (too complex)
    if 'header' in defaults:
        print(
           '\n',
           'Ignoring `header` keyword argument'
           '\n',
           )
        defaults.pop('header')


    # use simple header parsing instead
    if names is None:
       names = parse_header(filename)

    try:
        check_header(names)
    except:
        print(
           '\n',
           'check_header() failed, falling back to default_header()',
           '\n',
           )
        names = default_header()

    df = pd.read_table(filename, names=names, **defaults)


    nrows, ncols = df.shape
    if len(names) != ncols:
        print(
            f'Warning:  len(names) !=  ncols'
            f'  len(names) = {len(names)}'
            f'  ncols = {ncols}'
            )

    for _i, event in df.iterrows():
        event = event.to_dict()
        try:
              UTCDateTime(event['datetime'])
        except:
            print(
                '\nCheck order of columns in text file?\n'
                'Invalid datetime: %s'
                 )
            raise ValueError
        try:
            lat = event['latitude']
            assert -90. <= lat <= +90.
        except:
            print(
                '\nCheck order of columns in text file?\n'
                'Invalid latitude: %s'
                 )
            raise ValueError
        try:
            lon = event['longitude']
            assert -90. <= lon <= +90.
        except:
            print(
                '\nCheck order of columns in text file?\n'
                'Invalid longitude: %s'
                 )
            raise ValueError

    return df


def read_configs(filename, **kwargs):
    defaults = {'comment':'#', 'sep':r'\s+'}
    defaults.update(**kwargs)

    df = pd.read_table(filename, names=['path'], **defaults)
    return df.iloc[:,0]



