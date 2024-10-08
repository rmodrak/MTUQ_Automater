
import obspy
import yaml

from retry import retry


# Python2/3 compatibility
try:
    from urllib import URLopener
except ImportError:
    from urllib.request import URLopener


class AttribDict(obspy.core.util.attribdict.AttribDict):
    pass


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


def read_yaml(filename):
    with open(filename) as stream:
        pysep_dict = yaml.safe_load(stream)
    return pysep_dict


@retry(Exception, tries=4, delay=2, backoff=2)
def url_copy(url, filename):
    opener = URLopener()
    opener.retrieve(url, filename)

