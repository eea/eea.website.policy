"""Upgrade step to transform provider_url to resolve uid if the case"""

import os
import logging
import transaction
from zope.lifecycleevent import modified
from Products.ZCatalog.ProgressHandler import ZLogHandler
logger = logging.getLogger("eea.website.policy")


def upgrade_visualizations(portal):
    """
    Upgrade step to fix provider_url in visualizations.
    """
    i = 0
    brains = portal.portal_catalog(portal_type="visualization")
    pghandler = ZLogHandler(100)
    pghandler.init("Upgrade visualizations", len(brains))

    for idx, brain in enumerate(brains):
        pghandler.report(idx)
        try:
            obj = brain.getObject()
        except Exception:
            continue  # Skip objects that cannot be retrieved

        viz = getattr(obj, "visualization", None)

        if not viz or not isinstance(viz, dict):
            continue

        provider_url = viz.get("provider_url", None)

        if (
            provider_url and
            "resolveuid" in provider_url and
            provider_url.startswith("../")
        ):
            path = os.path.join(obj.absolute_url(1), provider_url)
            normpath = os.path.normpath(path)
            if not normpath.startswith("www/en"):
                provider_url = provider_url[3:]
                logger.warning(
                    "Fix visualization: %s. Normpath: %s. New provider_url: %s",
                    obj.absolute_url(), normpath, provider_url)
                viz["provider_url"] = provider_url
                obj.visualization = viz
                modified(obj)
                i += 1

        if i % 100 == 0:
            transaction.commit()

    pghandler.finish()
    transaction.commit()
