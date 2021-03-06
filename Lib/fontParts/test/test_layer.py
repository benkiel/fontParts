import unittest
from fontParts.base import FontPartsError


class TestLayer(unittest.TestCase):

    # ------
    # Glyphs
    # ------

    def getLayer_glyphs(self):
        layer, unrequested = self.objectGenerator("layer")
        for name in "ABCD":
            glyph = layer.newGlyph(name)
        return layer, unrequested

    # len

    def test_len(self):
        layer, unrequested = self.getLayer_glyphs()
        self.assertEqual(
            len(layer),
            4
        )