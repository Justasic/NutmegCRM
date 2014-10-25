#!/usr/bin/twistd -ny
import sys, os

from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor, protocol

#######################################################################

# Port to listen on 
PORT = 8000

# Environment setup for your Django project files:
sys.path.append("NutmegCRM")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

############################\############################################
class Root(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource


class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()


# Import our django stuff.
from django.core.wsgi import get_wsgi_application

# Twisted Application Framework setup:
application = service.Application('twisted-django')


# WSGI container for Django, combine it with twisted.web.Resource:
# XXX this is the only 'ugly' part: see the 'getChild' method in twresource.Root 
# The MultiService allows to start Django and Twisted server as a daemon.

multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)
wresource = wsgi.WSGIResource(reactor, tps.pool, get_wsgi_application())
root = Root(wresource)

# Servce Django media files off of /media:
mediasrc = static.File(os.path.join(os.path.abspath("."), "NutmegCRM/media"))
staticsrc = static.File(os.path.join(os.path.abspath("."), "NutmegCRM/static"))
root.putChild("media", mediasrc)
root.putChild("static", staticsrc)

# The cool part! Add in pure Twisted Web Resouce in the mix
# This 'pure twisted' code could be using twisted's XMPP functionality, etc:
#root.putChild("google", twresource.GoogleResource())

# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(multi)
multi.setServiceParent(application)

