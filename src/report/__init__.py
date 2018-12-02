""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

class BaseFileReport:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path


class FileReport(BaseFileReport):
    def __init__(self, path, content, bin_length):
        super(FileReport, self).__init__(path)
        self.content = content
        self.b_len = bin_length

    def __repr__(self):
        return 'FileReport(path={}, content_length={}, encoding=UTF-8)'.format(self.path,
                                                                               self.b_len)
