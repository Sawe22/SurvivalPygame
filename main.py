import math
import random
import pygame
from pygame import mixer


"""In this code I added a:
-Clock
-Death Border
-Modified All assets
-Change in the death zone
-bullet velocity + Hitbox, key input ("LSHIFT" to shoot, "a" to move left, "d" to go right), Enemy amount + Hitbox, Bullet start position, Enemy Movement speed (delta x and y)
-Scale added to all images, rather than using a premade size

"""


pygame.init() #Starts up the pygame engine

screen = pygame.display.set_mode((800, 900)) #Makes the screen

background = pygame.image.load('BetterBackground.jpeg') #Makes the bacground a jpeg i found from the internet

mixer.music.load("MarioMusic.flac") #loads mario music
mixer.music.play(-1) #plays the music in a LOOP, as seen by the -1

pygame.display.set_caption("Minecraft Attack") #Makes the caption
icon = pygame.image.load('hard-hat.png') #Imports a hat image I yoinked from the internet
pygame.display.set_icon(icon) #This makes the game icon the hat image


character = pygame.image.load('hands-up-2.png')
handX = 370
handY = 600
handX_delta = 0 #I just used delta unstead of change to sound cool. This is the change in the x position of the hand
crystalImg = [] #Many lists which contain info about the crystals, such as thier x and y positions, and the change in those positions
crystalX = []
crystalY = []
crystalX_delta = []
crystalY_delta = []
ENEMY_AMOUNT = 5 #Self explanatory, amount of enemies on screen





def rotate_image(character):
    character = pygame.transform.rotate.rotozoom(crystal, 20, 1)
    return character

for i in range(ENEMY_AMOUNT): #Goes though the amount of enemies (5) and atributes to each one an x and y position, putting those values into the lists which contain those data points
    crystal = pygame.image.load('crystal.webp')
    crystal = pygame.transform.scale(crystal, (50, 50)) #Here is an addition which scales images, used elsewhere also
    crystalImg.append(crystal) #Adds crystal to the list
    crystalX.append(random.randint(0, 720)) #Givrs teh crystal a random x position
    crystalY.append(random.randint(50, 100)) #Gives crystal a random y postion
    crystalX_delta.append(10) #The change in x potiion of the crystal
    crystalY_delta.append(20) #The change in y position of the crystal 

projectileImg = pygame.image.load('projectile.png')
projectileImg = pygame.transform.scale(projectileImg, (20, 20)) #Scales the projectile down

projectileX = 0 #The inital x posiotn of the projectile
projectileY = 700 #Y piosiiuon of bullet it starts at idly
projectileX_delta = 0 #Indicated how the x position of the bullet doesn't change
projectileY_delta = 20 #The bullet change in y position or "velocity"
projectile_state = "prepped" #The vixeo creats bullets in two stateas, one which has it prepared, whre its y position doesnt change until the user shoots it



current_points = 0 #The current points to be displayed pn the screen
font = pygame.font.Font('freesansbold.ttf', 32) #This font seems to work so i kept it here.

BORDER = pygame.Rect(0, 340, 800, 10)  #This clarifies the death sone of a player


wordsX = 10  #The x and y posituoins of the wrods
wordsY = 10

finished_font = pygame.font.Font('freesansbold.ttf', 64) #A font to be usead later on in the code


def show_score(x, y):
    score = font.render("Score : " + str(current_points), True, (255, 255, 255)) #Shows the score in a strong, while true (Always) in white
    screen.blit(score, (x, y))


def game_finished_words():
    finished_words = finished_font.render("You Died lol", True, (255, 255, 255))#Shows the score in a strong, while true (Always) in white
    screen.blit(finished_words, (200, 250))

def hand(x, y):
    screen.blit(character, (x, y))

def crystal(x, y, i):
    screen.blit(crystalImg[i], (x, y))

def shoot_projectile(x, y):
    global projectile_state
    projectile_state = "shoot" #In this state the bullet will have a change in positions
    screen.blit(projectileImg, (x+38, y+80)) #Starting positions of bullets

def isCollision(crystalX, crystalY, projectileX, projectileY):
    distance = math.sqrt(math.pow(crystalX - projectileX, 2) + (math.pow(crystalY - projectileY, 2))) #Math used in video, something to do with pytagroeon theorum
    if distance < 30:
        return True
    else:
        return False


Clock = pygame.time.Clock() #Added a clock to it since otherwise my laptop couldn't handle all the fps

playing = True #The video usese this method to start or end the game, by checking if a variable boolean is stll equal to true
while playing:
    Clock.tick(60)
    screen.fill((0, 0, 0)) #Fills screen iwth black FIRST, to ensure it is always in the bottn
    screen.blit(background, (0, 0)) #The backgorund is put at the top left of the screen, i didn't bother scaling it cause there's a watermark on it anyways
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #If user clicks the x, the game ends
            playing = False

        #Check if a keystroke is pressed, if it is then, checks which key is pressed then deals with it accordingly. Keystroke input values modified
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                handX_delta = -5
            if event.key == pygame.K_d:
                handX_delta = 5
            if event.key == pygame.K_LSHIFT:
                if projectile_state is "prepped": #"is" seems like another way of writing "==", but im binot too sure
                    projectileSound = mixer.Sound("Shoot.mp3") #PLays this sound once when space is places
                    projectileSound.play()
                    # Get the current x cordinate of the spaceship
                    projectileX = handX
                    shoot_projectile(projectileX, projectileY)

        if event.type == pygame.KEYUP: #If user stops pressing a button (Left or right key), then the change in x position stops
            if event.key == pygame.K_a or event.key == pygame.K_d:
                handX_delta = 0

    handX += handX_delta #Doesnt allow hand to move off screen, different to the other game, as this way it teleports the player back onto the screen, whereas in other shooter it just didn't allow for more input
    if handX <= 0:
        handX = 0
    elif handX >= 690:
        handX = 690 

    for i in range(ENEMY_AMOUNT): #Crystals are indexed between one and 5, thats how they are dealt with individually

        if crystalY[i] > 300:  #For any emeny if its y position id greter than this, its y position if checked until it passes the thershold, where teh game ends
            for j in range(ENEMY_AMOUNT):
                crystalY[j] = 501 #The posittions where if crossed by enemy, player dies. 
            game_finished_words()
            break

            #If the crystal starts goung too far in one direction on the screen, it starts to go the other way
        crystalX[i] += crystalX_delta[i]
        if crystalX[i] <= 0:
            crystalX_delta[i] = 4
            crystalY[i] += crystalY_delta[i]
        elif crystalX[i] >= 750:
            crystalX_delta[i] = -4
            crystalY[i] += crystalY_delta[i]


        collision = isCollision(crystalX[i], crystalY[i], projectileX, projectileY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            projectileY = 480
            projectile_state = "prepped"
            current_points += 1
            crystalX[i] = random.randint(0, 780) #Crystals are placed onto random stops in the screen, both the y and y position  etween two values
            crystalY[i] = random.randint(50, 150)

        crystal(crystalX[i], crystalY[i], i)

    if projectileY <= 0:
        projectileY = 480
        projectile_state = "prepped" #Before a certain point the projectile is only prepped

    if projectile_state == "shoot":  #The y positino of the bullet goes down (Travels up the screen)
        shoot_projectile(projectileX, projectileY)
        projectileY -= projectileY_delta

    hand(handX, handY) #Hand is placed in an x and y position
    show_score(wordsX, wordsY) #Score is showed on this x and y positio 
    pygame.draw.rect(screen, (0,0,0), BORDER) #Draws the death border
    pygame.display.update()
