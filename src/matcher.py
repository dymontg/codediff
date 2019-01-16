""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import logging
import difflib
import itertools
import inspect

_logger = logging.getLogger('codediff')


class BaseMatcher:
    def __init__(self, report1, report2):
        self.report1 = report1
        self.report2 = report2

    def compare(self):
        raise NotImplementedError('Subclasses must implement ratio()')


class SequenceMatcher(BaseMatcher):
    def __init__(self, report1, report2):
        super(SequenceMatcher, self).__init__(report1, report2)

    def compare(self):
        # Currently the reports contents contain every character. In the future, we
        # want to calculate the ratio of a fragmented file.
        # To calculate the actual ratio, we iterate through the content generator
        # and append it to a diff ratio array.
        diff_ratios = []
        _logger.debug('========== BEGIN `%s::%s::ratio` ==========', __name__, self.__class__.__name__)
        _logger.info('\rComparing %s and %s', self.report1, self.report2, extra={'terminator': ''})
        # for character_seq, character_seq_2 in zip(self.report1.content, self.report2.content):
        character_seq = self.report1.content
        character_seq_2 = self.report2.content
        seq_match = difflib.SequenceMatcher(lambda x: x in " \t", character_seq, character_seq_2)
        diff_ratios.append(seq_match.quick_ratio())

        # The next line is where we would determine the actual diff ratio
        # if the file was fragmented.
        diff_ratio = diff_ratios[0]
        _logger.debug('========== END `%s::%s::ratio` ==========', __name__, self.__class__.__name__)
        return diff_ratio


class SnapMatcher(BaseMatcher):
    def __init__(self, report1, report2):
        super(SnapMatcher, self).__init__(report1, report2)
        self._blacklisted_keys = ['project', 'path']

    def compare(self):
        diff_ratio = 0.0
        # Take the minimium number of elements of the two reports.
        total_elems = max(self.report1.elems() - len(self._blacklisted_keys),
                          self.report2.elems() - len(self._blacklisted_keys))
        inc_rate = 1.0 / total_elems
        _logger.debug('Found %d elements; increment rate is %f', total_elems, inc_rate)
        _logger.info('\rComparing %s and %s', self.report1, self.report2, extra={'terminator': ''})

        # Compare the elements
        sentinel = ('\0', '\0')
        _logger.debug('REPORT %s, %s', self.report1.name, self.report2.name)
        if self._cmp(self.report1.name, self.report2.name):
            diff_ratio += inc_rate

        for stage_elem1, stage_elem2 in itertools.zip_longest(
                self.report1.getstageelems(),
                self.report2.getstageelems(),
                fillvalue=sentinel):
            _logger.debug('STAGE %s %s', stage_elem1, stage_elem2)
            if self._cmp(stage_elem1[1], stage_elem2[1]):
                diff_ratio += inc_rate
        for sprite_elem1, sprite_elem2 in itertools.zip_longest(
                self.report1.stage.getspriteselems(),
                self.report2.stage.getspriteselems(),
                fillvalue=sentinel):
            _logger.debug('SPRITE %s %s', sprite_elem1, sprite_elem2)
            if self._cmp(sprite_elem1[1], sprite_elem2[1]):
                diff_ratio += inc_rate
        for block_elem1, block_elem2 in itertools.zip_longest(
                self.report1.getblockselems(),
                self.report2.getblockselems(),
                fillvalue=sentinel):
            _logger.debug('BLOCK %s %s', block_elem1, block_elem2)
            if self._cmp(block_elem1[1], block_elem2[1]):
                diff_ratio += inc_rate
        for cvar_elem1, cvar_elem2 in itertools.zip_longest(
                self.report1.getcvarselems(),
                self.report2.getcvarselems(),
                fillvalue=sentinel):
            _logger.debug('CUSTOM VAR %s %s', cvar_elem1, cvar_elem2)
            if self._cmp(cvar_elem1[1], cvar_elem2[1]):
                diff_ratio += inc_rate

        # Divide the number of shared elements by the total.
        return diff_ratio

    def _similar(self, val1, val2, thresh):
        return self._cmp(val1, val2)

    def _cmp(self, val1, val2):
        return val1 == val2
