
import re

from os.path import abspath, basename, dirname, isdir, exists, join
from shutil import copy

from mtuq_automater.parsers import event_parser, pysep_parser
from mtuq_automater.template_selector import build_templates_list
from mtuq_automater.utils import AttribDict, is_url, url_copy, pkg_dir
from mtuq_automater.utils.yaml import read_yaml


def _resub(lines, event):
    """ Default backend
    """
    # the following gets applied to every line:
    #   value = format % value
    #   re.sub(pattern+'.*', pattern+value, line)

    tuples = [
        # pattern           value                  format
        #['event_id=    ',   event.id,              '\'%s\''],
        ['path_data=    ',  event.path_data,       '\'%s\''],
        ['path_weights= ',  event.path_weights,    '\'%s\''],
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

    return lines


def main(input_file, input_dir, output_dir, resub=_resub):
    """ Generates MTUQ scripts by substituting event-specific attributes into
    region-specific templates
    """

    #
    # collect event attributes
    #
    event = AttribDict()

    # event time and location from input_file
    event.update(
        pysep_parser(read_yaml(input_file))
        )

    # event paths relative to input_dir
    event.update({
        'path_data': join(input_dir, 'SAC/*sac'),
        'path_weights': join(input_dir, 'weights.dat'),
        })


    # based on known test sites and regions
    templates = build_templates_list(input_file)


    #
    # substitute event time and location into templates
    #
    print()
    print('Substituting event attributes into region-specific templates')
    print()

    for template in templates:
        # output filename usually reduces to 
        #{DATETIME}__{FLINN_ENGDAHL_REGION}__{TEMPLATE_NAME}
        filename = f"{event['id']}__{basename(template)}"
        fullname = join(output_dir, filename)

        print(f'\ntemplate:\n  {template}')
        print(f'\noutput script:\n  {filename}\n')

        if is_url(template):
            url_copy(template, fullname)
            template = fullname

        with open(template, "r") as file:
            lines = file.readlines()

        lines = resub(lines, event)

        with open(fullname, "w") as file:
            file.writelines(lines)

