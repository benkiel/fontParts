import unittest
from fontParts.base import FontPartsError


class TestInfo(unittest.TestCase):

    def getInfo_generic(self):
        info, unrequested = self.objectGenerator("info")
        info.unitsPerEm = 1000
        return info, unrequested

    # ----------
    # Dimensions
    # ----------

    def test_unitsPerEm(self):
        info, unrequested = self.getInfo_generic()
        # get
        self.assertEqual(
            info.unitsPerEm,
            1000
        )
        # set: valid
        info.unitsPerEm = 2000
        self.assertEqual(
            info.unitsPerEm,
            2000
        )
        info.unitsPerEm = 2000.1
        self.assertEqual(
            info.unitsPerEm,
            2000.1
        )
        # set: invalid
        with self.assertRaises(FontPartsError):
            info.unitsPerEm = -1000
        with self.assertRaises(FontPartsError):
            info.unitsPerEm = "abc"