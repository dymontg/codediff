""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
from src.report import BaseFileReport
from src.utils import dict_verify


# Currently we simply do a shallow parse.
class SnapReport(BaseFileReport):
    def __init__(self, path, **kwargs):
        # Turn etree elements into snap reports
        super(SnapReport, self).__init__(path)
        self.project = kwargs['project']
        self.name = kwargs['name']
        self.stage = self._stagefrometreeelem(kwargs['stage'])
        self.blocks = [SnapBlock(**x.attrib) for x in self.project.find('blocks')]
        self.vars = [SnapVariable(**x.attrib) for x in self.project.find('variables')]

    def _stagefrometreeelem(self, elem):
        sprites = [SnapSprite(**x.attrib) for x in elem.find('sprites') if x.tag == 'sprite']
        return SnapStage(sprites, **elem.attrib)


class SnapNotes:
    pass


class SnapStage:
    def __init__(self, sprites, **kwargs):
        dict_verify(kwargs, ('name', 'width', 'height',
                             'costume', 'tempo', 'threadsafe',
                             'lines', 'ternary', 'codify', 'inheritance',
                             'sublistIDs', 'scheduled', 'id'))
        self.sprites = sprites
        self.name = kwargs['name']
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.costume = kwargs['costume']


class SnapSprite:
    def __init__(self, **kwargs):
        dict_verify(kwargs, ('name', 'idx', 'x', 'y',
                             'heading', 'scale', 'rotation',
                             'draggable', 'costume', 'color',
                             'pen', 'id', 'hidden="false"'))
        self.spriteid = kwargs['id']
        self.name = kwargs['name']
        self.posx = float(kwargs['x'])
        self.posy = float(kwargs['y'])
        self.idx = int(kwargs['idx'])
        self.hdg = float(kwargs['heading'])
        self.scl = float(kwargs['scale'])
        self.rot = float(kwargs['rotation'])
        self.draggable = bool(kwargs['draggable'])
        self.costume = int(kwargs['costume'])
        self.color = kwargs['color']
        self.pen = kwargs['pen']
        self.hidden = bool(kwargs['hidden'])

class SnapHidden:
    pass


class SnapHeaders:
    pass


class SnapCode:
    pass


class SnapBlock:
    def __init__(self, **kwargs):
        dict_verify(kwargs, ('s', 'type', 'category'))
        self.name = kwargs['s']
        self.typ = kwargs['type']
        self.cat = kwargs['category']


class SnapVariable:
    def __init__(self, name):
        self.name = name
