import sys
import socket
import math
from decimal import *
getcontext().prec = 4

serverip = raw_input("Ip:")
serverport = 7778
#serverip = "10.10.20.241"

class timers(object):
	def __init__(self):
		self.time = 0
		self.iocheck = 0
		self.iointerval = 300
timer = timers()

class yetCreep(object):
	def __init__(self, coord, time, type):
		self.type = input[2]
		self.coord = input[0]
		self.time = input[1]
	def buildNew(self):
		return CreepEnm(self.type, self.coord)

def cuttofour(number):
	number = str(number)
	leng = len(number)
	if leng > 4:
		print "Packet too long. Cutting " + str(int(number)-int(number[:4])) + " digits"
		number = number[:4]
	if leng < 4:
		rand = 4-leng
		#print "splicing " + str(rand) + " leading zeros"
		for i in range(rand):
			number = "0"+number
	return number

class player(object):
    def __init__(self, clientsocket, address):
        #fancy connection stuff
        self.s = clientsocket
        self.ip = address[0]
        self.port = address[1]
        self.connected = True
        
    def myreceive(self):
        #Recieve quantity of words
        chunks = []
        bytes_recd = 0
        while bytes_recd < 4 and self.connected:
            chunk = self.s.recv(min(4 - bytes_recd, 2048))
            if chunk == '':
                self.connected = False
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        if self.connected:
            MSGLEN = int(''.join(chunks))
            #recieve the words
            chunks = []
            bytes_recd = 0
            while bytes_recd < MSGLEN and self.connected:
                chunk = self.s.recv(min(MSGLEN - bytes_recd, 2048))
                if chunk == '':
                    self.connected = False
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
            return ''.join(chunks)
        
    def sendinfo(self, typewords):
        #send size of packet
        try:
            msg = cuttofour(len(typewords))
            totalsent = 0
            while totalsent < 4:
                sent = self.s.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                    break
                totalsent = totalsent + sent
            #send packet
            totalsent = 0
            while totalsent < int(msg):
                sent = self.s.send(typewords[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                    break
                totalsent = totalsent + sent
        except socket.error:
            self.connected = False

def getwords(input, quant):
    retreving = True
    words = []
    while retreving:
        word = ""
        getting = True
        for i in input:
            if i == " " and getting:
                words.append(word)
                word = ""
                if len(words)+1 >= quant:
                    getting = False
            else:
                word = word+i
        words.append(word)
        if len(words) == quant:
            return words
            retreving = False
        else:
            print "Missing "+str(quant-len(words))+" values"
		
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
isHost = raw_input("Are you the host?")	
if "y" in isHost:
	isHost = True
	print "Setting up as Host, waiting for client"
	#become a server socket
	s.bind((socket.gethostname(), serverport))
	s.listen(5)
	(clientsocket, address) = s.accept()
	thisplayer = player(clientsocket, address)
	
else:
	isHost = False
	print "Setting up as Client."
	s.connect((serverip, serverport))
	thisplayer = player(s, [serverip, serverport])
	print "waiting for host machine"
	print thisplayer.myreceive()
	
friendcreeps = []
enmcreeps = []
yetcreeps = []


while True:
	timer.time += 1
	timer.iocheck += 1
	if timer.iocheck >= timer.iointerval:
		timer.iocheck, outgoing, outnumber = 0, "", 0
		#Set tosend as list of strings: "50 40 normal", coord, time delay, type
		for i in tosend:
			outgoing += " " + str(i)
			outnumber += 3
		
		if isHost:
			thisplayer.sendinfo(outnumber + outgoing)
			recieved = thisplayer.myreceive()
		else:
			recieved = thisplayer.myreceive()
			thisplayer.sendinfo(outgoing)
		tosend, recieved = [], getwords(recieved, 2)
		
		#assuming recieved is list, not who won
		theinfo = getwords(recieved[1], 3*int(recieved[0]))
		rand = []
		for i in range(len(theinfo)):
			rand.append[theinfo[i]]
			if (i+1)%3 == 0:
				yetcreeps.append(yetCreep(rand))
				rand = []
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
