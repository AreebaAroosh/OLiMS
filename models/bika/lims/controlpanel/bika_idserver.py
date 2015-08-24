from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import InitializeClass
from dependencies.dependency import SimpleItem
from dependencies.dependency import permissions
from dependencies.dependency import getToolByName
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import t
from bika.lims.interfaces import IIdServer
from dependencies.dependency import implements
from dependencies.dependency import sha1
import App,os,sys,random,time,urllib,hmac

try:
    from dependencies.dependency import getSite
except:
    # Plone < 4.3
    from dependencies.dependency import getSite

class IDServerUnavailable(Exception):
    pass

class bika_idserver(object):

    implements(IIdServer)
    security = ClassSecurityInfo()

    security.declarePublic('generate_id')
    def generate_id(self, portal_type, batch_size = None):
        """ Generate a new id for 'portal_type'
        """
        plone = getSite()
        portal_id = plone.getId()

        if portal_type == 'News Item':
            portal_type = 'NewsItem'

        idserver_url = os.environ.get('IDServerURL')
        try:
            if batch_size:
                # GET
                f = urllib.urlopen('%s/%s%s?%s' % (
                        idserver_url,
                        portal_id,
                        portal_type,
                        urllib.urlencode({'batch_size': batch_size}))
                        )
            else:
                f = urllib.urlopen('%s/%s%s' % (
                    idserver_url, portal_id, portal_type
                    )
                )
            id = f.read()
            f.close()
        except:
            from sys import exc_info
            info = exc_info()
            import zLOG; zLOG.LOG('INFO', 0, '', 'generate_id raised exception: %s, %s \n idserver_url: %s' % (info[0], info[1], idserver_url))
            raise IDServerUnavailable(_('ID Server unavailable'))
        return id
