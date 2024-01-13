# THIS IS THE MAIN CLASS AND THIS HELPS IN ORCHESTRATE THE OTHER CLASSES
# CREATED ON 04-12-2022

from Environment import Field, CreateField
import time
from Agent import QLA
import pygame


# defining colors for the grid 
BLACK = (0, 0, 0)
#GREEN = (0, 150, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)



pygame.init()
pygame.display.set_caption('The Field')
environmentDisplay = pygame.display.set_mode((600, 700))
gameTime = pygame.time.Clock()

gridEnvironment = CreateField(r=10, c=10)
environment = Field(environmentDisplay, gridEnvironment)

# intializing the farmer and the row agents
farmer = QLA(environment, alpha=0.1, gamma=1.0, nA=4)
crow = QLA(environment, alpha=0.1, gamma=1.0, nA=4)


# this function displays the score of grab and steal
def displayInfo(wheat, steal):
    Coord = [0, 600, 600, 5]
    pygame.draw.rect(environmentDisplay, BLACK, Coord)
    font = pygame.font.SysFont(None, 40)
    grab = font.render("crow gets the wheat:{}".format(wheat), True, BLACK)
    steal = font.render("crow gets caught: {}".format(steal), True, BLACK)

    displayWidth = 50
    grabHeight = 610
    stealHeight = 655
    environmentDisplay.blit(grab, (displayWidth, grabHeight))
    environmentDisplay.blit(steal, (displayWidth, stealHeight))



crow_got = 0
wheat_got = 0


def draw_Rectangle(getColor, x_coordinate, y_coordinate, w, h):
    pygame.draw.rect(environmentDisplay, getColor, [w * x_coordinate, h * y_coordinate, w, h], 10)
    pygame.display.update()
    time.sleep(2)


epsilon = 1.0
epsilon_decay = 0.99
epsilon_min = 0.05

totalGetwayInterations = 1000

# looping the value over the getaways
for getaway in range(1, totalGetwayInterations+1):

    if 0 == getaway % 50:
        print("\r{} Rounds completed/Out of {}".format(getaway, totalGetwayInterations), end="")


    if 0 == getaway % 500:
        print("\nCrow got wheat: {}".format(wheat_got)  + "\n" + "Farmer got crow: {}".format(crow_got))


    epsilon = max(epsilon * epsilon_decay, epsilon_min)

    currentState = environment.reset_grid()
    crow_action = crow.greedyAlgorithm(currentState['crow'], epsilon)
    farmer_action = farmer.greedyAlgorithm(currentState['farmer'], epsilon)

    environment.display_grid(getaway)

    running = True
    while running:

        events = pygame.event.get()
        for i in range(len(events)):
            if events[i].type == pygame.QUIT:
                pygame.quit()
                quit()

        next, incentive, finish, data = environment.step(crow_action, farmer_action)

        # the agents graulally teach and here we define the learning calls 
        # teach function is defined in the agent classs
        crow.teach(currentState['crow'], crow_action, incentive['crow'], next['crow'])
        farmer.teach(currentState['farmer'], farmer_action, incentive['farmer'], next['farmer'])

        # rendering the environment
        environmentDisplay.fill(WHITE)
        environment.display_grid(getaway)
        displayInfo(wheat_got, crow_got)

        # update the display as soon as one of the agents achive the target
        pygame.display.update()
        gameTime.tick(100)

        if finish:
            if data['wheat_got']:
                wheat_got += 1
                draw_Rectangle(RED, data['x_coordinate'], data['y_coordinate'], data['w'], data['h'])

            if data['crow_got']:
                crow_got += 1
                draw_Rectangle(RED, data['x_coordinate'], data['y_coordinate'], data['w'], data['h'])
            break

        currentState = next
        crow_action = crow.greedyAlgorithm(currentState['crow'], epsilon)
        farmer_action = farmer.greedyAlgorithm(currentState['farmer'], epsilon)

# All the policies are saved as pickle files
farmer.save()
crow.save()
farmer.saveEachIteration('_farmer')
crow.saveEachIteration('_crow')

