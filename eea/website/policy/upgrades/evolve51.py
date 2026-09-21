"""Upgrade step to install EPANET context navigation actions."""

import logging

logger = logging.getLogger("eea.website.policy")


def add_epanet_context_navigation_actions(context):
    """Import only the actions step from the default profile.

    This creates the EPANET ``context_navigation`` action category and its
    actions without touching any other site configuration.
    """
    context.runImportStepFromProfile(
        "profile-eea.website.policy:default", "actions", run_dependencies=False
    )
    logger.info("Imported EPANET context_navigation actions")
