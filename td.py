import random
import pygame
import pyganim
import time
import math
clock = pygame.time.Clock()

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
		self.spd = 2
		self.cord = [50,50]
		self.vel = [0,0]
		self.img = img
		
		
		
	def update(self):
		self.cord[0] += self.vel[0] * self.spd
		self.cord[1] += self.vel[1] * self.spd
		
	def sendOver():
		
		
		
		
		
		
		
		
testCreep = CreepFrd("")
testCreep.vel = convertVel(45)

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
	
		
		
		
		
		
		
while not done:
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			done = True 
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_down = True
				
		elif event.type == pygame.MOUSEBUTTONUP:
			mouse_down = False
		
	mouse_pos = pygame.mouse.get_pos()
	testCreep.update()
	gScreen.fill(WHITE)
	pygame.draw.rect(gScreen, RED, [testCreep.cord[0], testCreep.cord[1], 25,25])
	
		
		
		
		
		
	pygame.display.flip()


	clock.tick(60)