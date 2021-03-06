import unittest
from fontParts.base import FontPartsError


class TestGroups(unittest.TestCase):

    def getGroups_generic(self):
        groups, unrequested = self.objectGenerator("groups")
        groups.update({
            "group 1" : ["A", "B", "C"],
            "group 2" : ["x", "y", "z"],
            "group 3" : [],
            "group 4" : ["A"]
        })
        return groups, unrequested

    # ---
    # len
    # ---

    def test_len(self):
        groups, unrequested = self.getGroups_generic()
        self.assertEqual(
            len(groups),
            4
        )
        groups.clear()
        self.assertEqual(
            len(groups),
            0
        )

    # ---------
    # Searching
    # ---------

    def test_find(self):
        groups, unrequested = self.getGroups_generic()
        found = groups.findGlyph("A")
        found.sort()
        self.assertEqual(
            found,
            [u"group 1", u"group 4"]
        )
        self.assertEqual(
            groups.findGlyph("five"),
            []
        )
        # find: invalid
        with self.assertRaises(FontPartsError):
            groups.findGlyph(5)