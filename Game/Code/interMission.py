import pygame
import random
import time
import shop


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


class musicToPlay:
    def __init__(self, ready=False, music=None):
        self.music = music
        self.ready = ready
    
    def add(self, music):
        self.music = music
        self.ready = True
    
    def play(self):
        self.ready = False
        playMusic(self.music)


def interMission(display, health, ammunition, Mdamage, Rdamage, fuel, money, n):
    global playingMusic
    global startTime
    global soundLength

    nextMusic = musicToPlay()

    clock = pygame.time.Clock()
    pygame.font.init()

    if n == 0:
        playMusic("../Audio/Effects/InterMissionTut.wav")
    else:
        if random.randint(0, 1) == 0:
            playMusic("../Audio/Effects/TimeForMission.wav")
        else:
            playMusic("../Audio/Effects/Interlude.wav")

    damageAmount = 50
    interChange = 100
    numberWords = 3

    words = ["Interest", "Interject", "Interlude", "Interchange", "Intermezzos", "Internment", "Interabang", "Interannual", "Interiority", "Interjoin",
    "Interlining", "Interlarded", "Internality", "Interlayers", "Internecine", "Intertribal", "Intermingle", "Intersperse", "Intervene", "Interoffice",
    "Interplead", "Intergrade", "Interview", "Interstrand", "Intermixing", "Interlinear", "Internuncio", "Interplant", "Interracial", "Internship",
    "Internalise", "Intertill", "Interacting", "Interschool", "Interisland", "Interabang", "Internecine", "Interpose", "Interpret", "Intermingle",
    "Intergraph", "Interlude", "Interview", "Interannual", "Intergrade", "Interlayers", "Interlinear", "Internalise", "Interline", "Internment"
    ] # Words to display
    wordPairs = [True, False, False, True, False, True, True, False, True, False, False, True, True, False, True, False, False, True, True, False,
    False, True, True, False, True, False, True, False, False, True, True, False, True, False, False, True, True, False, True, False, True, False,
    True, False, True, False, False, True, False, True
    ] # Is the word correct?
    word = [words[n], words[n+1]]
    correct = wordPairs[0]

    wordIndex = n * numberWords * 2 - 2
    loopExit = False
    unclicked = True
    getNext = True
    latestButtonData = [0, (0, 0)] # Last mouse button used and where it was used
    itemsToDisplay = [] # Items to blit to screen, and where to put them

    backgroundImage = createBackground('../Images/Backgrounds/intermission.png') # Load and scale background

    itemsToDisplay.append((backgroundImage, (0, 0), 1)) # Add background to queue

    # Clickable items on screen and their locations
    screenItems = [
        screenItem('inter1', 5, 243, 382, 5, 243, 337, '../Images/Sprites/IntermissionButtonPressed.png', '../Images/Sprites/IntermissionButton.png'),
        screenItem('inter2', 413, 243, 800, 413, 243, 337, '../Images/Sprites/IntermissionButtonPressed.png', '../Images/Sprites/IntermissionButton.png')
        ]
    
    playBackground('../Audio/Music/intermission.wav')

    while not loopExit:

        if nextMusic.ready:
            nextMusic.play()

        # Event Handling
        for event in pygame.event.get():
            # If any mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                latestButtonData[0] = event.button
                latestButtonData[1] = event.pos
                print("button %3d pressed in the position (%3d, %3d)" %(latestButtonData[0], latestButtonData[1][0], latestButtonData[1][1]))
            
            # If any mouse button is released
            if event.type == pygame.MOUSEBUTTONUP:
                unclicked = True
                for clickable in screenItems:
                    latestButtonData = [0, (0, 0)]
                    clickable.regular()

        for clickable in screenItems:
            if latestButtonData[0] == 1:
                if not playingMusic:
                    if (latestButtonData[1][0] >= clickable.xHitLow) and (latestButtonData[1][0] <= clickable.xHitHigh):
                        if (latestButtonData[1][1] >= clickable.yHitHigh) and (latestButtonData[1][1] <= clickable.yHitLow):
                            if (unclicked == True) and (clickable.isGray == False):
                                unclicked = False
                                getNext = True
                                clickable.clicked()
                                if clickable.name == "inter1":
                                    if correct == True:
                                        money += interChange
                                        playMusic("../Audio/Effects/coin.wav")
                                        nextMusic.add("../Audio/Effects/MissionRight.wav")
                                    else:
                                        health -= damageAmount
                                        playMusic("../Audio/Effects/damage.wav")
                                        if random.randint(0, 1) == 0:
                                            nextMusic.add("../Audio/Effects/MissionWrong1.wav")
                                        else:
                                            nextMusic.add("../Audio/Effects/MissionWrong2.wav")
                            
                                elif clickable.name == "inter2":
                                    if correct == False:
                                        money += interChange
                                        playMusic("../Audio/Effects/coin.wav")
                                        nextMusic.add("../Audio/Effects/MissionRight.wav")
                                    else:
                                        health -= damageAmount
                                        playMusic("../Audio/Effects/damage.wav")
                                        if random.randint(0, 1) == 0:
                                            nextMusic.add("../Audio/Effects/MissionWrong1.wav")
                                        else:
                                            nextMusic.add("../Audio/Effects/MissionWrong2.wav")
            
            if clickable.image != None:
                itemsToDisplay.append((clickable.image, (clickable.xPos, clickable.yPos), 0))
        
        textToBlit = createText(str(money), 'Comic Sand MS', 30, 262, 440)
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(health), 'Comic Sand MS', 30, 430, 440)
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(ammunition), 'Comic Sand MS', 30, 348, 440)
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(fuel), 'Comic Sand MS', 30, 502, 440)
        itemsToDisplay.append(textToBlit)

        textToBlit = createText(str(word[0]), 'Comic Sand MS', 42, 107, 281)
        itemsToDisplay.append(textToBlit)
        textToBlit = createText(str(word[1]), 'Comic Sand MS', 42, 523, 281)
        itemsToDisplay.append(textToBlit)

        if not playingMusic:
            if getNext:
                if wordIndex >= (n * numberWords * 2 + numberWords * 2) - 2:
                    loopExit = True
                else:
                    getNext = False
                    wordIndex += 2
                    word[0] = words[wordIndex]
                    word[1] = words[wordIndex + 1]
                    correct = wordPairs[wordIndex]
        
        stopTime = time.time()
        if ((stopTime - startTime) > soundLength) and not pygame.mixer.get_busy():
            playingMusic = False

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

    health, ammunition, Mdamage, Rdamage, fuel, money = shop.shop(display, health, ammunition, Mdamage, Rdamage, fuel, money)
    return (health, ammunition, Mdamage, Rdamage, fuel, money)

