#!/usr/bin/env python

############################################################################
#
# NAME:      interactivemap_test.py
#
# AUTHOR:    Caitlin Haedrich (caitlin dot haedrich gmail com)
#
# PURPOSE:   This is a test script for grass.jupyter's InteractiveMap
#
# COPYRIGHT: (C) 2021 by Caitlin Haedrich and the GRASS Development Team
#
#            This program is free software under the GNU General Public
#            License (>=v2). Read the file COPYING that comes with GRASS
#            for details.
#
#############################################################################


import os
import unittest
import sys
from pathlib import Path
import grass.jupyter as gj
from grass.gunittest.case import TestCase
from grass.gunittest.main import test


def can_import_folium():
    """Test folium import to see if test can be run."""
    try:
        import folium

        return True
    except ImportError:
        return False


class TestDisplay(TestCase):
    # Setup variables
    files = []

    @classmethod
    def setUpClass(cls):
        """Ensures expected computational region"""
        # to not override mapset's region (which might be used by other tests)
        cls.use_temp_region()
        # cls.runModule or self.runModule is used for general module calls
        # we'll use the elevation raster as a test display
        cls.runModule("g.region", raster="elevation")

    @classmethod
    def tearDownClass(cls):
        """Remove temporary region"""
        cls.del_temp_region()

    def tearDown(self):
        """
        Remove the PNG file created after testing with "filename =" option.
        This is executed after each test run.
        """
        for f in self.files:
            f = Path(f)
            if sys.version_info < (3, 8):
                try:
                    os.remove(f)
                except FileNotFoundError:
                    pass
            else:
                f.unlink(missing_ok=True)

    @unittest.skipIf(not can_import_folium(), "Cannot import folium")
    def test_basic(self):
        # Create InteractiveMap
        interactive_map = gj.InteractiveMap()
        interactive_map.add_raster("elevation")
        interactive_map.add_vector("roadsmajor")
        interactive_map.show()

    @unittest.skipIf(not can_import_folium(), "Cannot import folium")
    def test_save_as_html(self):
        # Create InteractiveMap
        interactive_map = gj.InteractiveMap()
        interactive_map.add_vector("roadsmajor")
        filename = "InteractiveMap_test.html"
        self.files.append(filename)
        interactive_map.save(filename)
        self.assertFileExists(filename)


if __name__ == "__main__":
    test()
