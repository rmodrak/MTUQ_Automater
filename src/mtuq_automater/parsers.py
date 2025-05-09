
import obspy
import sys

from copy import deepcopy
from os.path import join

from mtuq_automater import pkg_dir
from mtuq_automater.utils import flinn_engdahl
from mtuq_automater.utils.datetime import UTCDateTime, _super


from mtuq_automater.yaml import read_yaml as yaml_reader
from mtuq_automater.yaml import write_yaml as yaml_writer


def event_tagger(datetime, latitude, longitude, depth_in_km=None, magnitude=None):
    # returns 'YYYY-MM-DD--HH-MM-SS__REGION'

    parts = [
	_super(datetime).format_custom(),
        flinn_engdahl(latitude, longitude),
        ]

    return '__'.join(parts)


def event_parser(datetime, latitude, longitude, depth_in_km, magnitude, 
    tagger=event_tagger, template=None, write_yaml=True, verbose=1):

    if not isinstance(datetime, UTCDateTime):
        datetime = _super(datetime)

    if not (-90. < latitude < +90.):
        raise ValueError(f'Invalid latitude')

    if not (-180. < longitude < 180.):
        raise ValueError(f'Invalid longitude')

    if depth_in_km < 0:
        print('Warning: unexpected event depth')


    # construct event string
    event_tag = tagger(datetime, latitude, longitude)
    if verbose > 0:
        print(event_tag)

    # read default key,value pairs
    if not template:
        template = join(pkg_dir(), 'templates', 'events', 'default.yaml')

    default = yaml_reader(template)


    # update key,value pairs
    event = deepcopy(default)

    for key, val in [
        ['event_tag', event_tag],
        ['event_latitude', latitude],
        ['event_longitude', longitude],
        ['event_depth_km', depth_in_km],
        ['event_magnitude', magnitude],
        ['origin_time', datetime.format_iris()],
        ]:

        event.update({key: val})

        if verbose > 1:
            print('  key, val:', key, val)

    if write_yaml:
        yaml_writer(event_tag+'.yaml', event)

    return event


