import pygame
from polygon import Polygon
from intro import Intro
from spawnArea import spawnArea
import random
from car import Car

# pygame setup
pygame.init()
height = 900
width = 1600
screen = pygame.display.set_mode((width, height))
polygonScreen = pygame.Surface((width, height), pygame.SRCALPHA)
carSurface = pygame.Surface((500,350), pygame.SRCALPHA)         # Definition der Surface für das Auto mit den perfekten Masen
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)                           
directions = ["left", "right"]                                 # mögliche Richtungen
direction = directions[random.randint(0,100) % 2]              # zufällige Wahl von "left" oder "right"
cameraColor = (173, 216, 230, 100)
ellipse = pygame.Rect(0,0,500,350)
polygonScreen.fill("lightgrey")
offset_x = 67
offset_y = 122


# Auswahl des poligons und zeichnen der parkenden Autos
selectedPolygon = Intro(screen, font).run()
polygon = Polygon(polygonScreen, width, height, selectedPolygon)
polygon.drawPolygon()
polygon.park_cars()

# Definition der spawns
spawnArea_instance = spawnArea(polygonScreen, selectedPolygon)
showSpawn =  "false"
x = random.randint(spawnArea_instance.x1 + offset_x, spawnArea_instance.x2 - offset_x) # Definieren des genauen Startpunktes (Zufällig im Spawn
y = random.randint(spawnArea_instance.y1 + offset_y, spawnArea_instance.y2 - offset_y) # Bereich -> Offset dient zur verkleinerung der Spawns,



player = Car(0, 0, direction, carSurface, "black", "white")

running = True
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_s): # Klassisches XOR, falls 1, dann 0, falls 0 dann 1
                if (showSpawn == "false"):
                    showSpawn = "true"
                elif (showSpawn == "true"):
                    showSpawn = "false"
    carSurface.fill("black")
    screen.blit(polygonScreen, (0,0))                           # Zeichnen des Polygons
    pygame.draw.ellipse(carSurface, cameraColor, ellipse)       # Zeichnen der Kamera
    spawnArea_instance.showSpawn(showSpawn)                     # Zeige den Spawn an, falls nötig

    player.center = (carSurface.get_rect().center[0] - offset_y, carSurface.get_rect().center[1] - offset_x)
    player.updatePos()                                          # player.x und player.y mit center player.center überschreiben
    player.draw_parked_car(carSurface)                          # Zeichnen auf Surface (bis jetzt noch nicht angezeigt)

    #carSurface = pygame.transform.rotate(carSurface, 0)        # Rotieren das Surface, falls nötig (Lenkung)
    carSurface_rect = carSurface.get_rect(center=(x, y)) # Zentrum das Autos
    screen.blit(carSurface, carSurface_rect) # Anzeigen der Surface mit der mitte vom Auto, um die rotation mittig zu halten

    pygame.display.flip()
pygame.quit()