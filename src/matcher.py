""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import logging
import difflib
# from statistics import mean

_logger = logging.getLogger('codediff')


class SequenceMatcher:
    def __init__(self, report1, report2):
        self.report1 = report1
        self.report2 = report2

    def ratio(self):
        # Currently the reports contents contain every character. In the future, we
        # want to calculate the ratio of a fragmented file.
        # To calculate the actual ratio, we iterate through the content generator
        # and append it to a diff ratio array.
        diff_ratios = []
        _logger.debug('========== BEGIN `%s::%s::ratio` ==========', __name__, self.__class__.__name__)
        _logger.info('Comparing %s and %s.......', self.report1, self.report2, extra={'terminator': ''})
        # for character_seq, character_seq_2 in zip(self.report1.content, self.report2.content):
        character_seq = self.report1.content
        character_seq_2 = self.report2.content
        seq_match = difflib.SequenceMatcher(lambda x: x in " \t", character_seq, character_seq_2)
        diff_ratios.append(seq_match.quick_ratio())

        # The next line is where we would determine the actual diff ratio
        # if the file was fragmented.
        diff_ratio = diff_ratios[0]
        _logger.info('DONE - %d%% similar', round(float(diff_ratio)*100, 1))
        _logger.debug('========== END `%s::%s::ratio` ==========', __name__, self.__class__.__name__)
        return diff_ratio
