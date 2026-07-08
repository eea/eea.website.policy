"""Test layer for eea.website.policy."""

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile

import eea.website.policy


class EeaWebsitePolicyLayer(PloneSandboxLayer):
    """Test layer for eea.website.policy."""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=eea.website.policy)

    def setUpPloneSite(self, portal):
        """Set up Plone site."""
        applyProfile(portal, "eea.website.policy:default")


EEA_WEBSITE_POLICY_FIXTURE = EeaWebsitePolicyLayer()

EEA_WEBSITE_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_WEBSITE_POLICY_FIXTURE,),
    name="EeaWebsitePolicyLayer:IntegrationTesting",
)
