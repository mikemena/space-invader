import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# spaceship variables
spaceship_img = pygame.image.load("images/spaceship.png")
spaceship_x = 608
spaceship_y = 650
spaceship_x_change = 0

# green monster variables
green_monster_img = pygame.image.load("images/green_monster.png")
green_monster_x = random.randint(0, 608)
green_monster_y = random.randint(0, 10)
green_monster_x_change = 2.0
green_monster_y_change = 10


# spaceship function
def spaceship(x, y):
    screen.blit(spaceship_img, (x, y))


# green monster function
def green_monster(x, y):
    screen.blit(green_monster_img, (x, y))


# setup title and icon
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")
background = pygame.image.load("images/Background.jpg")

# main game loop
while running:
    # background image
    # screen.blit(background, (0, 0))
    screen.fill((72, 60, 148))
    # spaceship_x += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # handle press arrow key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_x_change = -2.0
            if event.key == pygame.K_RIGHT:
                spaceship_x_change = 2.0
        # handle key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_x_change = 0

    # handle spaceship movement
    spaceship_x += spaceship_x_change

    # keep the spaceship in the screen
    if spaceship_x <= 5:
        spaceship_x = 5
    elif spaceship_x >= 1210:
        spaceship_x = 1210

    # handle green monster movement
    green_monster_x += green_monster_x_change

    # keep the green monster in the screen
    if green_monster_x <= 5:
        green_monster_x_change = 2.0
        green_monster_y += green_monster_y_change
    elif green_monster_x >= 1210:
        green_monster_x_change = -2.0
        green_monster_y += green_monster_y_change

    spaceship(spaceship_x, spaceship_y)
    green_monster(green_monster_x, green_monster_y)
    # update screen
    pygame.display.update()
