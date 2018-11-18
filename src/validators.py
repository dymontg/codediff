""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import re, os, logging
from src.utils import UnsupportedFiletypeError, NotEnoughFilesError

_logger = logging.getLogger('codediff')

class PathValidator:
    def validate_dir(self, file_paths):
        _logger.warning('This validator does nothing. Use a subclass such as `XmlPathValidator`')
        pass

    def validate_file(self, path):
        _logger.warning('This validator does nothing. Use a subclass such as `XmlPathValidator`')
        pass

class XmlPathValidator(PathValidator):
    def validate_file(self, path):
        _logger.debug('========== BEGIN `%s::%s::validate_file` ==========', __name__, self.__class__.__name__)
        _logger.debug('Validating %s has `.xml` extension', path)
        if not path.endswith('.xml'):
            raise UnsupportedFiletypeError('{} is not an supported xml file type. Aborting.'.format(path))
        _logger.debug('========== END `%s::%s::validate_file` ==========', __name__, self.__class__.__name__)
        return path

    def validate_dir(self, file_paths):
        xml_filename_paths = [x for x in file_paths if x.endswith('.xml')]
        _logger.debug('Found following xml files: %s', xml_filename_paths)
        for filename_path in xml_filename_paths:
            self.validate_file(filename_path)
        return xml_filename_paths


class SnapPathValidator(XmlPathValidator):
    def validate_file(self, path):
        _logger.debug('========== BEGIN `%s::%s::validate_file` ==========', __name__, self.__class__.__name__)
        _REGEX_LITERAL = re.compile(r'^<project name=".*?" app=".*? http:\/\/snap.berkeley.edu" version=".*?">')
        super(SnapPathValidator, self).validate_file(path)
        _logger.debug('Validating %s is a snap file', path)

        with open(path, 'r') as snap_xml:
            # Only read the first 4096 bytes, as the project directive should be at the top of the file.
            # (Let's hope their project name is not massive!)
            _logger.debug('Opened %s, reading first 4096 bytes', path)
            if re.match(_REGEX_LITERAL, snap_xml.read(4096)) is None:
                # Tests if the regex does not match the first 4096 bytes.
                raise UnsupportedFiletypeError('{} is not a supported snap xml. Aborting.'.format(path))
        _logger.debug('========== END `%s::%s::validate_file` ==========', __name__, self.__class__.__name__)
        return path
