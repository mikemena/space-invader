import pygame
import random
import math
from pygame import mixer

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1616, 799))
clock = pygame.time.Clock()
running = True

# handle music
mixer.music.load("sounds/background.mp3")
mixer.music.set_volume(0.7)
mixer.music.play(-1)

# spaceship variables
spaceship_img = pygame.image.load("images/spaceship.png")
spaceship_width = spaceship_img.get_width()
# start the spaceship in the middle of the screen (screen is 1616 horizontal)
spaceship_x = 808
# start the spaceship at the bottom of the screen (screen is 799 height)
spaceship_y = 750
spaceship_x_change = 0

# missle variables
missle_img = pygame.image.load("images/missile.png")
missle_width = missle_img.get_width()
missle_x = 0
missle_y = 750
missle_x_change = 0
missle_y_change = 2.5
visible_missle = False

# explosion image
explosion_img = pygame.image.load("images/explode.png")

# score
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# monster images
monster_images = [
    pygame.image.load("images/green_monster.png"),
    pygame.image.load("images/red_monster.png"),
    pygame.image.load("images/blue_monster.png"),
    pygame.image.load("images/orange_monster.png"),
]
monster_img = []
monster_x = []
monster_y = []
monster_x_change = []
monster_y_change = []
monster_count = 5


for e in range(monster_count):
    img = random.choice(monster_images)
    monster_img.append(img)
    monster_x.append(random.randint(0, 608))
    monster_y.append(random.randint(0, 10))
    monster_x_change.append(0.8)
    # shift monster down when they reach the right side of the screen
    monster_y_change.append(100)


# show score function
def show_score(x, y):
    text = score_font.render(f"Score: {score}", True, (245, 132, 66))
    screen.blit(text, (x, y))


# spaceship function
def spaceship(x, y):
    screen.blit(spaceship_img, (x, y))


# green monster function
def green_monster(x, y, monstro):
    screen.blit(monster_img[monstro], (x, y))


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

# end game message
end_font = pygame.font.Font("freesansbold.ttf", 40)


def final_text():
    game_over = end_font.render("GAME OVER", True, (245, 132, 66))
    screen.blit(game_over, (800, 400))


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
                missle_sound = mixer.Sound("sounds/shot.mp3")
                missle_sound.set_volume(0.3)
                missle_sound.play()
                if not visible_missle:
                    missle_x = spaceship_x + (spaceship_width - missle_width) / 2
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
    elif spaceship_x >= 1580:
        spaceship_x = 1580

    # handle monster movement
    for monst in range(monster_count):
        # end game
        # show game over when the monster hits the rocket @ 700
        if monster_y[monst] > 750:
            for k in range(monster_count):
                monster_y[k] = 1000
            final_text()
            break
        monster_x[monst] += monster_x_change[monst]

        # keep the green monster in the screen
        if monster_x[monst] <= 5:
            monster_x_change[monst] = 0.5
            monster_y[monst] += monster_y_change[monst]
        elif monster_x[monst] >= 1590:  # monster moves to the right of screen
            monster_x_change[monst] = -0.5
            monster_y[monst] += monster_y_change[monst]
        # collision
        collision = target_hit(monster_x[monst], monster_y[monst], missle_x, missle_y)
        # explosion
        if collision:
            collision_sound = mixer.Sound("sounds/explosion.mp3")
            collision_sound.set_volume(0.3)
            collision_sound.play()
            screen.blit(explosion_img, (monster_x[monst], monster_y[monst]))
            # Update the display to show the explosion
            pygame.display.update()
            # Delay for half a second to show the explosion
            pygame.time.delay(800)
            # Reset the missile
            missle_y = 700
            visible_missle = False
            # Increase the score
            score += 1

            monster_x[monst] = random.randint(0, 608)
            monster_y[monst] = random.randint(0, 10)

        green_monster(monster_x[monst], monster_y[monst], monst)

    # missle movement
    if missle_y <= -80:
        missle_y = 700
        visible_missle = False
    if visible_missle:
        shoot_missle(missle_x, missle_y)
        missle_y -= missle_y_change

    # explode

    spaceship(spaceship_x, spaceship_y)

    # show score
    show_score(text_x, text_y)
    # update screen
    pygame.display.update()
