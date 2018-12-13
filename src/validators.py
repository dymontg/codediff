""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import re
import logging
from src.utils import UnsupportedFiletypeError

_logger = logging.getLogger('codediff')


class PathValidator:
    def validate_dir(self, file_paths):
        _logger.warning('This validator does nothing. Use a subclass such as `XmlPathValidator`')
        pass

    def validate_file(self, path):
        _logger.warning('This validator does nothing. Use a subclass such as `XmlPathValidator`')
        pass

    def _validate_path_extension(self, path, exe):
        if not path.endswith(exe):
            raise UnsupportedFiletypeError('{} is not an supported {} file type. Aborting.'.format(path, exe[1:]))

    def _find_files_by_extension(self, file_paths, exe):
        filename_paths = [x for x in file_paths if x.endswith(exe)]
        _logger.debug('Found following %s files: %s', exe, filename_paths)
        for filename_path in filename_paths:
            self.validate_file(filename_path)
        return filename_paths


class XmlPathValidator(PathValidator):
    def validate_file(self, path):
        self._validate_path_extension(path, '.xml')
        return path

    def validate_dir(self, file_paths):
        return self._find_files_by_extension(file_paths, '.xml')


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


class HtmlPathValidator(PathValidator):
    def validate_file(self, path):
        self._validate_path_extension(path, '.html')
        return path

    def validate_dir(self, file_paths):
        return self._find_files_by_extension(file_paths, '.html')
