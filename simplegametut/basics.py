#Import pygame module 
import pygame

#Import random for random numbers 
import random 

#Impport pygame.locals for easier access to key coordinates 
from pygame.locals import (
	RLEACCEL,
	K_w, 
	K_s, 
	K_a, 
	K_d, 
	K_ESCAPE, 
	KEYDOWN, 
	QUIT, 
)

#Initializes the game 
pygame.init()

#Define constants for the screen width and height 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



#Define a Player object by extending pygame.sprite.Sprite
#The surface is drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.imageload = pygame.image.load("player.png").convert()
		self.imagescale = pygame.transform.scale(self.imageload, (50, 50))
		self.surf = pygame.transform.rotate(self.imagescale, 270)
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect()

	def update(self, pressed_key):
		if pressed_key[K_w]:
			self.rect.move_ip(0, -5)
		if pressed_key[K_s]:
			self.rect.move_ip(0, 5)
		if pressed_key[K_a]:
			self.rect.move_ip(-5, 0)
		if pressed_key[K_d]:
			self.rect.move_ip(5, 0)


		#Keep player on the screen 
		if self.rect.left <0:
			self.rect.left = 0 
		if self.rect.right >SCREEN_WIDTH:
			self.rect.right = SCREEN_WIDTH
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT

#Define the enemy object by entending pygame.sprite.Sprite
#The surface you draw on the screen is now an attribute of enemy 
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.imageload = pygame.image.load('spr_missile.png').convert()
		self.surf = pygame.transform.rotate(self.imageload, 180)
		self.surf.set_colorkey((255,255,255),RLEACCEL)

		#Starting position is randomly generates, as is the speed 
		self.rect = self.surf.get_rect(
			center=(
				random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH +100),
				random.randint(0,SCREEN_HEIGHT),
				)
		)
		self.speed = random.randint(5, 20)

	#Move the sprite based on speed 
	# Remove the spite when it passes the left edge of the screen 
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right <0:
			self.kill()

#Define the cloud object by extending pygame.sprite.Sprite
# Us an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
	def __init__(self):
		super(Cloud, self).__init__()
		self.surf = pygame.image.load('Cloud_0.png').convert()
		self.surf.set_colorkey((0,0,0), RLEACCEL)
		#The starting position is randomly generated
		self.rect = self.surf.get_rect(
			center=(
				random.randint(SCREEN_WIDTH +20, SCREEN_WIDTH +100), 
				random.randint(0, SCREEN_HEIGHT),
				)
			)

		#Move the cloud based on a constant speed
		#Remove the cloud when it passes the left edge of the screen 
	def update(self):
		self.rect.move_ip(-5, 0)
		if self.rect.right <0:
			self.kill()

#Create the screen object 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Create a custom event for adding a new enemy 
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

#Create custom events for adding a new enemy and a cloud
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

#Instantiate player.
player = Player()

#Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates 
# - all_sprites is used for rendering 
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Variable to keep the main loop running 
running = True 

#Setup the clock for a decent framerate
clock = pygame.time.Clock()

#Main loop 
while running:
	#Look for every event in the queue
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False


		elif event.type == QUIT:
			running = False


		#Add a new enemy 
		elif event.type == ADDENEMY:
			#Create the new enemy and add it to sprite groups 
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)

		# Add new cloud
		elif event.type == ADDCLOUD:
			#Create the new cloud and add it to sprite groups 
			new_cloud = Cloud()
			clouds.add(new_cloud)
			all_sprites.add(new_cloud)



	#Get the set of keys pressed and check for user input 
	pressed_key = pygame.key.get_pressed()

	#Update the player sprit ebased on user keypresses 
	player.update(pressed_key)

	#Update enemy position and clouds
	enemies.update()
	clouds.update()

	#Fill the screen with blue
	screen.fill((135, 206, 250))

	#Draw all sprites
	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)

	#Check if any enemies have collided with the player
	if pygame.sprite.spritecollideany(player, enemies):
		#if so then remove the player and stop the loop
		player.kill()
		running = False

	#Draw the player on screen 
	screen.blit(player.surf, player.rect)

	#Update the display
	pygame.display.flip()

	#Ensure program maintains a rate of 30 frames per second
	clock.tick(30)


