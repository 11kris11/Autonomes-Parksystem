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
carSurface = pygame.Surface((450,550), pygame.SRCALPHA)         # Definition der Surface für das Auto mit den perfekten Masen
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)                           
directions = ["left", "right"]                                 # mögliche Richtungen
direction = directions[random.randint(0,100) % 2]              # zufällige Wahl von "left" oder "right"
cameraColor = (173, 216, 230, 100)
ellipse = pygame.Rect(0,0,450,550)
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
showSpawn =  False
player = Car(0, 0, "up", carSurface, "black", "white")
player.x = random.randint(spawnArea_instance.x1 + offset_x, spawnArea_instance.x2 - offset_x) # Definieren des genauen Startpunktes (Zufällig im Spawn
player.y = random.randint(spawnArea_instance.y1 + offset_y, spawnArea_instance.y2 - offset_y) # Bereich -> Offset dient zur verkleinerung der Spawns,


player.center = (carSurface.get_rect().center[0] - offset_x, carSurface.get_rect().center[1] - offset_y)
player.updatePos()                                          # player.x und player.y mit center player.center überschreiben

iter = 0
moved = None

running = True
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_s): # Klassisches XOR, falls 1, dann 0, falls 0 dann 1
                if showSpawn:
                    showSpawn = False
                elif not showSpawn:
                    showSpawn = True
    if moved:
        iter += 1
    if not moved:
        iter = 0
    moved = False
    #movedForward = False
    #movedBackward = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_h]:
        player.rotate(1001,right=True)
    if keys[pygame.K_DOWN]:
        player.move_backward()
        moved = True
    if keys[pygame.K_UP]:
        player.move_forward()
        moved = True
    if keys[pygame.K_LEFT] and moved and iter >= 15: #(movedForward or movedBackward):
        player.rotate(0.5, left=True)
    if keys[pygame.K_RIGHT] and moved: #(movedForward or movedBackward):
        player.rotate(0.5, right=True)

    if not moved and player.vel > 0:
        player.reduce_speed()
    if not moved and player.vel < 0:
    #if not movedBackward:
        player.reduce_speed_backwards()

    carSurface.fill((0,0,0,0))
    pygame.draw.ellipse(carSurface, cameraColor, ellipse)       # Zeichnen der Kamera
    spawnArea_instance.showSpawn(showSpawn)                     # Zeige den Spawn an, falls nötig

    player.draw_parked_car(carSurface)                          # Zeichnen auf Surface (bis jetzt noch nicht angezeigt)
    
    carSurface_rotated = pygame.transform.rotate(carSurface, player.angle)             # Rotieren das Surface, falls nötig (Lenkung)
    carSurface_rotated_rect = carSurface_rotated.get_rect(center=(player.surfaceX, player.surfaceY)) # Zentrum das Autos

    screen.blit(polygonScreen, (0,0))                        # Zeichnen des Polygons
    screen.blit(carSurface_rotated, carSurface_rotated_rect) # Anzeigen der Surface mit der mitte vom Auto, um die rotation mittig zu halten
    
    pygame.display.flip()
pygame.quit()