
import re

from mtuq_automater.pysep import parse_event
from mtuq_automater.utils import read_yaml




def build_templates_list(input_file, verbose=True):
    # read user-supplied templates if given
    try:
        user_templates = read_yaml(input_file)['mtuq_automater']['templates']
    except:
       user_templates = None

    if user_templates:
        return user_templates

    else:
        # eventually, we will add various regionalization schemes
        raise NotImplementedError


def generate_script(filename, paths, event):
        # to generate event-specific MTUQ scripts, we apply a regular expression
        # substitution every line in the following file
        with open(filename, "r") as file:
            lines = file.readlines()

        # the following gets applied to every line:
        #   value = format % value
        #   re.sub(pattern+'.*', pattern+value, line)

        tuples = [
            # pattern           value              format
            ['event_id=    ',   event.id,              '\'%s\''],
            ['path_data=    ',  paths.data,            '\'%s\''],
            ['path_weights= ',  paths.weights,         '\'%s\''],
            ['\'latitude\':',   event.latitude,        '%f,'],
            ['\'longitude\':',  event.longitude,       '%f,'],
            ['\'depth_in_m\':', event.depth_in_m,      '%f,'],
            ['magnitude=',      event.magnitude,       '%f'],
            ['\'time\':',       event.origin_time_str, 'UTCDateTime(\'%s\'')],
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


def search_sites(lat, lon):
    # not implemented yet
    return


def search_regions(lat, lon):
    # not implemented yet
    return

