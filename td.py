import random
import pygame
import pyganim
import time
import sys
import socket
import math
from decimal import *
getcontext().prec = 4
clock = pygame.time.Clock()


serverport = 7778

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
			return words
			retreving = False
			
		
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
	thisplayer.sendinfo("Connected")
	
else:
	isHost = False
	print "Setting up as Client."
	serverip = raw_input("Ip:")
	serverip = "192.168.1.35"
	s.connect((serverip, serverport))
	thisplayer = player(s, [serverip, serverport])
	print "waiting for host machine"
	print thisplayer.myreceive()

	
pygame.mixer.pre_init(22050, -16, 3, 8)
pygame.mixer.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREY = (100,100,100)
pygame.init()
size = (1250, 700)

gScreen = pygame.display.set_mode(size)

font = pygame.font.SysFont('Calibri', 15, True, False)
text = font.render("hi",True,BLACK)
 
pygame.display.set_caption("TD: THE MOST EPIC TD GAME EVER!")

done = False

def bubble_sort(items):
	""" Implementation of bubble sort """
	for i in range(len(items)):
		for j in range(len(items)-1-i):
			if items[j] > items[j+1]:
				items[j], items[j+1] = items[j+1], items[j] 
	return items
	
class SpreetSheet(object):
	def __init__(self, img, row, colm):
		self.img = img
		self.row = row
		self.colm = colm
		self.animation = pyganim.PygAnimation(list(zip(pyganim.getImagesFromSpriteSheet(self.img, rows = self.row, cols = self.colm, rects = []),[200] * self.row * self.colm)))
		self.animation.play()
	def image_at(self, rectangle):
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		return image
		
def hitDetect(p1, p2, p3, p4):
	if p2[0] > p3[0] and p1[0] < p4[0] and p2[1] > p3[1] and p1[1] < p4[1]:
		return True
		
def convertVel(input):
	
	radians = math.radians(input)
	x_vel = math.cos(radians)
	y_vel = -math.sin(radians)
	velocity = (x_vel, y_vel)
	return velocity		
	
def pointAt(source, point):
	deltax = source[0] - point[0]
	deltay = source[1] - point[1]
	angle = 0
	#upper left
	if deltax > 0 and deltay > 0:
		angle = 270 - math.atan((math.fabs(deltay))/(math.fabs(deltax))) + 90
	
	#lower left
	if deltax > 0 and deltay < 0:
		angle = 270 - math.atan(deltay/math.fabs(deltax)) + 90
		
	#upper right
	if deltax < 0 and deltay > 0:
		angle = math.atan(deltay/math.fabs(deltax))
	#lower right
	if deltax < 0 and deltay < 0:
		angle = math.atan(deltay/math.fabs(deltax))
	
	return math.degrees(angle)

class CreepEnm(object):
	def __init__(self, type, y):
		self.type = type
		self.cord = [0, y]
		self.tower = ""
		self.img = img
		if self.type == "normal":
			self.hp = 50
			self.spd = 2
			self.money = 25
		if self.type == "tower":
			self.hp = 50
			self.spd = 1
			self.money = 50

			
class CreepFrd(object):
	def __init__(self, img):
		self.tower = ""
		self.spd = 0
		self.size = (5, 100)
		self.center = (self.size[0] / 2, self.size[1] / 2)
		self.cord = [size[0] / 2, size[1] / 2]
		self.vel = [0,0]
		self.img = img
		self.baseimg = img
		self.angle = 0
		
	def update(self, mouse_pos):
		#self.cord[0] += self.vel[0] * self.spd
		#self.cord[1] += self.vel[1] * self.spd
		self.angle += 1
		self.img = pygame.transform.rotate(self.baseimg, pointAt(self.cord,mouse_pos))

		
	def sendOver():
		string = str(self.tower.name) + " " + timer.iocheck + " " + str(self.cord[1])
	
	def buildNew(self):
		newCreep = CreepFrd(pygame.image.load(self.img))
		newCreep.baseimg = newCreep.img
		return newCreep
		
testCreep = CreepFrd("Assets/images/creep.png")

testCreep = testCreep.buildNew()


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

class Tower(object):
	def __init__(self, name, type, hp, damage, cost, img):
		self.name = name
		self.type.type
		self.hp = hp
		self.damage = damage
		self.cost = cost
		self.pos = pos
		self.img = img
		
	def buildNew(self):
		newTower = Tower(self.name, self.hp, self.damage, self.cost, pygame.image.load(self.img))
		return newTower
	
friendcreeps = []
enmcreeps = []
yetcreeps = []
tosend = []

while not done:

	timer.time += 1
	timer.iocheck += 1
	if timer.iocheck >= timer.iointerval:
		timer.iocheck, outgoing, outnumber = 0, "", 0
		#Set tosend as list of strings: "50 40 normal", coord, time delay, type
		for i in tosend:
			outgoing += " " + str(i)
			outnumber += 3
		outgoing = str(outnumber) + outgoing
		print "Outgoing: ", outgoing
		if isHost:
			thisplayer.sendinfo(outgoing)
			recieved = thisplayer.myreceive()
		else:
			recieved = thisplayer.myreceive()
			thisplayer.sendinfo(outgoing)
		print recieved
		tosend, recieved = [], getwords(recieved, 2)
		
		#assuming recieved is list, not who won
		try:
			theinfo = getwords(recieved[1], 3*int(recieved[0]))
			rand = []
			for i in range(len(theinfo)):
				rand.append[theinfo[i]]
				if (i+1)%3 == 0:
					yetcreeps.append(yetCreep(rand))
					rand = []
		except IndexError:
			if recieved[0] == "0":
				print "Nothing happens"
			else:
				print recieved[0]
	
	for i in yetcreeps:
		if timer.iocheck >= i.time:
			
			yetcreeps.remove(i)
	
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			done = True 
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_down = True
				
		elif event.type == pygame.MOUSEBUTTONUP:
			mouse_down = False
	
	mouse_pos = pygame.mouse.get_pos()
	testCreep.update(mouse_pos)
	
	gScreen.fill(WHITE)
	
	gScreen.blit(testCreep.img, [testCreep.cord[0], testCreep.cord[1]])
	
	pygame.display.flip()
	clock.tick(60)