""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
import re, logging

class FileError(Exception):
    pass


class FileIOError(IOError):
    pass


class UnsupportedFiletypeError(FileError):
    pass

class NotEnoughFilesError(FileError):
    pass


def lineify_xml(path, encoding='utf-8'):
    """
    Takes one line xml and splits it into many. Makes it
    human readable.
    :param path: path to file as a string.
    :return: None.
    """
    logging.debug('========== BEGIN ` %s::lineify_xml` ==========', __name__)
    _REGEX_LITERAL = r'><'
    logging.debug('Lineifying xml file %s with encoding %s', path, encoding)
    with open(path, 'rb+') as xml:
        # Currently, we read the whole file into memory.
        # We could also has an ifile and ofile, with filename `filename.lineified.xml`
        # Could check for changes using a hash
        logging.debug('Subsituting %s with >\\n<', _REGEX_LITERAL)
        content = re.sub(_REGEX_LITERAL, r'>\n<', xml.read().decode(encoding), flags=re.M)
        logging.debug('Seeking 0th byte, truncating, and writing substitued content')
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
    logging.debug('========== END `%s::lineify_xml` ==========', __name__)
