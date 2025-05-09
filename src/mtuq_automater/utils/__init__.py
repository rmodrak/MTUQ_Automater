
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


