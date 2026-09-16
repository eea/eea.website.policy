"""Tests for the EEA Subsite customization wiring."""

import unittest
from pathlib import Path
from xml.etree import ElementTree


class SubsiteCustomizationTest(unittest.TestCase):
    """Verify the EEA behavior is enabled only through the website profile."""

    def test_profile_enables_main_logo_behavior(self):
        profile = (
            Path(__file__).parents[1] / "profiles" / "default" / "types" / "Subsite.xml"
        )
        root = ElementTree.parse(profile).getroot()
        behaviors = root.find("./property[@name='behaviors']")
        values = [element.attrib["value"] for element in behaviors]

        self.assertIn("eea.subsite_logo_main", values)


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
