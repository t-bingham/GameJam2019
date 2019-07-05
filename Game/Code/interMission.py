import pygame
import random
import time


# Definitions
displayWidth = 800
displayHeight = 600
fps = 60


# Colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)



# Main Stuff

class screenItem:
    def __init__(self, name, xPos, yPos, xHitHigh, xHitLow, yHitHigh, yHitLow, imagePathClicked, imagePathNormal=None, imagePathGray=None):
        self.name = name
        self.xPos = xPos
        self.yPos = yPos
        self.xHitHigh = xHitHigh
        self.xHitLow = xHitLow
        self.yHitHigh = yHitHigh
        self.yHitLow = yHitLow

        if imagePathNormal != None:
            self.imagePathNormal = pygame.image.load(imagePathNormal)
            self.imagePathNormal = pygame.transform.scale(self.imagePathNormal, ((xHitHigh - xHitLow), (yHitLow - yHitHigh)))
        else:
            self.imagePathNormal = None
        
        if imagePathGray != None:
            self.imagePathGray = pygame.image.load(imagePathGray)
            self.imagePathGray = pygame.transform.scale(self.imagePathGray, ((xHitHigh - xHitLow), (yHitLow - yHitHigh)))
        else:
            self.imagePathGray = None

        self.imagePathClicked = pygame.image.load(imagePathClicked)
        self.imagePathClicked = pygame.transform.scale(self.imagePathClicked, ((xHitHigh - xHitLow), (yHitLow - yHitHigh)))

        self.image = self.imagePathNormal
        self.isGray = False
    
    def clicked(self):
        self.image = self.imagePathClicked
    
    def regular(self):
        self.image = self.imagePathNormal
    
    def gray(self):
        self.image = self.imagePathGray


def createBackground(path):
    backgroundImage = pygame.image.load(path)
    backgroundImage = pygame.transform.scale(backgroundImage, (displayWidth, displayHeight))

    return backgroundImage


def createText(text, fontType, size, xPos, yPos):
    myFont = pygame.font.SysFont(fontType, size)
    textsurface = myFont.render(text, False, (0, 0, 0))

    return (textsurface, (xPos, yPos), 0)


def interMission(display, health, money, n):
    clock = pygame.time.Clock()
    pygame.font.init()

    damageAmount = 1
    interChange = 1
    numberWords = 5

    words = ["Interact", "Interject", "Interlude", "Interchange"] # Words to display
    wordPairs = [True, False, False, True] # Is the word correct?
    word = [words[n], words[n+1]]

    wordIndex = n * numberWords * 2 - 2
    loopExit = False
    unclicked = True
    getNext = True
    latestButtonData = [0, (0, 0)] # Last mouse button used and where it was used
    itemsToDisplay = [] # Items to blit to screen, and where to put them

    backgroundImage = createBackground('../Images/Backgrounds/Shop.png') # Load and scale background

    itemsToDisplay.append((backgroundImage, (0, 0), 1)) # Add background to queue

    # Clickable items on screen and their locations
    screenItems = [
        screenItem('inter1', 285, 200, 315, 285, 200, 230, '../Images/Sprites/StartButtonClicked.png', '../Images/Sprites/+.png'),
        screenItem('inter2', 285, 100, 315, 285, 100, 130, '../Images/Sprites/StartButtonClicked.png', '../Images/Sprites/+.png')
        ]

    while not loopExit:

        # Event Handling
        for event in pygame.event.get():
            # If any mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                latestButtonData[0] = event.button
                latestButtonData[1] = event.pos
                #print("button %3d pressed in the position (%3d, %3d)" %(latestButtonData[0], latestButtonData[1][0], latestButtonData[1][1]))
            
            # If any mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                unclicked = True
                for clickable in screenItems:
                    latestButtonData = [0, (0, 0)]
                    clickable.regular()

        for clickable in screenItems:
            if latestButtonData[0] == 1:
                if (latestButtonData[1][0] >= clickable.xHitLow) and (latestButtonData[1][0] <= clickable.xHitHigh):
                    if (latestButtonData[1][1] >= clickable.yHitHigh) and (latestButtonData[1][1] <= clickable.yHitLow):
                        if (unclicked == True) and (clickable.isGray == False):
                            unclicked = False
                            getNext = True
                            clickable.clicked()
                            if clickable.name == "inter1":
                                if correct == True:
                                    money += interChange
                                else:
                                    health -= damageAmount
                            
                            elif clickable.name == "inter2":
                                if correct == False:
                                    money += interChange
                                else:
                                    health -= damageAmount
            
            if clickable.image != None:
                itemsToDisplay.append((clickable.image, (clickable.xPos, clickable.yPos), 0))
        
        textToBlit = createText(str(money), 'Comic Sand MS', 30, 400, 150)
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(health), 'Comic Sand MS', 30, 400, 175)
        itemsToDisplay.append(textToBlit)

        textToBlit = createText(str(word[0]), 'Comic Sand MS', 30, 285, 200)
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(word[1]), 'Comic Sand MS', 30, 285, 100)
        itemsToDisplay.append(textToBlit)

        if getNext:
            if wordIndex > (n * numberWords * 2 + numberWords * 2):
                loopExit = True
            else:
                getNext = False
                wordIndex += 2
                word[0] = words[wordIndex]
                word[1] = words[wordIndex + 1]
                correct = wordPairs[wordIndex]

        display.fill(black)
        newDisp = []
        for item in itemsToDisplay:
            display.blit(item[0], item[1])
            if item[2] == 1:
                newDisp.append(item)
        itemsToDisplay = newDisp

        # Push to screen
        pygame.display.update()
        clock.tick(fps)

    return (health, money)

