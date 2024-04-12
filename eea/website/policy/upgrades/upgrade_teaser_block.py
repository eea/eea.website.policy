""" Upgrade teaserBlock to gridBlock """

from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.blocks import visit_blocks
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.lifecycleevent import modified

import logging
import transaction

logger = logging.getLogger("convert_teaser_to_grid_block")
logger.setLevel(logging.INFO)


def convert_teaser_to_grid_block(block_data):
    "Convert block_data to gridBlock"
    grid_block = block_data.copy()

    grid_block["@type"] = "gridBlock"
    grid_block["blocks_layout"] = {
        "items": [column["id"] for column in block_data["columns"]]
    }
    grid_block["blocks"] = {x["id"]: x for x in block_data["columns"]}
    del grid_block["columns"]
    return grid_block


def upgrade_teaser_block(portal):
    """Upgrade all teaserGrid blocks to gridBlock"""
    i = 0
    output = ""
    for brain in portal.portal_catalog(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        obj = brain.getObject()
        blocks = obj.blocks
        logger.info(f"Processing {obj.absolute_url()}")
        output += f"Processing {obj.absolute_url()}\n"
        # retrive block data from the item
        for block in visit_blocks(obj, blocks):
            # we have found a teaserGrid
            if block.get("@type", False) and block["@type"] == "teaserGrid":
                new_block = block.copy()
                new_block = convert_teaser_to_grid_block(block)
                block.clear()
                block.update(new_block)
                logger.info(f"{obj.absolute_url()} - Updated")
                output += f"{obj.absolute_url()} - Updated \n"

        obj.blocks = blocks
        modified(obj)
        i += 1
        if not i % 100:
            logger.info(i)
            transaction.commit()
    transaction.commit()
    return output
