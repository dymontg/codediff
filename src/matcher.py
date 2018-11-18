""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import logging
import difflib
from src.filereport import SnapReport

_logger = logging.getLogger('codediff')


class SnapMatcher:
    def __init__(self, path1, path2):
        # TODO Ensure paths have been parsed
        self.path1 = path1
        self.path2 = path2

    def ratio(self):
        _logger.debug('========== BEGIN `%s::%s::ratio` ==========', __name__, self.__class__.__name__)
        with open(self.path1, 'r') as xml, open(self.path2, 'r') as xml2:
            seq_match = difflib.SequenceMatcher(lambda x: x in " \t", xml.read(), xml2.read())
            _logger.info('Comparing %s and %s.......', self.path1, self.path2, extra={'terminator': ''})
            diff_ratio = seq_match.quick_ratio()
            _logger.info('DONE - %d%% similar', round(float(diff_ratio)*100, 1))
            _logger.debug('========== END `%s::%s::ratio` ==========', __name__, self.__class__.__name__)
        return diff_ratio


def snapcompare(parsed_paths):
    ratios = {}
    for i, path1 in enumerate(parsed_paths):
        for path2 in parsed_paths[i+1:]:
            ratios[path1, path2] = SnapMatcher(path1, path2).ratio()
    return ratios
