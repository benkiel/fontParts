import weakref
from fontParts.base.errors import FontPartsError
from fontParts.base.base import (
    BaseObject, TransformationMixin, dynamicProperty)
from fontParts.base import normalizers
from fontParts.base.deprecated import DeprecatedSegment


class BaseSegment(BaseObject, TransformationMixin, DeprecatedSegment):

    def _setPoints(self, points):
        assert not hasattr(self, "_points")
        self._points = points

    def __eq__(self, other):
        if hasattr(other, "points"):
            return self.points == other.points
        return False

    def _reprContents(self):
        contents = [
            "%s" % self.type,
        ]
        if self.index is not None:
            contents.append("index='%r'" % self.index)
        return contents

    # -------
    # Parents
    # -------

    def getParent(self):
        """
        This is a backwards compatibility method.
        """
        return self.contour

    # Contour

    _contour = None

    contour = dynamicProperty("contour", "The segment's parent contour.")

    def _get_contour(self):
        if self._contour is None:
            return None
        return self._contour()

    def _set_contour(self, contour):
        assert self._contour is None
        if contour is not None:
            contour = weakref.ref(contour)
        self._contour = contour

    # Glyph

    glyph = dynamicProperty("glyph", "The segment's parent glyph.")

    def _get_glyph(self):
        if self._contour is None:
            return None
        return self.contour.glyph

    # Layer

    layer = dynamicProperty("layer", "The segment's parent layer.")

    def _get_layer(self):
        if self._contour is None:
            return None
        return self.glyph.layer

    # Font

    font = dynamicProperty("font", "The segment's parent font.")

    def _get_font(self):
        if self._contour is None:
            return None
        return self.glyph.font

    # --------------
    # Identification
    # --------------

    index = dynamicProperty("base_index", "The index of the segment within the ordered list of the parent contour's segments.")

    def _get_base_index(self):
        if self.contour is None:
            return None
        value = self._get_index()
        value = normalizers.normalizeIndex(value)
        return value

    def _get_index(self):
        """
        Subclasses may override this method.
        """
        contour = self.contour
        value = contour.segments.index(self)
        return value

    # ----------
    # Attributes
    # ----------

    type = dynamicProperty("base_type", "The segment type. The possible types are move, line, curve, qcurve.")

    def _get_base_type(self):
        value = self._get_type()
        value = normalizers.normalizeSegmentType(value)
        return value

    def _set_base_type(self, value):
        value = normalizers.normalizeSegmentType(value)
        self._set_type(value)

    def _get_type(self):
        """
        Subclasses may override this method.
        """
        value = self.onCurve.type
        return value

    def _set_type(self, newType):
        """
        Subclasses may override this method.
        """
        oldType = self.type
        if oldType == newType:
            return
        contour = self.contour
        if contour is None:
            raise FontPartsError("The segment does not belong to a contour.")
        # converting line <-> move
        if newType in ("move", "line") and oldType in ("move", "line"):
            pass
        # converting to a move or line
        elif newType not in ("curve", "qcurve"):
            offCurves = self.offCurve
            for point in offCurves:
                contour.removePoint(point)
        # converting a line/move to a curve/qcurve
        else:
            segments = contour.segments
            i = segments.index(self)
            prev = segments[i - 1].onCurve
            on = self.onCurve
            x = on.x
            y = on.y
            points = contour.points
            i = points.index(on)
            contour.insertPoint(i, (x, y), "offcurve")
            off2 = contour.points[i]
            contour.insertPoint(i, (prev.x, prev.y), "offcurve")
            off1 = contour.points[i]
            del self._points
            self._setPoints((off1, off2, on))
        self.onCurve.type = newType

    smooth = dynamicProperty("base_smooth", "Boolean indicating if the segment is smooth or not.")

    def _get_base_smooth(self):
        value = self._get_smooth()
        value = normalizers.normalizeBoolean(value)
        return value

    def _set_base_smooth(self, value):
        value = normalizers.normalizeBoolean(value)
        self._set_smooth(value)

    def _get_smooth(self):
        """
        Subclasses may override this method.
        """
        return self.onCurve.smooth

    def _set_smooth(self, value):
        """
        Subclasses may override this method.
        """
        self.onCurve.smooth = value

    # ------
    # Points
    # ------

    def __getitem__(self, index):
        return self._getItem(index)

    def _getItem(self, index):
        """
        Subclasses may override this method.
        """
        return self.points[index]

    def __iter__(self):
        return self._iterPoints()

    def _iterPoints(self, **kwargs):
        """
        Subclasses may override this method.
        """
        points = self.points
        count = len(points)
        index = 0
        while count:
            yield points[index]
            count -= 1
            index += 1

    def __len__(self):
        return self._len()

    def _len(self, **kwargs):
        """
        Subclasses may override this method.
        """
        return len(self.points)

    points = dynamicProperty("base_points", "A list of points in the segment.")

    def _get_base_points(self):
        return tuple(self._get_points())

    def _get_points(self):
        """
        Subclasses may override this method.
        """
        return tuple(self._points)

    onCurve = dynamicProperty("base_onCurve", "The on curve point in the segment.")

    def _get_base_onCurve(self):
        return self._get_onCurve()

    def _get_onCurve(self):
        """
        Subclasses may override this method.
        """
        return self.points[-1]

    offCurve = dynamicProperty("base_offCurve", "The off curve points in the segment.")

    def _get_base_offCurve(self):
        """
        Subclasses may override this method.
        """
        return self._get_offCurve()

    def _get_offCurve(self):
        """
        Subclasses may override this method.
        """
        return self.points[:-1]

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, origin=None, originOffset=None, **kwargs):
        """
        Subclasses may override this method.
        """
        for point in self.points:
            point.transformBy(matrix, origin=origin)

    # ----
    # Misc
    # ----

    def round(self):
        """
        Round coordinates in all points.
        """
        for point in self.points:
            point.round()
