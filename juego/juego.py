#coding: utf-8

import pygame
import time
import random

pygame.init()

width = 800
height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
yellow = (255,255,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
car_width = 76 
car_height = 169

gameDisplay = pygame.display.set_mode ((width,height))
pygame.display.set_caption ("JUEGO")
pygame_events = pygame.event.get()

clock = pygame.time.Clock()
car = pygame.image.load("rojo.png")
road = pygame.image.load("road.png")
obstacle = pygame.image.load("azul.png")
introImg = pygame.image.load("fondo.png")
pause = False

def object_dodged(count):
	font = pygame.font.SysFont(None,35)
	text = font.render("Puntuacion: "+str(count),True,black)
	gameDisplay.blit(text,(0,0))

def object(objectx,objecty):
	gameDisplay.blit(obstacle,(objectx, objecty))
	
def car(x,y):	
	gameDisplay.blit(coche,(x,y))

def text_over(text,font):	
	textSurface = font.render(text,True,bright_red)
	return textSurface, textSurface.get_rect()
	
def text_intro(text,font):	
	textSurface = font.render(text,True,black)
	return textSurface, textSurface.get_rect()

def crash():	
	largeText = pygame.font.Font("freesansbold.ttf",90)
	TextSurf, TextRect = text_over("Game Over",largeText)	
	TextRect.center = ((width/2),(height/2))
	gameDisplay.blit(introImg,(0,0))
	gameDisplay.blit(TextSurf,TextRect)	
		
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		button("Volver",150,450,100,50,green,bright_green,game_loop)
		button("Salir",550,450,100,50,red,bright_red,quitgame)
		pygame.display.update()
		clock.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()	
		
	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			action()
	else: 
		pygame.draw.rect(gameDisplay,ic,(x,y,w,h))	
			
	smallText = pygame.font.Font("freesansbold.ttf",20)
	textSurf, textRect = text_intro(msg,smallText)
	textRect.center = ((x+(w/2)),(y+(h/2)))
	gameDisplay.blit(textSurf, textRect)

def quitgame():
	pygame.quit()
	quit()
	
def unpause():
	global pause
	pause = False

def paused():
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(white)
		largeText = pygame.font.Font("freesansbold.ttf",90)
		TextSurf, TextRect = text_intro("Pausa",largeText)
		TextRect.center = ((width/2),(height/2))
		gameDisplay.blit(TextSurf,TextRect)		
		button("Continuar",150,450,100,50,green,bright_green,unpause)
		button("Salir",550,450,100,50,red,bright_red,quitgame)
		pygame.display.update()
		clock.tick(15)
		
def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.blit(introImg,(0,0))
		largeText = pygame.font.Font("freesansbold.ttf",90)
		TextSurf, TextRect = text_over("Juego",largeText)
		TextRect.center = ((width/2),(height/2))
		gameDisplay.blit(TextSurf,TextRect)		
		button("Empezar",150,450,100,50,green,bright_green,game_loop)
		button("Salir",550,450,100,50,red,bright_red,quitgame)
		pygame.display.update()
		clock.tick(15)
	
def game_loop():
	global pause
	x = (width * 0.44)
	y = (height * 0.65)
	x_change = 0
	object_startx = random.randrange(0,width)
	object_starty = -600
	object_speed = 5
	object_width = 75
	object_height = 168
	dodged = 0
	left = False
	right = False
	gameExit = False
	
	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					left = True
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					right = True
				elif event.key == pygame.K_p:
					pause = True
					paused()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					left = False
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					right = False
				if event.key == pygame.K_p:
					pause = True
					paused()
		
		if left and right:
			x_change *= 1
		elif left:
			x_change = -5
		elif right:
			x_change= 5
		else:
			x_change = 0
					
		x += x_change			
		gameDisplay.blit(road,(0,0))	
		
		object(object_startx,object_starty)
		object_starty += object_speed
		car(x,y)
		object_dodged(dodged)
		
		if x > width - car_width or x < 0:
			crash()
		
		if object_starty > height:
			object_starty = 0 - object_height
			object_startx = random.randrange(0,width)
			dodged += 1
			if dodged % 2 == 0:
				object_speed += 1				
		
		if x in range(object_startx - car_width, object_startx + object_width):
			if y in range(object_starty - car_height, object_starty + object_height):
				crash()	
				
		pygame.display.update()
		clock.tick(60)
	
game_intro()
game_loop()
pygame.quit()
quit()
