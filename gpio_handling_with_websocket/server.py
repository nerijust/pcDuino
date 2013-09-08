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
	GPIO_MODE(i, OUTPUT) 						# make all GPIO output.

for i in range (14):
	GPIO_DATA(i, LOW) 							# make all GPIO low.

class EchoServerProtocol(WebSocketServerProtocol):
 
    def onMessage(self, msg, binary):
	
		if msg == "refresh": 					# on message "refresh" check GPIO status and send info to client
			for i in range (0,14):
				status = str(GPIO_STATUS(i))
				msg = str(i)+":"+status
				print "sending echo:", msg
				self.sendMessage(msg, binary)
				
				
		else: 									# at now client send only two types of messages 
			a = msg.split(':')[0]				# "refresh" and request to change GPIO status.
			b = msg.split(':')[1]				# So here is code for change GPIO status (ON/OFF).
			GPIO_DATA(a, b)
			#print "sending echo:", msg
			#self.sendMessage(msg, binary)
		
if __name__ == '__main__':

   log.startLogging(sys.stdout)
 
   factory = WebSocketServerFactory("ws://192.168.1.4:9000", debug = False)
   factory.protocol = EchoServerProtocol
   listenWS(factory)
 
   reactor.run()
