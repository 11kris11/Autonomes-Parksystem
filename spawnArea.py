import pygame
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
        self.selfScreen = pygame.Surface((1600, 900), pygame.SRCALPHA)
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
        pixel_color = self.screen.get_at((self.x1+1, self.y1+1))
        if hmm:
            pygame.draw.rect(self.selfScreen, "red", (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
            self.screen.blit(self.selfScreen, (0,0))
        elif not hmm and pixel_color != (190,190,190,255):
            pygame.draw.rect(self.selfScreen, "grey", (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
            self.screen.blit(self.selfScreen, (0,0))