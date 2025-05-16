
import re

from os.path import abspath, basename, dirname, isdir, exists, join
from shutil import copy

#from mtuq_automater.pysep import parse_event, parse_paths
from mtuq_automater.utils import is_url, url_copy
from mtuq_automater.yaml import read_yaml


def user_bool(prompt, default=None):
    """ Prompts user for yes or no answer
    """
    user_string = input(prompt).lower()

    if user_string == '' and default is not None:
        return strtobool(default)

    else:
        try:
            return strtobool(user_string)
        except:
            # retry
            user_bool(prompt, default=default)


def strtobool(val, default=0):
    # modified from distutil.util.strtobool
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError



def pysep_dir():
    try:
        import pysep
    except:
        raise ImportError('PySEP import failed')
    return  abspath(join(pysep.__path__[0], '..'))


def pkg_dir():
    # directory in which source code exists
    src_dir = dirname(abspath(__file__))

    # package directory
    pkg_dir = abspath(join(src_dir, '..', '..'))

    return pkg_dir



def mtuq_setup(input_file, input_dir, output_dir):
    """ Generates MTUQ scripts by substituting event-specific values into
       region-specific templates
    
    """

    #
    # event time and location from PySEP input file
    #
    event = parse_event(read_yaml(input_file))

    #
    # paths relative to PySEP download directory
    #
    paths = parse_paths(input_dir)

    #
    # the main work starts now
    #
    templates = build_templates_list(input_file)

    for template in templates:
        # output filename usually reduces to 
        #{DATETIME}__{FLINN_ENGDAHL_REGION}__{TEMPLATE_NAME}

        filename = f'{event['id']}__{basename(template)}'
        output = join(output_dir, filename)

        print('')
        print('template:', basename(template))
        print('output:  ', basename(output))
        print('')

        if is_url(template):
            url_copy(template, output)
        else:
            copy(template, output)

        _overwrite(output, paths, event)


def build_templates_list(input_file, verbose=True):
    #
    # read user-supplied templates if given
    #
    return [join(pkg_dir(), 'templates', 'models', 'ak135F', 'ak135F_sw.py')]


    # eventually, we will add various site and region schemes


def _overwrite(filename, paths, event):
        # we apply a regular expression substitution to every line in the file
        with open(filename, "r") as file:
            lines = file.readlines()

        # the following gets applied to every line:
        #   value = format % value
        #   re.sub(pattern+'.*', pattern+value, line)

        tuples = [
            # pattern           value                  format
            ['event_id=    ',   event.id,              '\'%s\''],
            ['path_data=    ',  paths.data,            '\'%s\''],
            ['path_weights= ',  paths.weights,         '\'%s\''],
            ['\'latitude\':',   event.latitude,        '%f,'],
            ['\'longitude\':',  event.longitude,       '%f,'],
            ['\'depth_in_m\':', event.depth_in_m,      '%f,'],
            ['magnitude=',      event.magnitude,       '%f'],
            ['\'time\':',       event.origin_time_str, 'UTCDateTime(\'%s\')'],
            #['magnitudes=',    event.magnitude']],
            ]

        for pattern, value, fmt in tuples:
            compiled = re.compile('.*'+pattern+'.*')

            for _i, line in enumerate(lines):
                if compiled.match(line):
                    try:
                        string = fmt % value
                    except:
                        string = fmt % float(value)
                    lines[_i] = re.sub(pattern+'.*', pattern+string, line)

                    break

        with open(filename, "w") as file:
            file.writelines(lines)


class SiteFinder(object):
   def __init__(self, lat, lon):
        # not implemented yet
        pass


class RegionFinder(object):
    def __init__(self, lat, lon):
        # not implemented yet
        pass

    def flinn_engdahl(self):
        # not implemented yet
        pass

