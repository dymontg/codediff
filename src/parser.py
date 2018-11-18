""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import re, os, logging
import difflib
from src.validators import PathValidator
from src.utils import UnsupportedFiletypeError, NotEnoughFilesError

_logger = logging.getLogger('codediff')

class FileParser:
    pass

class SnapParser(FileParser):
    def __init__(self, path):
        # TODO Ensure path has been parsed
        self.path = path

    def parse(self):
        pass

class PathParser:
    def __init__(self, paths, validator=None):
        if validator and not isinstance(validator, PathValidator):
            raise TypeError('Path validator must be an instance of `PathValidator`')
        self.paths = paths
        self.validator = validator

    def parse(self):
        _logger.debug('========== BEGIN `%s::%s::parse` ==========', __name__, self.__class__.__name__)
        _logger.debug('Parsing paths %s', self.paths)
        paths = []
        for path in self.paths:
            if os.path.isfile(path):
                _logger.debug('%s is a file', path)
                if self.validator:
                    self.validator.validate_file(path)
                paths += path
            elif os.path.isdir(path):
                _logger.debug('%s is a directory', path)
                path = path.rstrip('/') # Will only work on unix, use os.path.normalpath for windows
                file_paths = [root + '/' + x for root, _, files_list in os.walk(path) for x in files_list]
                if self.validator:
                    self.validator.validate_dir(file_paths)
                paths += file_paths
            else:
                raise FileNotFoundError('Could not find file {}. Aborting.'.format(path))

        if len(paths) < 2:
            raise NotEnoughFilesError('Expecting at least two xml files but found less than two.')

        _logger.debug('========== END `%s::%s::parse` ==========', __name__, self.__class__.__name__)
        return paths

    def __iter__(self):
        parsed_paths = self.parse()
        yield parsed_paths
