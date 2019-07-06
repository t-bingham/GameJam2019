import pygame
import random
import time

import game


# Initialise Pygame
pygame.init()


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


# Initialisations
display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('The Interim')
clock = pygame.time.Clock()
pygame.font.init()



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


def playMovie(clip):
    pygame.mouse.set_visible(False)

    pygame.mixer.quit()
    movie = pygame.movie.Movie(clip)
    movie_screen = pygame.Surface(movie.get_size()).convert()
    #movie_screen = pygame.transform.scale(movie_screen, (displayWidth, displayHeight))
    movie.set_display(movie_screen)
    movie.play()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    movie.stop()
                    running = False
        
        if not movie.get_busy():
            movie.stop()
            running = False
        
        display.fill(black)
        display.blit(movie_screen, (displayWidth / 2 - movie.get_size()[0] / 2, displayHeight / 2 - movie.get_size()[1] / 2))
        pygame.display.update()
        clock.tick(fps)

    pygame.mouse.set_visible(True)


def begin():
    # Close the window
    global display

    # Cutscene
    playMovie("../Images/Intro.mpg")

    pygame.quit()
    start = time.time()
    levelNumber = 1

    playerName = ""

    health = 87
    ammunition = 23
    Mdamage = 1
    Rdamage = 1
    fuel = 13
    money = 1233

    while (levelNumber < 6) and (type(playerName) == str):
        playerName = game.game(levelNumber, health, ammunition, Mdamage, Rdamage, fuel, money) # Start the game
        levelNumber += 1

    # Reopen the window
    end = time.time()
    playerTime = int(end - start)

    display = pygame.display.set_mode((displayWidth, displayHeight))
    pygame.display.set_caption('The Interim')
    clock = pygame.time.Clock()
    pygame.font.init()

    if type(playerName) == str:
        if playerName.strip() == '':
            playerName = '*'

    return [playerName, playerTime]


def close():
    pygame.quit()
    quit()


def main():
    loopExit = False
    startGame = False
    latestButtonData = [0, (0, 0)] # Last mouse button used and where it was used
    itemsToDisplay = [] # Items to blit to screen, and where to put them
    textItems = [] # Text to display for score sheet
    scores = [] # Player scores from the game
    scoreData = {} # Player names and scores from the game

    backgroundImage = createBackground('../Images/Backgrounds/MainMenu.png') # Load and scale background

    itemsToDisplay.append((backgroundImage, (0, 0), 1)) # Add background to queue

    # Clickable items on screen and their locations
    screenItems = [
        screenItem('Start', 285, 100, 315, 285, 100, 130, '../Images/Sprites/StartButtonClicked.png', '../Images/Sprites/StartButton.jpg'),
        screenItem('Quit', 285, 200, 315, 285, 200, 230, '../Images/Sprites/QuitButtonClicked.jpeg', '../Images/Sprites/QuitButton.png')
        ]

    while not loopExit:
        # Enter actual game?
        if startGame == True:
            data = begin() # Start the game

            if type(data[0]) == str:
                # Organise high score data
                while(data[0] in scoreData):
                    data[0] += "-"
            
                scoreData[data[0]] = data[1]
                scores.append(data[1])
                scores.sort()

            for clickable in screenItems:
                clickable.regular()
            
            # Game has ended, stay in main menu
            startGame = False
            latestButtonData = [0, (0, 0)]


        # Event Handling
        for event in pygame.event.get():
            # If the window 'exit' button is pressed
            if event.type == pygame.QUIT:
                loopExit = True

            # If the 'esc' key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loopExit = True
            
            # If any mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                latestButtonData[0] = event.button
                latestButtonData[1] = event.pos
                #print("button %3d pressed in the position (%3d, %3d)" %(latestButtonData[0], latestButtonData[1][0], latestButtonData[1][1]))

        for i in range(0, 5):
            if len(scores) <= i:
                break
            score = scores[i]
            playerName = "-"
            for name in scoreData:
                if scoreData[name] == score:
                    playerName = name
                    break
            
            while playerName[len(playerName)-1] == '-':
                playerName = playerName.strip('-')
            if len(playerName) > 5:
                playerName = playerName[:5]

            textToBlit = createText(playerName, 'Comic Sand MS', 30, 400, 150 + i * 25)
            itemsToDisplay.append(textToBlit)
            textToBlit = createText(str(score), 'Comic Sand MS', 30, 500, 150 + i * 25)
            itemsToDisplay.append(textToBlit)

        for clickable in screenItems:
            if latestButtonData[0] == 1:
                if (latestButtonData[1][0] >= clickable.xHitLow) and (latestButtonData[1][0] <= clickable.xHitHigh):
                    if (latestButtonData[1][1] >= clickable.yHitHigh) and (latestButtonData[1][1] <= clickable.yHitLow):
                        if not clickable.isGray:
                            clickable.clicked()
                            if clickable.name == "Start":
                                startGame = True
                            elif clickable.name == "Quit":
                                loopExit = True
            
            if clickable.image != None:
                itemsToDisplay.append((clickable.image, (clickable.xPos, clickable.yPos), 0))

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
    
    close()
	

if __name__ == '__main__':
	main()

close()
