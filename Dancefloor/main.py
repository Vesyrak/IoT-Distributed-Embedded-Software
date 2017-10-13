import pygame
from copy import copy, deepcopy
import sys
from Agent import Agent
from DJ import DJ
from mqtt import mqtt

width, height = 50, 50
# connecteer met mqtt op host *.101 en poort 1883
matrix = [[Agent() for j in range(width)] for i in range(height)]

# Bereid scherm voor op visualisatie van automata
def visualize_dancefloor():
    # initializeer pygame scherm met size 500x500 pixels
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    # teken een vierkant op het scherm op positie x=0,y=0 met een breedte van 10
    # refresh scherm
    while 1:
        run(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()



def run(screen):
    rect_width = 10
    global matrix
    newMatrix=deepcopy(matrix)
    rect = pygame.Rect(0,0, rect_width, rect_width)
    for i in range(height):
        for j in range(width):
            if i is not 0:
                newMatrix[i][j].influence(matrix[i - 1][j].LikeRates,0)
            if i is not width-1:
                newMatrix[i][j].influence(matrix[i + 1][j].LikeRates, 1)
            if j is not 0:
                newMatrix[i][j].influence(matrix[i][j - 1].LikeRates, 2)
            if j is not height-1:
                newMatrix[i][j].influence(matrix[i][j + 1].LikeRates, 3)
            rect.x=i*rect_width
            rect.y=j*rect_width
            pygame.draw.rect(screen, newMatrix[i][j].color(), rect)
    pygame.display.update()
    matrix=deepcopy(newMatrix)

dj=DJ()
visualize_dancefloor()
