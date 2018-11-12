""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""

import re, os
import difflib
from src.utils import UnsupportedFiletypeError, NotEnoughFilesError

class XmlParser:
    def __init__(self, path):
        self.paths = []
        if type(path) is list:
            self._validate_paths(path)
        if type(path) is str:
            self._validate_paths([path])

    def _validate_paths(self, paths):
        for path in paths:
            if os.path.isfile(path):
                self._validate_file(path)
                self.paths.append(path)
            elif os.path.isdir(path):
                if path.endswith('/'):
                    path = path[:-1] # Remove extra backslash if required

                filename_paths = [root + '/' + x for root, _, files_list in os.walk(path) for x in files_list]
                xml_filename_paths = [x for x in filename_paths if x.endswith('.xml')]
                for filename_path in xml_filename_paths:
                    self._validate_file(filename_path)
                    self.paths.append(filename_path)
            else:
                raise FileNotFoundError('Could not find file {}. Aborting.'.format(path))

        if len(self.paths) < 2:
            raise NotEnoughFilesError('Expecting at least two xml files but found less than two.')

    def _validate_file(self, path):
        if not path.endswith('.xml'):
            raise UnsupportedFiletypeError('{} is not an supported xml file type. Aborting.'.format(path))

    def ratios(self):
        self.diff_ratios = dict()
        # TODO: this is terribly slow. Add threading.
        for i, path in enumerate(self.paths):
            with open(path, 'r') as xml:
                for j in range(i+1, len(self.paths)):
                    path2 = self.paths[j]
                    with open(path2, 'r') as xml2:
                        seq_match = difflib.SequenceMatcher(lambda x: x in " \t", xml.read(), xml2.read())
                        ratio = seq_match.ratio()
                        self.diff_ratios[path, path2] = ratio

        return self.diff_ratios

class SnapXmlParser(XmlParser):
    def _validate_file(self, path):
        _REGEX_LITERAL = re.compile(r'^<project name=".*?" app=".*? http:\/\/snap.berkeley.edu" version=".*?">')
        super(SnapXmlParser, self)._validate_file(path)

        with open(path, 'r') as snap_xml:
            # Only read the first 4096 bytes, as the project directive should be at the top of the file.
            # (Let's hope their project name is not massive!)
            if re.match(_REGEX_LITERAL, snap_xml.read(4096)) is None:
                # Tests if the regex does not match the first 4096 bytes.
                raise UnsupportedFiletypeError('{} is not a supported snap xml. Aborting.'.format(path))
