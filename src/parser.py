""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import re, os, logging
import xml.etree.ElementTree as et
from src.validators import PathValidator
from src.report import FileReport
from src.report.snap_report import SnapReport
from src.utils import UnsupportedFiletypeError, NotEnoughFilesError

_logger = logging.getLogger('codediff')

class FileParser:
    def __init__(self, path):
        # TODO Ensure path as been parsed
        self.path = path

    def parse(self):
        with open(self.path, 'r') as f:
            # We pass the whole files content in for now, but we really should
            # fragament it.
            report = FileReport(self.path, f.read(),
                                os.path.getsize(self.path))

        return report

def parse_files(parsed_paths):
    files = []
    for i, path1 in enumerate(parsed_paths):
        parsed_file1 = FileParser(path1).parse()
        for path2 in parsed_paths[i+1:]:
            files.append((path1, path2, parsed_file1, FileParser(path2).parse()))
    return files

class SnapParser(FileParser):
    def __init__(self, path):
        super(SnapParser, self).__init__(path)

    def parse(self):
        project = et.parse(self.path).getroot()
        name = project.attrib['name']
        stage = project.find('stage')
        blocks = project.find('blocks')
        custom_vars = project.find('variables')

        return SnapReport(self.path, project=project,
                          name=name, stage=stage, blocks=blocks,
                          vars=custom_vars)


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
                paths.append(path)
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
