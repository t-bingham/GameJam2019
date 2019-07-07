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


pygame.mixer.pre_init(16384, -16, 2, 1024*3)
pygame.mixer.init()
def playBackground(music):
    #pygame.mixer.quit()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)


def playMusic(music):
    global playingMusic
    global startTime
    global soundLength
    effect = pygame.mixer.Sound(music)
    effect.play()
    playingMusic = True
    soundLength = pygame.mixer.Sound(music)
    soundLength = soundLength.get_length()
    startTime = time.time()


def shop(display, health, ammunition, Mdamage, Rdamage, fuel, money):
    clock = pygame.time.Clock()
    pygame.font.init()
    playBackground('../Audio/Music/shop.wav')

    playMusic('../Audio/Effects/WelcomeShop.wav')

    healthCost = 100
    ammoCost = 100
    MdamageCost = 100
    RdamageCost = 100
    fuelCost = 100
    totalCost = 0
    canIncrease = True

    loopExit = False
    latestButtonData = [0, (0, 0)] # Last mouse button used and where it was used
    itemsToDisplay = [] # Items to blit to screen, and where to put them
    textItems = [totalCost, money, 0, 0, 0, 0, 0] # Text to display

    backgroundImage = createBackground('../Images/Backgrounds/Shop.png') # Load and scale background

    itemsToDisplay.append((backgroundImage, (0, 0), 1)) # Add background to queue

    # Clickable items on screen and their locations
    screenItems = [
        screenItem('purchase', 477, 522, 721, 477, 522, 580, '../Images/Sprites/PushPurchase.png', '../Images/Sprites/Purchase.png', '../Images/Sprites/GrayPurchase.png'),
        screenItem('fuelIncrease', 424, 202, 474, 424, 202, 255, '../Images/Sprites/+PushShop.png', '../Images/Sprites/+Shop.png'),
        screenItem('fuelDecrease', 326, 202, 375, 326, 202, 255, '../Images/Sprites/-PushShop.png', '../Images/Sprites/-Shop.png'),
        screenItem('healthIncrease', 424, 265, 474, 424, 265, 318, '../Images/Sprites/+PushShop.png', '../Images/Sprites/+Shop.png'),
        screenItem('healthDecrease', 326, 265, 375, 326, 265, 318, '../Images/Sprites/-PushShop.png', '../Images/Sprites/-Shop.png'),
        screenItem('rDamIncrease', 424, 323, 474, 424, 323, 376, '../Images/Sprites/+PushShop.png', '../Images/Sprites/+Shop.png'),
        screenItem('rDamDecrease', 326, 323, 375, 326, 323, 376, '../Images/Sprites/-PushShop.png', '../Images/Sprites/-Shop.png'),
        screenItem('mDamIncrease', 424, 387, 474, 424, 387, 440, '../Images/Sprites/+PushShop.png', '../Images/Sprites/+Shop.png'),
        screenItem('mDamDecrease', 326, 387, 375, 326, 387, 440, '../Images/Sprites/-PushShop.png', '../Images/Sprites/-Shop.png'),
        screenItem('ammoIncrease', 424, 452, 474, 424, 452, 505, '../Images/Sprites/+PushShop.png', '../Images/Sprites/+Shop.png'),
        screenItem('ammoDecrease', 326, 452, 375, 326, 452, 505, '../Images/Sprites/-PushShop.png', '../Images/Sprites/-Shop.png')
        ]

    while not loopExit:

        # Event Handling
        for event in pygame.event.get():
            # If the window 'exit' button is pressed
            if event.type == pygame.QUIT:
                textItems = [0, money, 0, 0, 0, 0, 0]
                loopExit = True

            # If the 'esc' key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    textItems = [0, money, 0, 0, 0, 0, 0]
                    loopExit = True
            
            # If any mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                latestButtonData[0] = event.button
                latestButtonData[1] = event.pos
                print("button %3d pressed in the position (%3d, %3d)" %(latestButtonData[0], latestButtonData[1][0], latestButtonData[1][1]))
            
            # If any mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                canIncrease = True
                for clickable in screenItems:
                    latestButtonData = [0, (0, 0)]
                    clickable.regular()

        for clickable in screenItems:
            if latestButtonData[0] == 1:
                if (latestButtonData[1][0] >= clickable.xHitLow) and (latestButtonData[1][0] <= clickable.xHitHigh):
                    if (latestButtonData[1][1] >= clickable.yHitHigh) and (latestButtonData[1][1] <= clickable.yHitLow):
                        if (canIncrease == True) and (clickable.isGray == False):
                            canIncrease = False
                            clickable.clicked()
                            if clickable.name == "Quit":
                                loopExit = True
                            
                            elif clickable.name == "healthIncrease":
                                textItems[2] += 1
                                textItems[0] += healthCost
                            elif clickable.name == "healthDecrease":
                                if textItems[2] > 0:
                                    textItems[2] -= 1
                                    textItems[0] -= healthCost
                            elif clickable.name == "ammoIncrease":
                                textItems[3] += 1
                                textItems[0] += ammoCost
                            elif clickable.name == "ammoDecrease":
                                if textItems[3] > 0:
                                    textItems[3] -= 1
                                    textItems[0] -= ammoCost
                            elif clickable.name == "mDamIncrease":
                                textItems[4] += 1
                                textItems[0] += MdamageCost
                            elif clickable.name == "mDamDecrease":
                                if textItems[4] > 0:
                                    textItems[0] -= MdamageCost
                                    textItems[4] -= 1
                            elif clickable.name == "rDamIncrease":
                                textItems[5] += 1
                                textItems[0] += RdamageCost
                            elif clickable.name == "rDamDecrease":
                                if textItems[5] > 0:
                                    textItems[5] -= 1
                                    textItems[0] -= RdamageCost
                            elif clickable.name == "fuelIncrease":
                                textItems[6] += 1
                                textItems[0] += fuelCost
                            elif clickable.name == "fuelDecrease":
                                if textItems[6] > 0:
                                    textItems[6] -= 1
                                    textItems[0] -= fuelCost
                            elif clickable.name == "purchase":
                                textItems[1] -= textItems[0]
                                loopExit = True
            
            if clickable.image != None:
                itemsToDisplay.append((clickable.image, (clickable.xPos, clickable.yPos), 0))
        
        textToBlit = createText(str(textItems[0]), 'Comic Sand MS', 30, 326, 539) # Total Cost
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(textItems[1]), 'Comic Sand MS', 30, 722, 23) # Money
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(textItems[2]), 'Comic Sand MS', 30, 387, 283) # Health Units
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(textItems[3]), 'Comic Sand MS', 30, 387, 472) # Ammo Units
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(textItems[4]), 'Comic Sand MS', 30, 387, 407) # Mdam Units
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(textItems[5]), 'Comic Sand MS', 30, 387, 342) # Rdam Units
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(textItems[6]), 'Comic Sand MS', 30, 387, 219) # Fuel Units
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(health), 'Comic Sand MS', 30, 526, 23) # Health
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(fuel), 'Comic Sand MS', 30, 416, 23) # Fuel
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(ammunition), 'Comic Sand MS', 30, 617, 23) # Ammo
        itemsToDisplay.append(textToBlit)

        if (textItems[0] > textItems[1]):
            screenItems[0].gray()
            screenItems[0].isGray = True
        elif (screenItems[0].isGray == True):
            screenItems[0].regular()
            screenItems[0].isGray = False

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

    pygame.mixer.music.stop()
    return (health + textItems[2] * 100, ammunition + textItems[3] * 10, Mdamage + textItems[4], Rdamage + textItems[5], fuel + textItems[6] * 100, textItems[1])


