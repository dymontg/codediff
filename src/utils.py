""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
import re
import logging


class FileError(Exception):
    pass


class FileIOError(IOError):
    pass


class UnsupportedFiletypeError(FileError):
    pass


class NotEnoughFilesError(FileError):
    pass


class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return '{}, {}'.format(self.a, self.b)

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('`key` must be of type integer.')
        if key not in [0, 1]:
            raise IndexError('Expecting an index of 0 and 1, but found {}.'.format(key))

        if key == 0:
            return self.a
        return self.b


def lineify_xml(path, encoding='utf-8'):
    """
    Takes one line xml and splits it into many. Makes it
    human readable.
    :param path: path to file as a string.
    :return: None.
    """
    _logger = logging.getLogger('codediff')
    _logger.debug('========== BEGIN ` %s::lineify_xml` ==========', __name__)
    _REGEX_LITERAL = r'><'
    logging.debug('Lineifying xml file %s with encoding %s.', path, encoding)
    with open(path, 'rb+') as xml:
        # Currently, we read the whole file into memory.
        # We could also has an ifile and ofile, with filename `filename.lineified.xml`.
        # Could check for changes using a hash.
        logging.debug('Subsituting %s with >\\n<', _REGEX_LITERAL)
        content = re.sub(_REGEX_LITERAL, r'>\n<', xml.read().decode(encoding), flags=re.M)
        logging.debug('Seeking 0th byte, truncating, and writing substitued content.')
        xml.seek(0)
        xml.truncate()
        xml.write(bytes(content, encoding))
        # WIP: bugged
        '''_BLOCK_SIZE = 4096 # bytes
        current_tell = xml.tell()
        while content:
            content = re.sub(_REGEX_LITERAL, r'>\n<', content, flags=re.M)
            delta_blen = len(content) - _BLOCK_SIZE
            xml.write(bytes('\23'*delta_blen, encoding))
            xml.seek(current_tell)
            xml.write(bytes(content, encoding))
            current_tell = xml.tell()
            content = xml.read(_BLOCK_SIZE).decode(encoding)'''
    _logger.debug('========== END `%s::lineify_xml` ==========', __name__)


def dict_verify(dictionary, kws):
    pure_kws = [x.split('=')[0] if '=' in x else x for x in kws]
    # First we check for default values
    for item in [x for x in kws if '=' in x]:
        key, value = item.split('=')
        dictionary[key] = value

    # Then we verify that the dictionary has the proper values
    for key, _ in dictionary.items():
        if key not in pure_kws:
            raise ValueError('Key `{}` not in acceptable keywords.'.format(key))

def sdv(d, reverse=False):
    """Sort a dictionary by value and return a representation
    of it as a list.
    :param d: the dictionary to sort
    :param reverse: whether to reverse the order. Default is false.
    :returns: a sorted list.
    """
    return sorted(d.items(), key=lambda t: t[1], reverse=reverse)
