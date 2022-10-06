import os
import random
import pygame
from sys import exit

pygame.init()

# variables for game
gameWidth = 840
gameHeight = 840
picSize = 128
gameColumns = 5
gameRows = 4
padding = 7
topPadding = 30
leftMargin = (gameWidth - ((picSize + padding) * gameColumns)) // 2
rightMargin = leftMargin
topMargin = (gameHeight - ((picSize + padding) * gameRows)) // 2
bottomMargin = (gameHeight - ((picSize + padding) * gameRows)) // 2
GREEN = (253, 194, 12)
selection1 = None
selection2 = None
winningScreen = pygame.image.load("win.png")
winningScreenRect = winningScreen.get_rect()

#loading the pygame screen
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("CoGhent Memory")
gameIcon = pygame.image.load("elmo.png")
pygame.display.set_icon(gameIcon)

#achtergrond instellen
bgImage = pygame.image.load("background.png")
bgImageRect = bgImage.get_rect()

#create list of memory pictures
memoryPictures = []
for item in os.listdir("images/"):
    memoryPictures.append(item.split('.')[0])
memoryPictureCopy = memoryPictures.copy()
memoryPictures.extend(memoryPictureCopy)
memoryPictureCopy.clear()
random.shuffle(memoryPictures)

#load images into game
memPics = []
memPicsRect = []
hiddenImages = []
for item in memoryPictures:
    picture = pygame.image.load(f"images/{item}.png")
    picture = pygame.transform.scale(picture, (picSize, picSize))
    memPics.append(picture)
    pictureRect = picture.get_rect()
    memPicsRect.append(pictureRect)

for i in range(len(memPicsRect)):
    memPicsRect[i][0] = leftMargin + ((picSize + padding) * (i % gameColumns))
    memPicsRect[i][1] = topMargin + ((picSize + padding) * (i % gameRows))
    hiddenImages.append(False)

gameLoop = True
while gameLoop:
    #load background image
    screen.blit(bgImage, bgImageRect)

    #input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in memPicsRect:
                if item.collidepoint(event.pos):
                    if not hiddenImages[memPicsRect.index(item)]:
                        if selection1 != None:
                            selection2 = memPicsRect.index(item)
                            hiddenImages[selection2] = True
                        else:
                            selection1 = memPicsRect.index(item)
                            hiddenImages[selection1] = True

    for i in range(len(memoryPictures)):
        if hiddenImages[i] == True:
            screen.blit(memPics[i], memPicsRect[i])
        else:
            pygame.draw.rect(screen, GREEN, (memPicsRect[i][0], memPicsRect[i][1], picSize, picSize))
    pygame.display.update()

    if selection1 != None and selection2 != None:
        if memoryPictures[selection1] == memoryPictures[selection2]:
            selection1, selection2 = None, None
        else:
            pygame.time.wait(1000)
            hiddenImages[selection1] = False
            hiddenImages[selection2] = False
            selection1, selection2 = None, None

    win = 1
    for number in range(len(hiddenImages)):
        win *= hiddenImages[number]

    if win == 1:
        screen.blit(winningScreen, winningScreenRect)
        pygame.display.update()
        pygame.time.wait(4000)
        gameLoop = False

