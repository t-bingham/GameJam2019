import pygame
from pygame.locals import *

def name():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    intro = "High Score Name: "
    name = ""
    #tlwgtypo
    font = pygame.font.SysFont("tlwgtypo", 25)
    while True:
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
                    return name
                    pygame.quit()
            elif evt.type == QUIT:
                return
        screen.fill((0, 0, 0))
        block = font.render(intro + name + "_", True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()