import pygame
import random
import math
from pygame import mixer

# initializing pygame module
pygame.init()

# creating game screen
screen = pygame.display.set_mode((800, 600))

# changing screen title and fav icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# adding background music
mixer.music.load("cartoon-birds-2_daniel-simion.wav")
mixer.music.play(-1)

# adding sound on bullet fire
bullet_sound = mixer.Sound("gun-gunshot-01.wav")

# creating player
player = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# creating enemy
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemy.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(30, 120))
    enemyX_change.append(0.7)
    enemyY_change.append(40)


# creating bullet
bullet = pygame.image.load("bullet.png")
bulletX = 480
bulletY = 370
bulletX_change = 0
bulletY_change = -2
bullet_state = "ready"

# creating score and bullet used
score = 0
bullet_used = 0
score_font = pygame.font.Font("freesansbold.ttf", 28)
def show_score():
    value = score_font.render("Score : "+str(score), True, (237, 26, 146))
    screen.blit(value, (10, 10))
    bullet_value = score_font.render("Bullets Used :" + str(bullet_used), True, (237, 26, 146))
    screen.blit(bullet_value, (10, 40))

# code for game over conditions and its display
over_font = pygame.font.Font("freesansbold.ttf", 48)
check_for_game_over = False

def game_over():
    global check_for_game_over
    check_for_game_over = True
    screen.blit(over_font.render("GAME OVER", True, (237, 26, 146)), (200, 250))
    screen.blit(score_font.render("Press ENTER to play again", True, (237, 26, 146)), (200, 320))



# creating the background image
background = pygame.image.load("project_background.jpg")

def show_player(x,y):
    screen.blit(player, (x, y))

def show_enemy(i, x, y):
    screen.blit(enemy[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x+16, y+10))

def is_collision(ex, ey, bx, by):
    collide = math.sqrt(math.pow(ex-bx, 2)+math.pow(ey-by, 2))
    if collide < 27:
        return True
    else:
        return False


running = True

# Game loop

while running:

    # filling a color on game screen
    screen.fill((22, 84, 89))
    screen.blit(background, (0, 0))

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            elif event.key == pygame.K_RIGHT:
                playerX_change = 1
            elif event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bullet_used += 1
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound.play()
            elif event.key == pygame.K_SPACE:
                if check_for_game_over == True:
                    score = 0
                    bullet_used = 0
                    check_for_game_over = False
                    for i in range(no_of_enemies):
                        enemyX[i] = random.randint(0, 736)
                        enemyY[i] = random.randint(30, 120)





        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0


    # showing enemies
    for i in range(no_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]
        if enemyY[i] >= 480:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(30, 120)
            score += 10
            bullet_state = "ready"
            bulletY = 480
        else:
            show_enemy(i, enemyX[i], enemyY[i])




    # showing player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    show_player(playerX, playerY)

    if bullet_state == "fire":
        bulletY += bulletY_change
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = 480
        else:
            fire_bullet(bulletX, bulletY)

    show_score()

    # updating the game screen
    pygame.display.update()



