import pygame
from pygame.locals import*
import os


def getHighScores():
	with open ("scoreboard.txt","r") as scoreboard:
		scores = [s.split() for s in scoreboard.readlines()[1:11]]
		scores = [[int(s[0]),s[1]] for s in scores]

		return scores

def saveHighScores(scores):
	with open ("scoreboard.txt", "w") as scoreboard:
		scores.sort()
		scoreboard.write("High Scores\n")
		for score in reversed(scores):
			scoreboard.write(str(score[0]) + " " +score[1] + "\n")


def keyboard(screen, joysticks, joystick_control):
	screen.fill((0,0,0))
	keyboard = [['A','B','C','D','E','F','G'],
				['H','I','J','K','L','M','N'],
				['O','P','Q','R','S','T','U'],
				['V','W','X','Y','Z','-','+']]

	fuente = pygame.font.Font(None, 30)

	current = [0,0]
	string = ""

	timesincelastjoystickmovement = 11

	while True:
		screen.fill((0,0,0))
		for i in range(4):
			for j in range(7):
				if i == current[1] and j == current[0]:
					letter = fuente.render(keyboard[i][j], 1, (0,0,255))
					screen.blit(letter, (100 + 40*j, 300 + 40*i))
				else:
					letter = fuente.render(keyboard[i][j], 1, (255,255,255))
					screen.blit(letter, (100 + 40*j, 300 + 40*i))

		name = fuente.render(string, 1, (255,255,255))
		screen.blit(name, (100,150))

		if joystick_control:
			if timesincelastjoystickmovement < 11:
				timesincelastjoystickmovement += 1
			if pygame.joystick.Joystick(0).get_axis(1) < -0.4 and timesincelastjoystickmovement == 11:
				current[1] = (current[1] - 1)%4
				timesincelastjoystickmovement = 0
			if pygame.joystick.Joystick(0).get_axis(1) > 0.4 and timesincelastjoystickmovement == 11:
				current[1] = (current[1] + 1)%4
				timesincelastjoystickmovement = 0
			if pygame.joystick.Joystick(0).get_axis(0) < -0.4 and timesincelastjoystickmovement == 11:
				current[0] = (current[0] - 1)%7
				timesincelastjoystickmovement = 0
			if pygame.joystick.Joystick(0).get_axis(0) > 0.4 and timesincelastjoystickmovement == 11:
				current[0] = (current[0] + 1)%7
				timesincelastjoystickmovement = 0


		for evento in pygame.event.get():

			if evento.type == QUIT:
				pygame.quit()
				sys.exit()

			elif evento.type == JOYAXISMOTION:
				joystick_control = True

			elif evento.type == pygame.JOYBUTTONDOWN:
				if evento.button == 0:
					if keyboard[current[1]][current[0]] == '-':
						string = string[:-1]
					elif keyboard[current[1]][current[0]] == '+':
						return string
					else:
						string += keyboard[current[1]][current[0]]
				
			elif evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE:
					return "menu"

				elif evento.key == pygame.K_UP:
					current[1] = (current[1] - 1 ) % 4
				elif evento.key == pygame.K_DOWN:
					current[1] = (current[1] + 1 ) % 4
				elif evento.key == pygame.K_LEFT:
					current[0] = (current[0] - 1 ) % 7
				elif evento.key == pygame.K_RIGHT:
					current[0] = (current[0] + 1 ) % 7
				elif evento.key == 13:		#ENTER
					if keyboard[current[1]][current[0]] == '-':
						string = string[:-1]
					elif keyboard[current[1]][current[0]] == '+':
						return string
					else:
						string += keyboard[current[1]][current[0]]
		pygame.time.Clock().tick(60)
		pygame.display.update()

	return "LAWRENCE"

def scoreboards(screen, scores, joysticks, joystick_control):
	screen.fill((255,255,255))
	background = pygame.image.load(os.path.join("imagen","333.png"))
	screen.blit(background,(500,0))

	fuente3 = pygame.font.Font("fuente/nasalization2.ttf",30)

	fuente4 = pygame.font.Font("fuente/nasalization2.ttf",60)
	highscoresmessage = fuente4.render("High Scores", 1, ((0,0,0)))
	screen.blit(highscoresmessage, (90,70))

	scoreMessages = []
	for score, name in scores:
		message1 = fuente3.render(name, 1, (0,0,0))
		message2 = fuente3.render(str(score), 1, (0,0,0))
		length = len(str(score))
		scoreMessages.append([message1,message2,length])

	for i in range(10):
		screen.blit(scoreMessages[i][0], (100, 200 + 40*i))
		screen.blit(scoreMessages[i][1], (450 - 20*scoreMessages[i][2], 200 + 40*i))

	pygame.display.update()

	while True:
		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()

			elif evento.type == pygame.JOYBUTTONDOWN:
				if evento.button == 1:
					return "menu"

			elif evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					return "menu"




