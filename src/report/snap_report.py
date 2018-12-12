""" CodeDiff - A file differencer for use in APCS(P) classes.
    See codediff executable for copyright disclaimer.
"""
import itertools
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
        self.cvars = [SnapVariable(**x.attrib) for x in self.project.find('variables')]

    def _stagefrometreeelem(self, elem):
        sprites = [SnapSprite(**x.attrib) for x in elem.find('sprites') if x.tag == 'sprite']
        return SnapStage(sprites, **elem.attrib)

    def elems(self):
        return 3 + self.stage.elems() + sum([x.elems() for x in self.blocks]) + sum([x.elems() for x in self.cvars])

    def getstageelems(self):
        return self.stage.__iter__()

    def getblockselems(self):
       return [(yield from x.iterelems()) for x in self.blocks]

    def getcvarselems(self):
       return [(yield from x.iterelems()) for x in self.cvars]

    def iterelems(self):
        """Iterates through all the (sub)elements of the report.

        :returns: An iterator for all (sub)elements, as a key-value tuple.
        """
        # Take all attributes into dictionary except for the stage, blocks, and
        # custom variables
        itr = {key: value for key, value in self.__dict__.items() if key not in ('stage', 'blocks', 'cvars')}
        # Chain the `itr` iterator and the stage, blocks and custom variable iterators
        chn = itertools.chain(itr.items(), self.stage.iterelems(),
                              [(yield from x.iterelems()) for x in self.blocks],
                              [(yield from x.iterelems()) for x in self.cvars])
        yield from chn

    def __iter__(self):
        yield from self.__dict__.items()


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

    def elems(self):
        # Subtract one for sprites
        return sum([x.elems() for x in self.sprites]) + len(self.__dict__) - 1

    def getspriteselems(self):
       return [(yield from x.iterelems()) for x in self.sprites]

    def iterelems(self):
        """Iterates through all the (sub)elements of the report.

        :returns: An iterator for all (sub)elements, as a key-value tuple.
        """
        # Take all attributes into dictionary except the sprites.
        chn = itertools.chain(self.__iter__(), [(yield from x.iterelems()) for x in self.sprites])
        yield from chn

    def __iter__(self):
        yield from {key: value for key, value in self.__dict__.items() if key != 'sprites'}


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

    def iterelems(self):
        yield from self.__dict__.items()

    def elems(self):
        return len(self.__dict__)

    def __iter__(self):
        yield from self.__dict__.items()


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

    def iterelems(self):
        yield from self.__dict__.items()

    def elems(self):
        return len(self.__dict__)


class SnapVariable:
    def __init__(self, **kwargs):
        dict_verify(kwargs, ('name', 'transient="false"'))
        self.name = kwargs['name']
        self.transient = kwargs['transient']

    def iterelems(self):
        yield from self.__dict__.items()

    def elems(self):
        return len(self.__dict__)
