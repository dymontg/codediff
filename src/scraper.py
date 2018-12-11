""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
import re
import os
import sys
import logging
from urllib import request

from src.utils import UnsupportedFiletypeError

_logger = logging.getLogger('codediff')

class SnapScraper:
    def __init__(self, path):
        _logger.debug('========== BEGIN `%s::%s::__init__` ==========', __name__, self.__class__.__name__)
        _logger.debug('Instantiating `HtmlParser` with argument `path`: %s.', path)
        self.paths = []
        self.data = []
        if type(path) is list:
            _logger.debug('`path` is of type list, validating paths.')
            self._validate_paths(path)
        if type(path) is str:
            _logger.debug('`path` is of type str, converting to list and validating paths.')
            self._validate_paths([path])

        for p in self.paths:
            with open(p, 'r') as html:
                content = html.read()
                start = content.find('url=')+4 #beginning of link in content
                end = content.find('<title>')-5 #end of link in content
                link = (content[start:end])
            data = self._get_data(link)
            if data:
                self.data.append(data)
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

    def _get_data (self, link):
        resp = request.urlopen(link)
        url = resp.geturl()
        if 'Username' not in url:
            _logger.info('No snap project found at {}. Ignoring.'.format(link))
        else:
            user = url[url.find('Username=')+9:url.find('&ProjectName')]
            project = url[url.find('&ProjectName')+13:len(url)]
            return ([user, project])

    def scrape(self):
        paths = []
        try:
            os.mkdir('canvas_files')
        except FileExistsError:
            _logger.info('Canvas output folder already exists, overwriting old files.')
        for d in self.data:
            # TODO get this path from the html file.
            path = 'canvas_files/' + d[0] + d[1] + '.xml'
            response = request.urlopen('https://cloud.snap.berkeley.edu/projects/' + d[0] + '/' + d[1])
            with open(path, 'w+') as newfile:
                newfile.write(response.read().decode('utf-8'))
            paths.append(path)
        _logger.debug('Finished with scrape.')
        return paths
