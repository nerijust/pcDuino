#!/usr/bin/env python
#
# nerijust.com
# https://github.com/nerijust/pcDuino.git
# broadcast server example from https://github.com/tavendo


import sys
from gpio import *

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS


for i in range (14): 
	GPIO_MODE(i, OUTPUT) 						# make all GPIO output.

for i in range (14):
	GPIO_DATA(i, LOW) 							# make all GPIO low.
							   
class BroadcastServerProtocol(WebSocketServerProtocol):

	def onOpen(self):
		self.factory.register(self)

	def onMessage(self, msg, binary):
		if not binary:
			if msg == "refresh": 					# on message "refresh" check GPIO status and send info to client
				for i in range (0,14):
					status = str(GPIO_STATUS(i))
					msg = str(i)+":"+status
					print "sending echo:", msg
					self.factory.broadcast(msg)
		
			else: 									# at now client send only two types of messages 
				a = msg.split(':')[0]				# "refresh" and request to change GPIO status.
				b = msg.split(':')[1]				# So here is code for change GPIO status (ON/OFF).
				GPIO_DATA(a, b)
				self.factory.broadcast(msg)
		
			

	def connectionLost(self, reason):
		WebSocketServerProtocol.connectionLost(self, reason)
		self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
	"""
	Simple broadcast server broadcasting any message it receives to all
	currently connected clients.
	"""

	def __init__(self, url, debug = False, debugCodePaths = False):
		WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
		self.clients = []
      
	def register(self, client):
		if not client in self.clients:
			print "registered client " + client.peerstr
			self.clients.append(client)

	def unregister(self, client):
		if client in self.clients:
			print "unregistered client " + client.peerstr
			self.clients.remove(client)

	def broadcast(self, msg):
		print "broadcasting message '%s' .." % msg
		for c in self.clients:
			c.sendMessage(msg)
			print "message sent to " + c.peerstr


class BroadcastPreparedServerFactory(BroadcastServerFactory):
	"""
	Functionally same as above, but optimized broadcast using
	prepareMessage and sendPreparedMessage.
	"""

	def broadcast(self, msg):
		print "broadcasting prepared message '%s' .." % msg
		preparedMsg = self.prepareMessage(msg)
		for c in self.clients:
			c.sendPreparedMessage(preparedMsg)
			print "prepared message sent to " + c.peerstr


if __name__ == '__main__':

	if len(sys.argv) > 1 and sys.argv[1] == 'debug':
		log.startLogging(sys.stdout)
		debug = True
	else:
		debug = False

	ServerFactory = BroadcastServerFactory
	#ServerFactory = BroadcastPreparedServerFactory

	factory = ServerFactory("ws://localhost:9000",
							debug = debug,
							debugCodePaths = debug)

	factory.protocol = BroadcastServerProtocol
	factory.setProtocolOptions(allowHixie76 = True)
	listenWS(factory)

	webdir = File(".")
	web = Site(webdir)
	reactor.listenTCP(8080, web)

	reactor.run()

