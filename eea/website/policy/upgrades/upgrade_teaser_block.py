""" Upgrade teaserBlock to gridBlock 
"""

from Products.CMFCore.utils import getToolByName


def convert_teaser_grid_to_grid_block(block_data):
    grid_block = block_data.copy()

    grid_block["@type"] = "gridBlock"
    grid_block["blocks_layout"] = {
        "items": list(map(lambda column: column["id"], block_data["columns"]))
    }
    grid_block["blocks"] = {x["id"]: x for x in block_data["columns"]}
    del grid_block["columns"]
    return grid_block


def upgrade_teaser_block(context):
    """Upgrade all teaserGrid blocks to gridBlock"""
    ctool = getToolByName(context, "portal_catalog")
    # create a list of all content from the site
    brains_docs = list(ctool.getAllBrains())
    for brain in brains_docs:
        # retrive block data from the item
        doc = brain.getObject()
        blocks = getattr(doc, "blocks", [])
        for key in blocks.keys():
            # we have found a teaserGrid
            if blocks[key]["@type"] == "teaserGrid":
                blocks[key] = convert_teaser_grid_to_grid_block(blocks[key])
        doc.blocks = blocks
