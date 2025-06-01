
from mtuq_automater.utils import pkg_dir
from os.path import join

def build_templates_list(input_file, verbose=True):
    #
    # read user-supplied templates if given
    #
    return [join(pkg_dir(), 'templates', 'models', 'ak135F', 'ak135F_sw.py')]


    # eventually, we will add various site and region schemes

