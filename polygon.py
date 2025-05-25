import random
from typing import List
import pygame

from car import Car


class Polygon:
    screen = None
    toFill = 7
    cars: List[Car] = []

    def __init__(self, screen, width, height, polNum):
        self.height = height
        self.width = width
        self.selectedPolygon = polNum
        self.screen = screen
        self.screen.fill("lightgrey")
        if polNum == 2:
            self.parkingSpaceWidth = self.width / 10 * 2 - 10
            self.parkingSpaceLength = 150
        elif polNum == 1:
            self.parkingSpaceWidth = 265
            self.parkingSpaceLength = height / 10 + height / 10 - 10

    # Hier werden die Parkplätze gezeichnet, Poligon 1 = Rückwärts parkenn
    def draw_polygon_1(self, screen):
        # Fahrbereich
        asphalt1 = pygame.Rect(
            self.width / 10 - 50,
            self.height / 10,
            self.width / 10 * 9 + 100 - self.width / 10,
            self.height / 10 * 8 + 10,
        )
        asphalt2 = pygame.Rect(self.width / 2 - 200, 0, 400, self.height)
        pygame.draw.rect(screen, "grey", asphalt1)
        pygame.draw.rect(screen, "grey", asphalt2)

        # Parkplätze
        vert1 = pygame.Rect(
            self.width / 10 - 50, self.height / 10, 10, self.height / 10 * 8
        )
        vert2 = pygame.Rect(
            self.width / 10 * 9 + 40, self.height / 10, 10, self.height / 10 * 8
        )
        pygame.draw.rect(screen, "white", vert1)
        pygame.draw.rect(screen, "white", vert2)

        for i in range(5):
            horiz1 = pygame.Rect(
                self.width / 10 - 50,
                self.height / 10 + i * self.height / 10 * 8 / 4,
                275,
                10,
            )
            horiz2 = pygame.Rect(
                self.width / 10 * 9 - 225,
                self.height / 10 + i * self.height / 10 * 8 / 4,
                275,
                10,
            )
            pygame.draw.rect(screen, "white", horiz1)
            pygame.draw.rect(screen, "white", horiz2)

    # Hier werden die Parkplätze gezeichnet, Poligon 2 = Seitlich parkenn
    def draw_polygon_2(self, screen):
        # Fahrbereich
        asphalt1 = pygame.Rect(0, self.height / 10, self.width, self.height / 10 * 8)
        pygame.draw.rect(screen, "grey", asphalt1)

        # Parkplätze
        horiz1 = pygame.Rect(self.width / 10, self.height / 10, self.width / 10 * 8, 10)
        horiz2 = pygame.Rect(
            self.width / 10, self.height / 10 * 9 - 10, self.width / 10 * 8, 10
        )
        pygame.draw.rect(screen, "white", horiz1)
        pygame.draw.rect(screen, "white", horiz2)

        for i in range(5):
            vert1 = pygame.Rect(
                self.width / 10 + self.width / 10 * 8 * i / 4, self.height / 10, 10, 160
            )
            vert2 = pygame.Rect(
                self.width / 10 + self.width / 10 * 8 * i / 4,
                self.height / 10 * 8 - 70,
                10,
                160,
            )
            pygame.draw.rect(screen, "white", vert1)
            pygame.draw.rect(screen, "white", vert2)

    # Hier werden geparkte Autos zufällig einem Parkplatz zugeordnet
    def park_cars(self, surface):
        # Definition der Parkplätze
        parkingSpacesX = []  # Liste für die X-Koordinaten der Parkplätze
        parkingSpacesY = []  # Liste für die Y-Koordinaten der Parkplätze
        directions = ["left", "right"]  # Mögliche Ausrichtungen der geparkten Autos
        colors = [
            "pink",
            "brown",
            "black",
            "blue",
            "red",
            "green",
            "cyan",
            "magenta",
            "orange",
            "purple",
        ]  # Verfügbare Farben für die Autos

        if self.selectedPolygon == 1:
            # Bei Rückwärtsparken: Zwei Spalten von Parkplätzen (links und rechts)
            parkingSpacesX = [self.width / 10 - 20, self.width / 10 * 9 - 200]
            # Vier Reihen von Parkplätzen mit gleichmäßigem Abstand
            parkingSpacesY = [
                self.height / 10 + 30,
                self.height / 10 + 30 + self.height / 10 * 8 / 4,
                self.height / 10 + 30 + self.height / 10 * 8 / 4 * 2,
                self.height / 10 + 30 + self.height / 10 * 8 / 4 * 3,
            ]
        if self.selectedPolygon == 2:
            # Bei Seitwärtsparken: Vier Spalten von Parkplätzen mit gleichmäßigem Abstand
            parkingSpacesX = [
                self.width / 10 + 50,
                self.width / 10 + 50 + self.width / 10 * 8 / 4,
                self.width / 10 + 50 + self.width / 10 * 8 / 4 * 2,
                self.width / 10 + 50 + self.width / 10 * 8 / 4 * 3,
            ]
            # Zwei Reihen von Parkplätzen (oben und unten)
            parkingSpacesY = [self.height / 10 + 25, self.height / 10 * 8 - 60]

        # Zufällige uaswahl der Parkplätze
        ammountToFill = random.randint(3, 7)
        filled = []
        for i in range(ammountToFill):
            direction = directions[random.randint(0, 1000) % 2]
            while self.toFill in filled:
                self.toFill = random.randint(0, 1000) % 8
            carColor = colors[random.randint(0, len(colors) - 1)]
            roofColor = colors[random.randint(0, len(colors) - 1)]
            while roofColor == carColor:
                roofColor = colors[random.randint(0, len(colors) - 1)]

            if self.selectedPolygon == 1 and self.toFill not in filled:
                filled.append(self.toFill)
                if self.toFill >= 4:
                    car = Car(
                        parkingSpacesX[1],
                        parkingSpacesY[self.toFill - 4],
                        direction,
                        surface,
                        carColor,
                        roofColor,
                    )
                    car.draw_parked_car(surface)
                    self.cars.append(car.getCarRect())
                if self.toFill < 4:
                    car = Car(
                        parkingSpacesX[0],
                        parkingSpacesY[self.toFill],
                        direction,
                        surface,
                        carColor,
                        roofColor,
                    )
                    car.draw_parked_car(surface)
                    self.cars.append(car.getCarRect())

            if self.selectedPolygon == 2 and self.toFill not in filled:
                filled.append(self.toFill)
                if self.toFill >= 4:
                    car = Car(
                        parkingSpacesX[self.toFill - 4],
                        parkingSpacesY[1],
                        direction,
                        surface,
                        carColor,
                        roofColor,
                    )
                    car.draw_parked_car(surface)
                    self.cars.append(car.getCarRect())

                if self.toFill < 4:
                    car = Car(
                        parkingSpacesX[self.toFill],
                        parkingSpacesY[0],
                        direction,
                        surface,
                        carColor,
                        roofColor,
                    )
                    car.draw_parked_car(surface)
                    self.cars.append(car.getCarRect())

    def drawPolygon(self):
        if self.selectedPolygon == 1:
            self.draw_polygon_1(self.screen)
        elif self.selectedPolygon == 2:
            self.draw_polygon_2(self.screen)
        else:
            print("Polygon nicht gespeichert")  # Debug


# probe
