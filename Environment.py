# THE ENIRONMENT CLASS IS USED TO SET UP THE ENVIRONMENT IN WHICH WE TEST OUR AGAENTS
# CREATED ON 04-12-2022

from DefineAgents import DefineAgents
import numpy as np
import pygame
from random import random, randrange



# Defining the colours to be used

TEXT_COLOR = (0, 0, 220)
BLUE = (0, 0, 255)
#GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (188, 233, 84)


class Field:

    def __init__(self, Playgroung_Display, environmentMatrix):  # Setting up the environment to play in

        self.rows = environmentMatrix.r #getting the rows
        self.columns = environmentMatrix.c #getting the columns

        self.Display = Playgroung_Display  # redering the playground

        playgroundWidth, playgroundHeight = Playgroung_Display.get_size() #getting the size
        playgroundHeight -= 100  

        self.w = playgroundWidth // self.columns
        self.h = playgroundHeight // self.rows

        #  Using the constructor to define the agents
        self.Farmer = DefineAgents(self.Display, self.w, self.h, "Farmer")
        self.Crow = DefineAgents(self.Display, self.w, self.h, "Crow")
        self.Shifts = {'crow': 150, 'farmer': 150}


        # Defining the Walls in the environment
        self.Walls = environmentMatrix.Walls
        self.Wheat_Icon = pygame.transform.scale(pygame.image.load('pictures/Wheat.png'), (self.w, self.h))

    # this funtions defines the current state of the class
    def getCurrentState(self):
        self.CurrentState = {
            'crow': (self.Crow_Pos[0] - self.Farmer_Pos[0], self.Crow_Pos[1] - self.Farmer_Pos[1], self.Crow_Pos[0] - self.Wheat_Pos[0], self.Crow_Pos[1] - self.Wheat_Pos[1]),
            'farmer': (self.Farmer_Pos[0] - self.Crow_Pos[0],self.Farmer_Pos[1] - self.Crow_Pos[1])}  # Using the wheat location the farmer can track the crow
        return self.CurrentState

    # As soon as we have crow catching the wheat or the farmer catching the crow we rest the playground
    def reset_grid(self):
        self.Wheat_Pos = list(np.random.randint(0, 9, 2))
        self.Farmer_Pos= [8,9]
        self.Crow_Pos = [0,0]

        for Wall in self.Walls:
            if self.Wheat_Pos == Wall:
                self.Wheat_Pos[1] -= 1
            if self.Crow_Pos == Wall:
                self.Crow_Pos[1] -= 1
            if self.Farmer_Pos == Wall:
                self.Farmer_Pos[1] -= 1
        self.Shifts['farmer'] = 125
        self.Shifts['farmer'] = 125
        return self.getCurrentState()

    
    def display_grid(self, iteration):

        self.Farmer.Create(self.Farmer_Pos[0], self.Farmer_Pos[1])
        self.Crow.Create(self.Crow_Pos[0], self.Crow_Pos[1])

        self.Display.blit(self.Wheat_Icon, (self.Wheat_Pos[0] * self.w, self.Wheat_Pos[1] * self.h))

        for wall in self.Walls:
            wall_dimension = [self.w * wall[0], self.h * wall[1], self.w, self.h]
            pygame.draw.rect(self.Display, BLACK, wall_dimension)
        
        self.displayIteration(iteration)


    def step(self, crow_action, farmer_action):
        
        intialValue = False
        incentive = {'crow': -1, 'farmer': -1}
        finish = False
        data = {
            'wheat_got': intialValue,
            'crow_got': intialValue,
            'x_coordinate': -1, 
            'y_coordinate': -1,
            'w': self.w,
            'h': self.h
        }

        self.Shifts['farmer'] -= 1
        self.Shifts['crow'] -= 1
        if self.Shifts['farmer'] == 0 or self.Shifts['crow'] == 0:
            finish = True

        self.update_Steps(crow_action, farmer_action)

        if self.Crow_Pos == self.Wheat_Pos:
            finish = True
            incentive['crow'] = 50
            data['wheat_got'], data['x'], data['y'] = True, self.Crow_Pos[0], self.Crow_Pos[1]

        if self.Farmer_Pos == self.Crow_Pos:
            finish = True
            incentive['farmer'] = 50
            incentive['crow'] = -20
            data['crow_got'], data['x'], data['y'] = True, self.Crow_Pos[0], self.Crow_Pos[1]

        for Walls in self.Walls:
            if self.Crow_Pos == Walls:
                incentive['crow'] = -20
                self.Crow_Pos = [0, 0]

            if self.Farmer_Pos == Walls:
                incentive['farmer'] = -20
                self.Farmer_Pos = [8, 9]

        return self.getCurrentState(), incentive, finish, data


    def displayIteration(self, iterations):
        font = pygame.font.SysFont(None, 30)
        text = font.render("Iteration: {}".format(iterations), True, BLACK)
        self.Display.blit(text, (1, 1))


    def getChanges(self, move):
        newXPosition, newYPosition = 0, 0
        if move == 0:
            newXPosition = 1  
        elif move == 4:
            newXPosition == -1  
            newYPosition == -1  
        elif move == 3:
            newYPosition = 1  
        elif move == 2:
            newYPosition = -1  
        elif move == 1:
            newXPosition = -1  
        elif move == 5:
            newXPosition == -1  
            newYPosition == 1
        elif move == 5:
            newXPosition == 1   
            newYPosition == 1
        elif move == 5:
            newXPosition == 1   
            newYPosition == -1

        return newXPosition, newYPosition


    def update_Steps(self, crow_action, farmer_action):
        crow_new_pos = list(self.getChanges(crow_action))
        farmer_new_pos = list(self.getChanges(farmer_action))



        self.Crow_Pos[0] += crow_new_pos[0]
        self.Crow_Pos[1] += crow_new_pos[1]
        self.Farmer_Pos[0] += farmer_new_pos[0]
        self.Farmer_Pos[1] += farmer_new_pos[1]

        self.Crow_Pos = list(self.checkBounds(self.Crow_Pos))
        self.Farmer_Pos = list(self.checkBounds(self.Farmer_Pos))


    def checkBounds(self, coordinate):
        if coordinate[0] < 0:
            coordinate[0] = 0
        if coordinate[0] > self.columns -1:
            coordinate[0] = self.columns -1 
        if coordinate[1] < 0:
            coordinate[1] = 0
        if coordinate[1] > self.rows - 1:
            coordinate[1] = self.rows - 1
        return coordinate


class CreateField:

    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.Walls = []
        for i in range(0, self.r):
            for j in range(1, self.c):
                if i%4 == 1 and j%2 == 1:
                    self.Walls.append([i, j])
                elif i%4 == 3 and j%2 == 0:
                    self.Walls.append([i,j])
        print(self.Walls)
