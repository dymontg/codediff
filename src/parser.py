""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import re, os, logging
import difflib
from src.utils import UnsupportedFiletypeError, NotEnoughFilesError, Pair


_logger = logging.getLogger('codediff')

class XmlParser:
    def __init__(self, path):
        _logger.debug('========== BEGIN `%s::%s::__init__` ==========', __name__, self.__class__.__name__)
        _logger.debug('Instantiating `XmlParser` with argument `path`: %s.', path)
        self.paths = []
        if type(path) is list:
            _logger.debug('`path` is of type list, validating paths.')
            self._validate_paths(path)
        if type(path) is str:
            _logger.debug('`path` is of type str, coberting to list and validating paths.')
            self._validate_paths([path])
        _logger.debug('========== END `%s::%s::__init__` ==========', __name__, self.__class__.__name__)

    def _validate_paths(self, paths):
        _logger.debug('========== BEGIN `%s::%s::_validate_paths` ==========', __name__, self.__class__.__name__)
        _logger.debug('Validating paths %s', paths)
        for path in paths:
            if os.path.isfile(path):
                _logger.debug('%s is a file', path)
                self._validate_file(path)
                self.paths.append(path)
            elif os.path.isdir(path):
                _logger.debug('%s is a directory', path)
                path = path.rstrip('/') # Will only work on unix, use os.path.normalpath for windows.
                filename_paths = [root + '/' + x for root, _, files_list in os.walk(path) for x in files_list]
                xml_filename_paths = [x for x in filename_paths if x.endswith('.xml')]
                _logger.debug('Found %s in `%s`', filename_paths, path)
                _logger.debug('Found following xml files: %s', xml_filename_paths)
                for filename_path in xml_filename_paths:
                    self._validate_file(filename_path)
                    self.paths.append(filename_path)
            else:
                raise FileNotFoundError('Could not find file {}. Aborting.'.format(path))

        if len(self.paths) < 2:
            raise NotEnoughFilesError('Expecting at least two xml files, but found less than two.')
        _logger.debug('========== END `%s::%s::_validate_paths` ==========', __name__, self.__class__.__name__)

    def _validate_file(self, path):
        _logger.debug('========== BEGIN `%s::%s::_validate_file` ==========', __name__, self.__class__.__name__)
        _logger.debug('Validating %s has `.xml` extension', path)
        if not path.endswith('.xml'):
            raise UnsupportedFiletypeError('{} is not an supported xml file type. Aborting.'.format(path))
        _logger.debug('========== END `%s::%s::_validate_file` ==========', __name__, self.__class__.__name__)

    def ratios(self):
        _logger.debug('========== BEGIN `%s::%s::ratios` ==========', __name__, self.__class__.__name__)
        self.diff_ratios = dict()
        _logger.debug('Finding similarity ratio between all files.')
        for i, path in enumerate(self.paths):
            with open(path, 'r') as xml:
                _logger.debug('Opened %s, i=%i', path, i)
                for j in range(i+1, len(self.paths)):
                    path2 = self.paths[j]
                    with open(path2, 'r') as xml2:
                        _logger.debug('Opened %s, j=%i, i=%i', path2, j, i)
                        seq_match = difflib.SequenceMatcher(lambda x: x in " \t", xml.read(), xml2.read())
                        _logger.info('Comparing %s and %s.......', path, path2, extra={'terminator': ''})
                        ratio = seq_match.quick_ratio()
                        _logger.info('DONE')
                        self.diff_ratios[Pair(path, path2)] = ratio

        _logger.debug('========== END `%s::%s::ratios` ==========', __name__, self.__class__.__name__)
        return self.diff_ratios

class SnapXmlParser(XmlParser):
    def _validate_file(self, path):
        _logger.debug('========== BEGIN `%s::%s::_validate_file` ==========', __name__, self.__class__.__name__)
        _REGEX_LITERAL = re.compile(r'^<project name=".*?" app=".*? http:\/\/snap.berkeley.edu" version=".*?">')
        super(SnapXmlParser, self)._validate_file(path)
        _logger.debug('Validating %s is a snap file', path)

        with open(path, 'r') as snap_xml:
            # Only read the first 4096 bytes as the project directive should be near the top of the file.
            # (Let's hope their project name is not gigantic!)
            _logger.debug('Opened %s, reading first 4096 bytes', path)
            if re.match(_REGEX_LITERAL, snap_xml.read(4096)) is None:
                # Tests if the regex does not match the first 4096 bytes.
                raise UnsupportedFiletypeError('{} is not a supported snap file. Aborting.'.format(path))
        _logger.debug('========== END `%s::%s::_validate_file` ==========', __name__, self.__class__.__name__)
