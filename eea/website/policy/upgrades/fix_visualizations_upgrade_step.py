"""Upgrade step to transform provider_url to resolve uid if the case"""
from urllib.parse import urlparse
import transaction
from zope.lifecycleevent import modified
from Products.ZCatalog.ProgressHandler import ZLogHandler
from plone.restapi.deserializer.utils import path2uid
import re


def upgrade_visualizations(portal):
    """
    Upgrade step to fix provider_url in visualizations.
    """
    i = 0
    brains = portal.portal_catalog(portal_type="viz")
    pghandler = ZLogHandler(100)
    pghandler.init("Upgrade visualizations", len(brains))

    for idx, brain in enumerate(brains):
        pghandler.report(idx)
        try:
            obj = brain.getObject()
        except Exception:
            continue  # Skip objects that cannot be retrieved

        viz = getattr(obj, 'visualization', None)

        if not viz or not isinstance(viz, dict):
            continue

        provider_url = viz.get('provider_url', None)

        if provider_url and 'resolveuid' in provider_url and  viz['provider_url'].startswith("../"):
            viz['provider_url'] =  viz['provider_url'][3:];
            obj.visualization = viz
            modified(obj)
            i += 1

        if i % 100 == 0:
            transaction.commit()

    pghandler.finish()
    transaction.commit()