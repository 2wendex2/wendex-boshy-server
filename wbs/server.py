"""
Server with basic logging (with UDP)
"""

# try and run psyco for performance


from twisted.internet import reactor
from lacewing.server import ServerProtocol, ServerDatagram, ServerFactory
from dummy import DUMMY_PLAYER_NAME, DummyProtocol
from __init__ import __version__
from lacewing.multidict import MultikeyDict
from boshyframes import BOSHY_FRAMES

PROHIBITED_NICKNAMES = [
    'OnlineCoop', DUMMY_PLAYER_NAME
]

def getProtocolType(settings):
    if settings.get('datagram', False):
        return 'UDP'
    else:
        return 'TCP'


class WendexBoshyServer(ServerProtocol):
    def connectionAccepted(self, welcome):
        self.log('Client connection accepted.')

    def messageReceived(self, message):
        protocolType = getProtocolType(message.settings)
        if protocolType=='TCP':
            self.log('(%s) %s %r' % (protocolType, message.subchannel, message.value))
        
    def channelMessageReceived(self, channel, message):
        protocolType = getProtocolType(message.settings)
        if protocolType=='TCP':
            self.log('(%s)(%s) %s %r' % (protocolType, channel.name, message.subchannel, message.value))
        if message.value == "/ping":
            channel.sendMessage('pong', message.subchannel, self.factory.dummy,
                typeName = message.getDataType(), asObject = message.isObject,
                asDatagram = message.settings.get('datagram', False))
        elif message.value == "/version":
            channel.sendMessage('Wendex boshy server v%s' % __version__, message.subchannel, self.factory.dummy,
                typeName = message.getDataType(), asObject = message.isObject,
                asDatagram = message.settings.get('datagram', False))
        else:
            splitted = message.value.split()
            if (len(splitted) == 4 and splitted[0] == '/save' and splitted[1] in BOSHY_FRAMES and
                splitted[2].isdigit() and splitted[3].isdigit()):
                channel.sendMessage('%s|%s|%s|%s' % (splitted[2], splitted[3], BOSHY_FRAMES[splitted[1]], 0), 63, self.factory.dummy,
                typeName = message.getDataType(), asObject = message.isObject,
                asDatagram = message.settings.get('datagram', False))

    def privateMessageReceived(self, channel, recipient, message):
        protocolType = getProtocolType(message.settings)
        if protocolType=='TCP':
            self.log('(%s)(to %s) %s %r' % (protocolType, recipient.name, message.subchannel, message.value))

    def loginAccepted(self, name):
        self.log('Name set to "%s"' % name)
        if name in PROHIBITED_NICKNAMES:
            self.log('PIZDEC')
            self.disconnect()
        
    def channelListSent(self):
        self.log('(sent channel list)')
        
    def channelJoined(self, channel):
        self.log('Signed on to channel "%s"' % channel.name)
        self.factory.dummy.joinChannelWeak(channel)
        
    def channelLeft(self, channel):
        self.log('Left channel "%s"' % channel.name)
        
    def nameChanged(self, name):
        self.log('Name changed to %s' % name)
        
    def connectionLost(self, reason):
        # here, we need to call OServer's connectionLost
        # because connectionLost is a twisted method, and the server
        # needs to know that the client has disconnected.
        ServerProtocol.connectionLost(self, reason)
        if self.loggedIn:
            self.log('Connection disconnected.')
    
    def disconnect(self, reason = None, *arg, **kw):
        print self.log('Kicked: %s' % reason)          
        ServerProtocol.disconnect(self, reason, *arg, **kw)
            
    def log(self, message):
        """
        Log a message.
        """
        print '%s: %s' % (self.id, message)
        
class WendexBoshyFactory(ServerFactory):
    protocol = WendexBoshyServer
    ping = True
    channelListing = True
    masterRights = True
    welcomeMessage = 'Wendex Boshy Server v' + __version__
    dummy = None
    
    def run(self, prt):
        try:
            import psyco
            psyco.full()
        except ImportError:
            pass
        
        port = reactor.listenTCP(prt, self)
        reactor.listenUDP(prt, ServerDatagram(self))
        print 'Opening new server on port %s...' % prt
        reactor.run()
    
    def startFactory(self):
        ServerFactory.startFactory(self)
        channels = MultikeyDict()
        self.dummy = DummyProtocol(self)
    
