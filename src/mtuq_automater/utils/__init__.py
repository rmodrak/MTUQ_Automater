
import obspy
import yaml

from os.path import abspath, dirname, join
from retry import retry


# Python2/3 compatibility
try:
    from urllib import URLopener
except ImportError:
    from urllib.request import URLopener


class AttribDict(obspy.core.util.attribdict.AttribDict):
    pass


def flinn_engdahl(lat, lon):
    from obspy.clients.iris import Client

    _, region = Client().flinnengdahl(lat, lon)
    region = region.replace(" ", "_")
    region = region.replace(",", "")
    #region = region.upper()
    return region


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


@retry(Exception, tries=4, delay=2, backoff=2)
def url_copy(url, filename):
    opener = URLopener()
    opener.retrieve(url, filename)




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
    pkg_dir = abspath(join(src_dir, '..', '..', '..'))

    return pkg_dir


