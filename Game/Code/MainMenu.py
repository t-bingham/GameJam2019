import pygame
import time


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
pygame.display.set_caption('GAME NAME HERE!')
clock = pygame.time.Clock()



# Main Stuff


class screenItem:

    def __init__(self, xPos, yPos, xHitHigh, xHitLow, yHitHigh, yHitLow, imagePathNormal, imagePathClicked=None, imagePathGray=None:
        self.xPos = xPos
        self.yPos = yPos
        self.xHitHigh = xHitHigh
        self.xHitLow = xHitLow
        self.yHitHigh = yHitHigh
        self.yHitLow = yHitLow
        self.imagePathNormal = imagePathNormal
        self.imagePathClicked = imagePathClicked
        self.imagePathGray = imagePathGray

        self.image = imagePathNormal

        if imagePathClicked != None:
            self.canClick = True
        else:
            self.canClick = False


def createBackground(path):
    backgroundImage = pygame.image.load(path)
    backgroundImage = pygame.transform.scale(backgroundImage, (displayWidth, displayHeight))

    return backgroundImage


def close():
    pygame.quit()
    quit()


def main():
    loopExit = False
    latestButtonData = [0, (0, 0)]
    itemsToDisplay = []

    backgroundImage = createBackground('../Images/Backgrounds/MainMenu.png')

    itemsToDisplay.append((backgroundImage, (0, 0)))

    screenItems = []

    while not loopExit:
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

        display.fill(black)

        for item in itemsToDisplay:
            display.blit(item[0], item[1])

        # Push to screen
        pygame.display.update()
        clock.tick(fps)
    
    close()
	

if __name__ == '__main__':
	main()

close()