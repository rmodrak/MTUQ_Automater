
import yaml

from os.path import exists, join


# define a custom representer for strings
# https://stackoverflow.com/questions/38369833/pyyaml-and-using-quotes-for-strings-only
class quoted(str):
    pass

def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

yaml.add_representer(quoted, quoted_presenter)


def read_yaml(filename):
    if not exists(filename):
        raise IOError(f'File not found: {filename}')

    with open(filename, 'r') as file:
        yaml_dict = yaml.load(file, yaml.Loader)

    return yaml_dict


def write_yaml(filename, data, **kwargs):
    if 'sort_keys' not in kwargs:
        kwargs.update({'sort_keys':False})

    #if 'preserve_quotes' not in kwargs:
    #    kwargs.update({'preserve_quotes':True})

    with open(filename, 'w') as file:
        yaml.dump(data, file, **kwargs)


