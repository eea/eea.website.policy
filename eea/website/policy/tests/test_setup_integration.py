"""Integration tests for eea.website.policy setup."""

import unittest

from plone import api

from eea.website.policy.testing import EEA_WEBSITE_POLICY_INTEGRATION_TESTING

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that eea.website.policy is properly installed."""

    layer = EEA_WEBSITE_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if eea.website.policy is installed."""
        self.assertTrue(self.installer.is_product_installed("eea.website.policy"))

    def test_browserlayer(self):
        """Test that browser layer is registered."""
        from plone.browserlayer import utils

        from eea.website.policy.interfaces import IEeaWebsitePolicyLayer

        self.assertIn(IEeaWebsitePolicyLayer, utils.registered_layers())


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
