import re
import os
import sys
import logging
from src.utils import UnsupportedFiletypeError

_logger = logging.getLogger('codediff')

class scraperInstance:
    def __init__(self, path):
        _logger.debug('========== BEGIN `%s::%s::__init__` ==========', __name__, self.__class__.__name__)
        _logger.debug('Instantiating `HtmlParser` with argument `path`: %s.', path)
        self.links = []
        self.paths = []
        if type(path) is list:
            _logger.debug('`path` is of type list, validating paths.')
            self._validate_paths(path)
        if type(path) is str:
            _logger.debug('`path` is of type str, converting to list and validating paths.')
            self._validate_paths([path])
        _logger.debug('========== END `%s::%s::__init__` ==========', __name__, self.__class__.__name__)
        for p in self.paths:
            with open(p, 'r') as html:
                content = html.read()
                start = content.find('url=')
                end = content.find('<title>')
                self.links.append(content[start+4:end-5])
        print(self.links)


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
                html_filename_paths = [x for x in filename_paths if x.endswith('.html')]
                _logger.debug('Found %s in `%s`', filename_paths, path)
                _logger.debug('Found following html files: %s', html_filename_paths)
                for filename_path in html_filename_paths:
                    self._validate_file(filename_path)
                    self.paths.append(filename_path)
            else:
                raise FileNotFoundError('Could not find file {}. Aborting.'.format(path))

    def _validate_file(self, path):
        _logger.debug('========== BEGIN `%s::%s::_validate_file` ==========', __name__, self.__class__.__name__)
        _logger.debug('Validating %s has `.html` extension', path)
        if not path.endswith('.html'):
            raise UnsupportedFiletypeError('{} is not an supported html file type. Aborting.'.format(path))
        _logger.debug('========== END `%s::%s::_validate_file` ==========', __name__, self.__class__.__name__)

    def scrape(self, paths, destination):
        pass


