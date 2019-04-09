#!/usr/bin/python

SOCKET_SRC_PORT     = 9995
SOCKET_DST_PORT     = 9996
WEBSOCKET_DST_PORT  = 9997

import sys
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
try:
    from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
except:
    from autobahn.websocket import WebSocketServerProtocol, WebSocketServerFactory

import datetime

socketClients = []
webSocketClients = []

def log(*args):
    print '[%s] %s' % (str(datetime.datetime.now()), ' '.join([str(a) for a in args]))


class NotifierSource(LineReceiver):

    def connectionMade(self):
        log("NotifierSource.connectionMade: Source connected:", self.transport.getPeer())

    def connectionLost(self, reason):
        log("NotifierSource.connectionLost: Source disconnected:", self.transport.getPeer(), ".. Reason:", reason)

    def lineReceived(self, line):
        log("NotifierSource.lineReceived: (writing to %d+%d clients): %s" % (len(socketClients), len(webSocketClients), line))
        for protocol in socketClients:
            protocol.sendData(line)
        for protocol in webSocketClients:
            protocol.sendMessage(line, False)

class NotifierSocketDestination(Protocol):

    def connectionMade(self):
        socketClients.append(self)
        log("NotifierSocketDestination.connectionMade: added to socketClients list (socketClients count: %d):" % len(socketClients), self.transport.getPeer())

    def connectionLost(self, reason):
        if self in socketClients:
            socketClients.remove(self)
            log("NotifierSocketDestination.connectionLost: removed from socketClients list (socketClients count: %d).. Reason:" % len(socketClients), reason)
        else:
            log("NotifierSocketDestination.connectionLost: Reason:", reason)

    def dataReceived(self, data):
        log("NotifierSocketDestination.lineReceived: %s" % data)

    def sendData(self, data):
        if data:
            self.transport.write(data.rstrip() + "\r\n")


class NotifierWebSocketDestination(WebSocketServerProtocol):

    def onConnect(self, request):
        webSocketClients.append(self)
        log("NotifierWebSocketDestination.connectionMade: added to webSocketClients list: webSocketClients count: %d:" % len(webSocketClients), request.peer)

    def onOpen(self):
        log("NotifierWebSocketDestination.onOpen: WebSocket connection open")

    def onMessage(self, payload, isBinary):
        if isBinary:
            log("NotifierWebSocketDestination.onMessage: Binary message received: {0} bytes".format(len(payload)))
        else:
            log("NotifierWebSocketDestination.onMessage: Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        if self in webSocketClients:
            webSocketClients.remove(self)
            log("NotifierWebSocketDestination.connectionLost: removed from webSocketClients list (webSocketClients count: %d).. Reason:" % len(webSocketClients), reason)
        else:
            log("NotifierWebSocketDestination.connectionLost: Reason:", reason)

sourceFactory = Factory()
sourceFactory.protocol = NotifierSource

socketDestFactory = Factory()
socketDestFactory.protocol = NotifierSocketDestination

webSocketDestFactory = WebSocketServerFactory(u"ws://127.0.0.1:%d" % WEBSOCKET_DST_PORT)
webSocketDestFactory.protocol = NotifierWebSocketDestination

reactor.listenTCP(SOCKET_SRC_PORT, sourceFactory)
reactor.listenTCP(SOCKET_DST_PORT, socketDestFactory)
reactor.listenTCP(WEBSOCKET_DST_PORT, webSocketDestFactory)
print "----- Running reactor notifier -----"
reactor.run()
