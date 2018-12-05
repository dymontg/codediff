""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
import re
import logging
from xml.dom.minidom import parse as xmlparse

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

def prettyformatxml(path, encoding=None):
    """
    Takes a one line xml file and splits it into many.
    Formats the xml to be more readable.
    :param path: path to file as a string.
    :return: the prettier xml.
    """
    return xmlparse(path, encoding).toprettyxml(indent=' '*2)


def prettyfilexml(path, encoding=None):
    """
    Takes a one line xml file and splits it into many.
    Formats the xml to be more readable.
    :param path: path to file as a string.
    :return: None.
    """
    xml_str = prettyformatxml(path, encoding).encode(encoding or 'utf-8')
    # TODO: We should still write to the file in blocks, not all at once.
    with open(path, 'wb') as xml:
        xml.write(xml_str)

def sdv(d, reverse=False):
    """Sort a dictionary by value and return a representation
    of it as a list.

    :param d: the dictionary to sort
    :param reverse: whether to reverse the order. Default is false.
    :returns: a sorted list.
    """
    return sorted(d.items(), key=lambda t: t[1], reverse=reverse)
