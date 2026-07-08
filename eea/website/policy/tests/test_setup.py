"""Tests for setup handlers."""

import unittest

from eea.website.policy.setuphandlers import HiddenProfiles


class TestHiddenProfiles(unittest.TestCase):
    """Test HiddenProfiles."""

    def setUp(self):
        self.hidden = HiddenProfiles()

    def test_get_non_installable_profiles(self):
        """Test that uninstall profiles are hidden."""
        profiles = self.hidden.getNonInstallableProfiles()
        self.assertIsInstance(profiles, list)
        self.assertIn("eea.website.policy:languages", profiles)
        self.assertIn("eea.website.policy:uninstall", profiles)

    def test_profiles_are_strings(self):
        """Test that all profile entries are strings."""
        profiles = self.hidden.getNonInstallableProfiles()
        for profile in profiles:
            self.assertIsInstance(profile, str)

    def test_no_installable_profile_leaked(self):
        """Test that the default profile is NOT hidden."""
        profiles = self.hidden.getNonInstallableProfiles()
        self.assertNotIn("eea.website.policy:default", profiles)


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
