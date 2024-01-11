import pygame
import random
import math

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

# missle variables
missle_img = pygame.image.load("images/missile.png")
missle_x = 0
missle_y = 650
missle_x_change = 0
missle_y_change = 2.5
visible_missle = False


# score
score = 0

# green monster variables
green_monster_img = pygame.image.load("images/green_monster.png")
green_monster_x = random.randint(0, 608)
green_monster_y = random.randint(0, 10)
green_monster_x_change = 0.8
green_monster_y_change = 10


# spaceship function
def spaceship(x, y):
    screen.blit(spaceship_img, (x, y))


# green monster function
def green_monster(x, y):
    screen.blit(green_monster_img, (x, y))


# shoot missle function
def shoot_missle(x, y):
    global visible_missle
    visible_missle = True
    screen.blit(missle_img, (x + 1, y + 10))


# detect collision
def target_hit(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distance < 27:
        return True
    else:
        return False


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
        # handle press key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_x_change = -1.2
            if event.key == pygame.K_RIGHT:
                spaceship_x_change = 1.2
            if event.key == pygame.K_SPACE:
                if not visible_missle:
                    missle_x = spaceship_x
                    shoot_missle(missle_x, missle_y)
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
        green_monster_x_change = 0.5
        green_monster_y += green_monster_y_change
    elif green_monster_x >= 1210:
        green_monster_x_change = -0.5
        green_monster_y += green_monster_y_change

    # missle movement
    if missle_y <= -25:
        missle_y = 600
        visible_missle = False
    if visible_missle:
        shoot_missle(missle_x, missle_y)
        missle_y -= missle_y_change

    # collision
    collision = target_hit(green_monster_x, green_monster_y, missle_x, missle_y)
    # explosion
    explosion_img = pygame.image.load("images/explosion.png")
    if collision:
        screen.blit(explosion_img, (green_monster_x, green_monster_y))
        # Update the display to show the explosion
        pygame.display.update()
        # Delay for half a second to show the explosion
        pygame.time.delay(800)
        # Reset the missile
        missle_y = 600
        visible_missle = False
        # Increase the score
        score += 1
        print(score)
        green_monster_x = random.randint(0, 608)
        green_monster_y = random.randint(0, 10)

    # explode

    spaceship(spaceship_x, spaceship_y)
    green_monster(green_monster_x, green_monster_y)
    # update screen
    pygame.display.update()
