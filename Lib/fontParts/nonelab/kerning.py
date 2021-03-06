import defcon
from fontParts.base import BaseKerning, FontPartsError
from fontParts.nonelab.base import RBaseObject


class RKerning(RBaseObject, BaseKerning):

    wrapClass = defcon.Kerning

    def _items(self):
        return self.naked().items()

    def _contains(self, key):
        return key in self.naked()

    def _setItem(self, key, value):
        self.naked()[key] = value

    def _getItem(self, key):
        return self.naked()[key]

    def _delItem(self, key):
        del self.naked()[key]
