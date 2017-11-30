import pygame
from pygame.locals import*
import os
import sys

def intro(screen):
	pygame.mixer.music.load("sonido/menu-theme.wav")
	pygame.mixer.music.play()

	fuente2 = pygame.font.Font("fuente/Foreplayer.otf", 90)
	presents = fuente2.render("presents", 1, (255,255,255))

	time = 0
	while time < 180:
		if time < 120:
			#TokyoTeam logo
			pass
		else:
			screen.fill((0,0,0))
			screen.blit(presents,(450,374))
		time +=1
		pygame.time.Clock().tick(60)
		pygame.display.update()



def menu(screen, joysticks, joystick_control):

	background = pygame.image.load(os.path.join("imagen","333.png"))

	fuente3 = pygame.font.Font("fuente/nasalization2.ttf",40)
	opciones = ["Arcade","Campaign","High Scores","Help","Exit"]
	mensajes = []
	for i in opciones:
		mensaje = fuente3.render(i,1,(0,0,0))
		mensajes.append(mensaje)

	current_option = 0
	x = 100

	timesincelastjoystickmovement = 11

	while True:
		screen.fill((255,255,255))
		screen.blit(background,(500,0))

		for i in range(5):
			screen.blit(mensajes[i], (180,430 + 50*i))

		y = 442 + 50*current_option
		flecha = [(x,y),(x+50,y+25),(x,y+50)]
		pygame.draw.polygon(screen, (0,0,0), flecha)

		if timesincelastjoystickmovement < 11:
			timesincelastjoystickmovement += 1
		if joystick_control:
			if pygame.joystick.Joystick(0).get_axis(1) < -0.4 and timesincelastjoystickmovement == 11:
				current_option = (current_option - 1)%5
				timesincelastjoystickmovement = 0
			if pygame.joystick.Joystick(0).get_axis(1) > 0.4 and timesincelastjoystickmovement == 11:
				current_option = (current_option + 1)%5
				timesincelastjoystickmovement = 0

		for evento in pygame.event.get():

			if evento.type == JOYAXISMOTION:
				joystick_control = True

			elif evento.type == pygame.JOYBUTTONDOWN:
				if evento.button == 0:
					return opciones[current_option]

			elif evento.type == pygame.KEYDOWN:
				joystick_control = False
				if evento.key == pygame.K_ESCAPE:
					return "Exit"
				elif evento.key == pygame.K_DOWN:
					current_option = (current_option + 1)%5
				elif evento.key == pygame.K_UP:
					current_option = (current_option - 1)%5
				elif evento.key == 13:
					return opciones[current_option]

		pygame.time.Clock().tick(60)
		pygame.display.update()