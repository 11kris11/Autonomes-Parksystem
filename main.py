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
screen1 = pygame.Surface((width, height), pygame.SRCALPHA)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)
directions = ["left", "right", "up", "down"]
cameraColor = (173, 216, 230, 100)

# Auswahl des poligons und zeichnen der parkenden Autos
selectedPolygon = Intro(screen, font).run()
screen1.fill("lightgrey")

# Definition der Unterschiedlichkeiten zwischen Polygonen
polygon = Polygon(screen1, width, height, selectedPolygon)
if selectedPolygon == 1:
    polygon.draw_polygon_1(screen1)                                 
    screen2 = pygame.Surface((125, 225), pygame.SRCALPHA)           # Definition der Surface für das Auto mit den perfekten Masen
    direction = directions[random.randint(0,100) % 2 + 2]           # zufällige Wahl von "up" oder "down"
    offset_y = 112                                                  # Hälfte der länge des Autos
    offset_x = 66                                                   # Hälfte der breite des Autos
    cameraScreen = pygame.Surface((350,500), pygame.SRCALPHA)
    ellipse = pygame.Rect(0,0,350,500)

elif selectedPolygon == 2:
    polygon.draw_polygon_2(screen1)
    screen2 = pygame.Surface((225, 125), pygame.SRCALPHA)          # Definition der Surface für das Auto mit den perfekten Masen
    direction = directions[random.randint(0,100) % 2]              # zufällige Wahl von "left" oder "right"
    offset_y = 66                                                  # Hälfte der breite des Autos
    offset_x = 112                                                 # Hälfte der länge des Autos
    cameraScreen = pygame.Surface((500,350), pygame.SRCALPHA)
    ellipse = pygame.Rect(0,0,500,350)
polygon.park_cars()                    # Nach erfolgreicher Definition kommt die Ausführung

# Definition der spawns
spawnArea_instance = spawnArea(screen1, selectedPolygon)
showSpawn =  "false"
x = random.randint(spawnArea_instance.x1 + offset_x, spawnArea_instance.x2 - offset_x) # Definieren des genauen Startpunktes (Zufällig im Spawn
y = random.randint(spawnArea_instance.y1 + offset_y, spawnArea_instance.y2 - offset_y) # Bereich -> Offset dient zur verkleinerung der Spawns,
center = (x, y)                                                                        # da Mittelpunkt als Referenz genommen wird)


player = Car(0, 0, direction, screen2, "black", "white")

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
    pygame.draw.ellipse(cameraScreen, cameraColor, ellipse) # Zeichnen der Kamera
    screen.blit(screen1, (0,0)) # Zeichnen des screen1, wo das Polygon drauf ist
    spawnArea_instance.showSpawn(showSpawn) # Zeige den Spawn an, falls nötig


    player.draw_parked_car(screen2) # Zeichnen auf Surface (bis jetzt noch nicht angezeigt)
    carSurface = pygame.transform.rotate(screen2, 0) # Rotieren das Surface, falls nötig (Lenkung)
    carSurface_rect = carSurface.get_rect(center=center) # Zentrum das Autos
    camera_rect = cameraScreen.get_rect(center=center)
    screen.blit(cameraScreen, camera_rect)
    screen.blit(carSurface, carSurface_rect) # Anzeigen der Surface mit der mitte vom Auto, um die rotation mittig zu halten

    pygame.display.flip()
pygame.quit()