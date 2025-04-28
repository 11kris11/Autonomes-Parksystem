import pygame
import random
from car import Car

# Diese Klasse soll die Fläche, wo das Auto initiert wird darstellen und sie anzeigen können
class spawnArea:
    x1 = None
    x2 = None
    y1 = None
    y2 = None
    screen = None
    selectedPolygon = None
    
    def __init__(self, screen, polNum):
        self.screen = screen
        self.selectedPolygon = polNum    
        if polNum == 1:
            self.x1 = 600
            self.x2 = 1000
            self.y1 = 0
            self.y2 = 900
        elif polNum == 2:
            self.x1 = 0
            self.x2 = 1600
            self.y1 = 300
            self.y2 = 600
        

    def showSpawn(self, hmm):
        if hmm:
            pygame.draw.rect(self.screen, "red", (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
        elif not hmm:
            pygame.draw.rect(self.screen, "grey", (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))