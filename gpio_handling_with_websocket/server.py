#!/usr/bin/env python
#
# nerijust.com
# https://github.com/nerijust/pcDuino.git


import sys
import os
from gpio import *
from twisted.internet import reactor
from twisted.python import log

 
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS
for i in range (14): 
	GPIO_MODE(i, OUTPUT)

for i in range (14):
	GPIO_DATA(i, LOW)

class EchoServerProtocol(WebSocketServerProtocol):
 
    def onMessage(self, msg, binary):
		a = msg.split(':')[0]
		b = msg.split(':')[1]
		GPIO_DATA(a, b)
		print "sending echo:", msg
		self.sendMessage(msg, binary)
		

 
if __name__ == '__main__':
 
   log.startLogging(sys.stdout)
 
   factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
   factory.protocol = EchoServerProtocol
   listenWS(factory)
 
   reactor.run()
