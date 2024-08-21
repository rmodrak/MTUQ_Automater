
import re

from os.path import abspath, basename, isdir, exists, join
from shutil import copy

from mtuq_automater.pysep import parse_event, parse_paths
from mtuq_automater.utils import is_url, read_yaml, url_copy



def generate_script(input_file, input_dir, output_dir):
    """ Generates MTUQ scripts by substituting event-specific values into
       region-specific templates
    
       Event-specific values, including origin time and location, are simply 
       read from a PySEP file. These values are then substituted into one 
       or more region-specific templates. (The way in which the templates are
       determined is somewhat involved, as explained in the detailed notes)
    
       Imagine we have already run PySEP for a given event, but have yet
       to run MTUQ. Suppose that 
    
        - PYSEP_FILE is the PySEP input file
        - PYSEP_DIR is the PySEP download directory containing SAC waveforms
          and weight files
    
       The script generator can then be invoked as follows:
    
        >> script_generator  PYSEP_FILE  PYSEP_DIR
    

       A user-supplied templates can be specified in the PySEP input file 
       as follows:
    
         mtuq_automater:
           templates:
           - path_or_url_1
           - path_or_url_2
    
       If no user-supplied templates are given, the script generator will
       try to construct a list of templates based on
      
       - proximity of the event to known sites of interest
          (see templates/sites)
       - Flinn-Engdahl regionalization (see templates/flinn_engdahl)
    
       If the event occurs away from any currently implemented sites or regions,
       the script generator falls back to 1D reference models
       (for example templates/ak135f)
    
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
        # output filename usually reduces to {DATETIME}-{FLINN_ENGDAHL_REGION}-{TEMPLATE_NAME}
        filename = f'{event['id']}-{basename(template)}'
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
    try:
        user_templates = read_yaml(input_file)['mtuq_automater']['templates']
    except:
       user_templates = None

    if user_templates:
        return user_templates

    else:
        # eventually, we will add various site and region schemes
        raise NotImplementedError


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

