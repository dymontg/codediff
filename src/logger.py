""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
import logging
import sys

def init_logger(log_level):
    _logger = logging.getLogger('codediff')
    _logger.setLevel(log_level)
#    stdout_handler = logging.StreamHandler(stream=sys.stdout) # Logging handler for debug and verbosity.
#    stdout_handler.setLevel(log_level) # only show errors if they don't enable debugging.
#    stdout_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    handler = LeveledStreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    handler.set_level_formatter(LeveledFormatter(logging.DEBUG, '%(levelname)s - %(message)s'))
    handler.set_level_formatter(LeveledFormatter(logging.INFO, '%(message)s'))
    handler.set_level_formatter(LeveledFormatter(logging.WARNING, '%(message)s'))
    _logger.addHandler(handler)

    return _logger

class TerminatorStreamHandler(logging.StreamHandler):

    def emit(self, record):
        # WARNING: FOLLOWING ONLY WORKS IN PYTHON 3.2 AND ABOVE.
        # SEE https://github.com/python/cpython/blob/3.2/Lib/logging/__init__.py#L897
        if 'terminator' in record.__dict__:
            self.terminator = record.__dict__['terminator']
        super(TerminatorStreamHandler, self).emit(record)
        self.flush()
        self.terminator = '\n'

class LeveledStreamHandler(TerminatorStreamHandler):
    def __init__(self, stream=sys.stdout):
        super(LeveledStreamHandler, self).__init__(stream)
        self._level_fmtrs = dict()

    def set_level_formatter(self, level_fmtr):
        self._level_fmtrs[level_fmtr.get_log_level()] = level_fmtr

    def format(self, record):
        if record.levelno in self._level_fmtrs:
            fmtr = self._level_fmtrs[record.levelno]
        elif self.formatter:
            fmtr = self.formatter
        else:
            fmtr = logging._defaultFormatter
        return fmtr.format(record)

class LeveledFormatter(logging.Formatter):
    def __init__(self, log_level=logging.INFO, fmt=None, datefmt=None):
        super(LeveledFormatter, self).__init__(fmt, datefmt)
        self._validate_level(log_level)
        self.set_log_level(log_level)

    def set_log_level(self, log_level):
        self.log_level = log_level

    def get_log_level(self):
        return self.log_level

    def _validate_level(self, log_level):
        return log_level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
