import pygame
from pygame.locals import*
import random

from scoreboards import *
from menu import *
from game import *

pygame.init()
pygame.mouse.set_visible(False)


def main():
	class Error(Exception):
		pass
	class NotFound(Error):
		pass

	scene = "menu"
	scores = getHighScores()

	joysticks = []
	for i in range(pygame.joystick.get_count()):
		joysticks.append(pygame.joystick.Joystick(i))
		joysticks[-1].init()
	joystick_control = False

	#screen = pygame.display.set_mode((1300,700))
	resolution = pygame.display.Info()
	screen = pygame.display.set_mode((resolution.current_w, resolution.current_h), pygame.FULLSCREEN)


	#intro(screen)


	
	while scene != "Exit" :

		try:		
			if scene == "Exit":
				pass
			elif scene == "menu":
				scene = menu(screen, joysticks, joystick_control)
			elif scene == "High Scores":
				scene = scoreboards(screen, scores, joysticks, joystick_control)
			elif scene == "Arcade":
				score = arcade(screen, joysticks, joystick_control)
				if score > scores[-1][0]:
					name = keyboard(screen, joysticks, joystick_control)
					scores[-1] = [score, name]
					scores.sort(reverse=True)
					screen.fill((0,0,0))
				scene = restart(screen, joysticks, joystick_control, score)
			else:
				raise NotFound
		except NotFound:
			scene = Error404(screen, joysticks)
		
		
			
	saveHighScores(scores)
	pygame.display.quit()

def Error404(screen, joysticks):
	screen.fill((255,255,255))
	fuente5 = pygame.font.Font(None, 80)
	msg = fuente5.render("Error 404", 1, (0,0,0))
	screen.blit(msg, (300,300))


	pygame.display.update()

	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.JOYBUTTONDOWN:
				return "menu"
			elif evento.type == pygame.JOYAXISMOTION:
				return "menu"
			elif evento.type == pygame.KEYDOWN:
				return "menu"



main()

