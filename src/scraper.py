""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
import os
import logging
import sys
from urllib import request
from src.utils import Pair

_logger = logging.getLogger('codediff')


class CanvasScraper:
    def __init__(self, paths):
        self.paths = paths
        self.data = {}

    def parse_html(self):
        for i, path in enumerate(self.paths):
            sys.stdout.write('\rParsing {} \t({}/{})'.format(path, i, len(self.paths)))
            sys.stdout.flush()
            with open(path, 'r') as html:
                content = html.read()
                start = content.find('url=')+4 # beginning of link in content
                end = content.find('<title>')-5 # end of link in content
                link = (content[start:end])
            data = self._get_data(link)
            if data:
                self.data[path] = data

    def _get_data(self, link):
        resp = request.urlopen(link)
        url = resp.geturl()
        if 'Username' not in url:
            _logger.info('\nNo snap project found at %s. Ignoring.', link)
        else:
            user = url[url.find('Username=')+9:url.find('&ProjectName')]
            project = url[url.find('&ProjectName')+13:]
            return Pair(user, project)

    def scrape(self):
        paths = []
        try:
            os.mkdir('canvas_files')
        except FileExistsError:
            _logger.info('\nCanvas output folder already exists, overwriting old files.')
        for i, tupl in enumerate(self.data.items()):
            path = tupl[0]
            data = tupl[1]
            ofile_path = 'canvas_files/' + os.path.basename(path).replace('.html', '.xml')
            response = request.urlopen('https://cloud.snap.berkeley.edu/projects/' + data[0] + '/' + data[1])
            sys.stdout.write('\rScraping {} \t({}/{})'.format(path, i, len(self.paths)))
            sys.stdout.flush()
            with open(ofile_path, 'w+') as ofile:
                rdata = response.read().decode('utf-8')
                # Spaghetti code, but whatever.
                _, rdata = rdata.split('<snapdata>')
                rdata, _ = rdata.rsplit('<media')
                ofile.write(rdata)
            paths.append(ofile_path)
        _logger.debug('Finished with scrape.')
        return paths
