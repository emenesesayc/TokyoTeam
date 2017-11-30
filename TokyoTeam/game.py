import pygame
from pygame.locals import*
import random

def restart(screen, joysticks, joystick_control, score):
	fuente1 = pygame.font.Font(None, 80)
	fuente2 = pygame.font.Font(None, 30)

	finalscoremessage = "score: " + str(int(score))
	finalscore = fuente1.render(finalscoremessage,1,(255,255,255))
	screen.blit(finalscore, (280,250))

	restarButton = "<< Press <r> to restart >>" if not joystick_control else "<<Press -> to restart>>"
	restartmessage = fuente2.render(restarButton,1,(255,255,255))
	screen.blit(restartmessage, (250,320))

	pygame.display.update()

	while True:
		for evento in pygame.event.get():
				

			if evento.type == pygame.JOYBUTTONDOWN:
				if evento.button == 7:
					return "Arcade"

				elif evento.button == 1:
					return "menu"


			elif evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE:
					return "menu"


				elif evento.key == pygame.K_r:
					return "Arcade"

def pause(screen):
	fuente = pygame.font.Font(None, 80)
	pausemessage = fuente.render("PAUSE" ,1,(255,255,255))
	screen.blit(pausemessage, (280,250))

	pygame.display.update()

	pause = True
	while pause:
		for evento in pygame.event.get():

			if evento.type == JOYBUTTONDOWN:
				if evento.button == 7:
					pause = False

			elif evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE:
					pause = False
				elif evento.key == pygame.K_p:
					pause = False

def joystickControls(joysticks, player):
	if pygame.joystick.Joystick(0).get_axis(0) < -0.4 and player["x"] > 0:
		#left
		velocidadx = -5
	elif pygame.joystick.Joystick(0).get_axis(0) > 0.4 and player["x"] < 1334:
		#right
		velocidadx = +5
	else:
		velocidadx = 0
	boost = 2 if pygame.joystick.Joystick(0).get_button(0) else 0
	return velocidadx, boost

def keyboardControls(player):
	if pygame.key.get_pressed()[K_RIGHT] and player["x"] < 1334:
		velocidadx = +5
	elif pygame.key.get_pressed()[K_LEFT] and player["x"] > 0:
		velocidadx = -5
	else:
		velocidadx = 0
	boost = 2 if pygame.key.get_pressed()[K_SPACE] else 0
	return velocidadx, boost

def createEnemigo():
	# agregar sprites
	x = random.randrange(1350)
	y = random.randint(-768,-10)
	a = random.randint(-5,5)
	if a == -5:
		velx = -4
	elif a == 5:
		velx = 4
	else:
		velx = 0
	rect = pygame.Rect(x,y,20,20)
	return {"x": x, "y": y, "velx": velx, "rect": rect}

def enemigo(screen, score, player, enemigos, asteroid):
	lose = False
	velocidadEnemigo0 = 6 + int(score/20)
	if len(enemigos) < 40:
		enemigos.append(createEnemigo())
	for i in range(len(enemigos)):
		for j in range(len(enemigos)):
			if enemigos[i]["rect"].colliderect(enemigos[j]["rect"]) and i!=j:
				if enemigos[i]["x"] < enemigos[j]["x"]:
					enemigos[i]["velx"] = -4
					enemigos[j]["velx"] = 4
				else:
					enemigos[i]["velx"] = 4
					enemigos[j]["velx"] = -4

		if enemigos[i]["x"] < 0 or enemigos[i]["x"] > 1346:
			enemigos[i]["velx"] = -enemigos[i]["velx"]

		enemigos[i]["y"] += velocidadEnemigo0
		enemigos[i]["x"] += enemigos[i]["velx"]
		enemigos[i]["rect"] = pygame.Rect(enemigos[i]["x"], enemigos[i]["y"], 20, 20)
		screen.blit(asteroid, (enemigos[i]["x"], enemigos[i]["y"]))
		if enemigos[i]["y"] > 768:
			enemigos[i] = createEnemigo()

		if player["rect"].colliderect(enemigos[i]["rect"]):
			enemigos[i]["image"] = pygame.image.load("imagen/asteroid.png")
			player_mask = pygame.mask.from_surface(player["image"])
			asteroid_mask = pygame.mask.from_surface(enemigos[i]["image"])

			player_rect = player["image"].get_rect()
			asteroid_rect = enemigos[i]["image"].get_rect()

			offset_x = player_rect.x - asteroid_rect.x
			offset_y = player_rect.y - asteroid_rect.y

			#if pygame.sprite.collide_mask(player["image"], enemigos[i]["image"]):
			if player_mask.overlap(player_mask, (offset_x, offset_y)):
				lose = True

	return lose

def arcade(screen, joysticks, joystick_control):
	score = 0
	fuente3 = pygame.font.Font("fuente/nasalization2.ttf", 30)

	asteroid = pygame.image.load("imagen/asteroid.png")

	#player
	image_forward = pygame.image.load("imagen/lawrence_ship.png")
	image_left = pygame.image.load("imagen/lawrence_ship_left.png")
	image_right = pygame.image.load("imagen/lawrence_ship_right.png")
	player = {"x": 700, "velocidad": 0, "boost": 0}
	player["rect"] = pygame.Rect(player["x"], 680, 34, 47)
	player["image"] = image_forward
	# y = 680

	enemigos = []

	clock = pygame.time.Clock()

	while True:
		
		screen.fill((0,0,0))

		scoreprint = fuente3.render(str(int(score)),1,(255,255,255))
		screen.blit(scoreprint,(10,10))

		player["velocidad"], player["boost"] = joystickControls(joysticks, player) if joystick_control else keyboardControls(player)

		player["x"] += player["velocidad"] * player["boost"] if player["boost"] else player["velocidad"]
		player["rect"] = pygame.Rect(player["x"], 680, 34, 47)


		if player["velocidad"] < 0:
			player["image"] = image_left
		elif player["velocidad"] == 0:
			player["image"] = image_forward
		else:
			player["image"] = image_right
		screen.blit(player["image"], (player["x"],680))

		if enemigo(screen, score, player, enemigos, asteroid):
			return int(score)

		for evento in pygame.event.get():


			if evento.type == JOYAXISMOTION:
				joystick_control = True
			elif evento.type == JOYBUTTONDOWN:
				if evento.button == 7:
					pause(screen)

			elif evento.type == pygame.KEYDOWN:
				joystick_control = False
				if evento.key == pygame.K_ESCAPE:
					pause(screen)

				elif evento.key == pygame.K_p:
					pause(screen)



		score += 1/60

		clock.tick(60)
		pygame.display.update()


