import pygame
import random
from car import Car

class Polygon:
    width = 0
    height = 0
    selectedPolygon = 0
    screen = None
    toFill = 8

    
    def __init__(self, screen, width, height, polNum):
        self.height = height
        self.width = width
        self.selectedPolygon = polNum
        self.screen = screen
        

    # Hier werden die Parkplätze gezeichnet, Poligon 1 = Rückwärts parkenn
    def draw_polygon_1(self, screen):
        # Fahrbereich
        asphalt1 = pygame.Rect(self.width/10-50, self.height/10, self.width/10*9+100-self.width/10, self.height/10*8+10)
        asphalt2 = pygame.Rect(self.width/2-200, 0, 400, self.height)
        pygame.draw.rect(screen, "grey", asphalt1)
        pygame.draw.rect(screen, "grey", asphalt2)

        # Parkplätze
        vert1 = pygame.Rect(self.width/10-50, self.height/10, 10, self.height/10*8)
        vert2 = pygame.Rect(self.width/10*9+50, self.height/10, 10, self.height/10*8)
        pygame.draw.rect(screen, "white", vert1)
        pygame.draw.rect(screen, "white", vert2)

        for i in range(5):
            horiz1 = pygame.Rect(self.width/10-50, self.height/10 + i*self.height/10*8/4, 275, 10)
            horiz2 = pygame.Rect(self.width/10*9-225, self.height/10 + i*self.height/10*8/4, 275+10, 10)
            pygame.draw.rect(screen, "white", horiz1)
            pygame.draw.rect(screen, "white", horiz2)

    # Hier werden die Parkplätze gezeichnet, Poligon 2 = Seitlich parkenn
    def draw_polygon_2(self, screen):
        # Fahrbereich
        asphalt1 = pygame.Rect(0, self.height/10, self.width, self.height/10*8)
        pygame.draw.rect(screen, "grey", asphalt1)

        # Parkplätze
        horiz1 = pygame.Rect(self.width/10, self.height/10, self.width/10*8, 10)
        horiz2 = pygame.Rect(self.width/10, self.height/10*9-10, self.width/10*8, 10)
        pygame.draw.rect(screen, "white", horiz1)
        pygame.draw.rect(screen, "white", horiz2)

        for i in range(5):
            vert1 = pygame.Rect(self.width/10 + self.width/10*8*i/4, self.height/10, 10, 160)   
            vert2 = pygame.Rect(self.width/10 + self.width/10*8*i/4, self.height/10*8-70, 10, 160)   
            pygame.draw.rect(screen, "white", vert1)
            pygame.draw.rect(screen, "white", vert2)
            
    # Hier werden geparkte Autos zufällig einem Parkplatz zugeordnet
    def park_cars(self):
        # Definition der Parkplätze
        parkingSpacesX = []
        parkingSpacesY = []
        directions = ["left","right"]
        colors = ["pink", "brown", "black", "blue", 
                "red", "green", "cyan", "magenta",
                "orange", "purple"]

        if self.selectedPolygon == 1:
            parkingSpacesX = [self.width / 10 - 20, self.width/10*9-200]
            parkingSpacesY = [self.height / 10 + 30, 
                                self.height / 10 + 30 + self.height/10*8/4, 
                                self.height / 10 + 30 + self.height/10*8/4*2, 
                                self.height / 10 + 30 + self.height/10*8/4*3]
        if self.selectedPolygon == 2:
            parkingSpacesX = [self.width / 10 + 50, 
                                self.width / 10 + 50 + self.width/10*8/4,
                                self.width / 10 + 50 + self.width/10*8/4*2,
                                self.width / 10 + 50 + self.width/10*8/4*3]
            parkingSpacesY = [self.height / 10 + 25, self.height/10*8-60]
            
        # Zufällige uaswahl der Parkplätze
        ammountToFill = random.randint(3,7)
        for i in range(ammountToFill):
            direction = directions[random.randint(0,1000) % 2]
            self.toFill =  random.randint(0,1000) % 8
            carColor =  colors[random.randint(0,len(colors)-1)]
            roofColor = colors[random.randint(0,len(colors)-1)]
            while roofColor == carColor:
                roofColor = colors[random.randint(0,len(colors)-1)]
        
            if self.selectedPolygon == 1:
                if self.toFill >= 4:
                    Car(parkingSpacesX[1], parkingSpacesY[self.toFill - 4], direction, self.screen, carColor, roofColor).draw_parked_car(self.screen)
                if self.toFill < 4:
                    Car(parkingSpacesX[0], parkingSpacesY[self.toFill], direction, self.screen, carColor, roofColor).draw_parked_car(self.screen)
            
            if self.selectedPolygon == 2:
                if self.toFill >= 4:
                    Car(parkingSpacesX[self.toFill - 4], parkingSpacesY[1], direction, self.screen, carColor, roofColor).draw_parked_car(self.screen)
                if self.toFill < 4:
                    Car(parkingSpacesX[self.toFill], parkingSpacesY[0], direction, self.screen, carColor, roofColor).draw_parked_car(self.screen)

    def drawPolygon(self):
        if self.selectedPolygon == 1:
            self.draw_polygon_1(self.screen)
        elif self.selectedPolygon == 2:
            self.draw_polygon_2(self.screen)
        else:
            print("Polygon nicht gespeichert")          # Debug