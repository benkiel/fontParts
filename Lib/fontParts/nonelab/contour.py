import defcon
from fontParts.base import BaseContour, FontPartsError
from fontParts.nonelab.base import RBaseObject
from fontParts.nonelab.point import RPoint
from fontParts.nonelab.segment import RSegment
from fontParts.nonelab.bPoint import RBPoint


class RContour(RBaseObject, BaseContour):

    wrapClass = defcon.Contour
    pointClass = RPoint
    segmentClass = RSegment
    bPointClass = RBPoint

    # --------------
    # Identification
    # --------------

    # index

    def _set_index(self, value):
        contour = self.naked()
        glyph = contour.glyph
        if value > glyph.contours.index(contour):
            value -= 1
        glyph.removeContour(contour)
        glyph.insertContour(value, contour)

    # identifier

    def _get_identifier(self):
        contour = self.naked()
        return contour.identifier

    def _generateIdentifier(self):
        contour = self.naked()
        return contour.generateIdentifier()

    def _generateIdentifierforPoint(self, point):
        contour = self.naked()
        point = point.naked()
        return contour.generateIdentifierforPoint(point)

    # ----
    # Open
    # ----

    def _get_open(self):
        return self.naked().open

    # ---------
    # Direction
    # ---------

    def _get_clockwise(self):
        return self.naked().clockwise

    def _reverseContour(self, **kwargs):
        self.naked().reverse()

    # ------
    # Points
    # ------

    def _lenPoints(self, **kwargs):
        return len(self.naked())

    def _getPoint(self, index, **kwargs):
        contour = self.naked()
        point = contour[index]
        return self.pointClass(point)

    def _insertPoint(self, index, position, type=None, smooth=None, name=None, identifier=None, **kwargs):
        point = self.pointClass()
        point.x = position[0]
        point.y = position[1]
        point.type = type
        point.smooth = smooth
        point.name = name
        point = point.naked()
        point.identifier = identifier
        self.naked().insertPoint(index, point)

    def _removePoint(self, index, **kwargs):
        contour = self.naked()
        point = contour[index]
        contour.removePoint(point)
