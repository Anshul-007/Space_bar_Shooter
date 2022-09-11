import math
import pygame
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('space.png')
pygame.display.set_caption("Space Fighters")
# background music
mixer.music.load('audio.mp3')
mixer.music.play(-1)

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('plyr.png')
playerX = 350
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemy = 6
for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load('stone64.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(20)

# bullet
# ready = invisible bullet
# fire bullet is fired and visible
bulletImg = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# score
score = 0
font = pygame.font.Font('Comfortaa-Bold.ttf', 32)


# Game over
over_font = pygame.font.Font('Comfortaa-Bold.ttf', 64)
text_X = 10
text_Y = 10


# line font
line_font = pygame.font.Font('Comfortaa-Bold.ttf', 32)


def show_score(x, y):
    score_v = font.render("Score: " + str(score), True, (4, 25, 75))
    screen.blit(score_v, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER ", True, (4, 25, 75))
    screen.blit(over_text, (200, 250))
    

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, p):
    screen.blit(enemyImg[p], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollliding(enemX, enemY, bulleX, bulleY):
    distance = math.sqrt(math.pow((enemX - bulleX), 2) + math.pow((enemY - bulleY), 2))
    if distance < 35:
        return True
    else:
        return False


# game running loop
run = True
while run:
    # RGB colors
    screen.fill((135, 42, 85))
    screen.blit(background, (0, 9))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6

            if event.key == pygame.K_DOWN:
                playerY_change = 0.6

            if event.key == pygame.K_UP:
                playerY_change = -0.6

            if event.key == pygame.K_SPACE:

                # only fire when bullet is not on screen
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('bullet.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == \
                    pygame.K_DOWN or event.key == pygame.K_UP:
                playerX_change = 0
                playerY_change = 0

    # player cannot exceed the boundary
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= -21:
        playerX = -21
    elif playerX >= 692:
        playerX = 692
    if playerY >= 480:
        playerY = 480
    elif playerY <= 260:
        playerY = 260

    # enemy movement
    for i in range(no_of_enemy):
        # game over
        if enemyY[i] > 200:
            for j in range(no_of_enemy):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -5:
            enemyX_change[i] = 0.6
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 750:
            enemyX_change[i] = -0.6

        # collision
        collision = isCollliding(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            impact_sound = mixer.Sound('explosion.mp3')
            impact_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 10
            # print(score)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    line_v = font.render("--------------------------------------------------------------", True, (4, 25, 75))
    screen.blit(line_v, (0, 240))
    player(playerX, playerY)
    show_score(text_X, text_Y)
    pygame.display.update()
