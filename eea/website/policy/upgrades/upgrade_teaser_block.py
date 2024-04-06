""" Upgrade to version 4.0
"""
# pylint: disable=line-too-long
import logging
from Products.CMFCore.utils import getToolByName
from eea.dexterity.indicators.interfaces import IIndicator

logger = logging.getLogger("eea.dexterity.indicators")


def convert_teaserGrid_to_gridblock(block_data):
     grid_block = block_data.copy()
     grid_block["@type"] = "gridBlock"
     grid_block["blocks_layout"] = {
          "items":list(map(lambda column:column["id"],block_data["columns"]))
          }
     grid_block["blocks"] ={x["id"] : x for x in block_data["columns"]}
     del grid_block["columns"]
     return grid_block
                         
def upgrade_teaser_block(context):
    """ Fix Indicator schema """
    ctool = getToolByName(context, "portal_catalog")
    #create a list of all content from the site
    docsBrain = list(ctool.getAllBrains())
    for brain in docsBrain:
        #retrive block data from the item 
        doc = brain.getObject()
        blocks = getattr(doc, "blocks", None)
        for key in blocks.keys():
                if blocks[key]["@type"] == "teaserGrid":
                   blocks[key] = convert_teaserGrid_to_gridblock(blocks[key])
                   print(blocks[key])
        doc.blocks = blocks;

                     
                     
                       
   

