import pygame


class DefineAgents:

     # constructer funtion to intialize the Agents in the enviroment
    def __init__(self, gd, w, h, agent):
        self.agent = agent
        self.w = w
        self.h = h
        self.Display = gd

        self.image = pygame.transform.scale(pygame.image.load(f'pictures/{agent}.png'), (self.w, self.h))

    def Create(self, x_coordinate, y_coordinate):
        self.Display.blit(self.image, (x_coordinate * self.w, y_coordinate * self.h))
