
from lacewing.server import ServerProtocol
from lacewing.multidict import MultikeyDict

DUMMY_PLAYER_NAME = 'WBS'

class DummyProtocol(ServerProtocol):
    def __init__(self, factory):
        self.name = DUMMY_PLAYER_NAME
        self.id = factory.userPool.pop()
        self.channels = MultikeyDict()
        self.isAccepted = True
        self.loggedIn = True
        self.factory = factory
    
    def sendLoader(self, loader, asDatagram = False, **settings):
        pass
    
    def loaderReceived(self, loader, isDatagram = False):
        pass
    
    def joinChannelWeak(self, channelName):
        if channelName in self.channels:
            return
        try:
            channel, = self.factory.channels[channelName]
        except KeyError:
            pass
        channel = self.joinChannel(channelName, False, 
            False)