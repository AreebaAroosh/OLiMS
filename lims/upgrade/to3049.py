from dependencies.dependency import aq_inner
from dependencies.dependency import aq_parent
from dependencies.dependency import getToolByName
from lims.permissions import *
from lims.setuphandlers import BikaGenerator
from lims import logger

def upgrade(tool):
    """ Sort by Type in instruments
    """
    # Hack prevent out-of-date upgrading
    # Related: PR #1484
    # https://github.com/bikalabs/Bika-LIMS/pull/1484
    from lims.upgrade import skip_pre315
    if skip_pre315(aq_parent(aq_inner(tool))):
        return True


    portal = aq_parent(aq_inner(tool))
    bsc = getToolByName(portal, 'bika_setup_catalog', None)

    if 'getInstrumentType' not in bsc.indexes():
        bsc.addIndex('getInstrumentType', 'FieldIndex')
        bsc.addColumn('getInstrumentType')

        bsc.addIndex('getInstrumentTypeName','FieldIndex')
        bsc.addColumn('getInstrumentTypeName')

    #Del old "getType" Index, it's not used now.
    if 'getType' in bsc.indexes():
        bsc.delIndex('getType')
    if 'getType' in bsc.indexes():
        bsc.delColumn('getType')

    setup = portal.portal_setup

    logger.info("Reindex added indexes in bika_setup_catalog")
    bsc.manage_reindexIndex(
        ids=['getInstrumentType', 'getInstrumentTypeName', ])

    return True
