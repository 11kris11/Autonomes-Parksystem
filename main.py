import pygame
from polygon import Polygon
from intro import Intro
from spawnArea import spawnArea
import random
from car import Car
from automation import automation

# pygame setup
height = 900
width = 1600
GAME_OVER = pygame.image.load(r"Autonomes-Parksystem\src\gameOver.jpg")
GAME_OVER_POSITION = (width / 2 - GAME_OVER.get_width() / 2, height / 2 - GAME_OVER.get_height() / 2)
pygame.init()
screen = pygame.display.set_mode((width, height))
polygonScreen = pygame.Surface((width, height), pygame.SRCALPHA)
parkedSurface = pygame.Surface((width, height), pygame.SRCALPHA)
carSurface = pygame.Surface((550,450), pygame.SRCALPHA)         # Definition der Surface für das Auto mit den perfekten Masen
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)                                                          # mögliche Richtungen
cameraColor = (173, 216, 230, 100)
ellipse = pygame.Rect(0,0,550,450)
polygonScreen.fill("lightgrey")





# Auswahl des poligons und zeichnen der parkenden Autos
selectedPolygon = Intro(screen, font).run()
polygon = Polygon(polygonScreen, width, height, selectedPolygon)
polygon.drawPolygon()
polygon.park_cars(parkedSurface)

# Definition der spawns
spawnArea_instance = spawnArea(polygonScreen, selectedPolygon)
showSpawn =  False
einspur = False
player = Car(0, 0, "right", carSurface, "red", "white")
player.center = (carSurface.get_rect().center[0] - player.car_length / 2, carSurface.get_rect().center[1] - player.car_width / 2)
player.x = player.center[0] 
player.y = player.center[1]
player.surfaceX = random.randint(spawnArea_instance.x1, spawnArea_instance.x2) # Definieren des genauen Startpunktes (Zufällig im Spawn
player.surfaceY = random.randint(spawnArea_instance.y1, spawnArea_instance.y2) # Bereich -> Offset dient zur verkleinerung der Spawns,

if selectedPolygon == 1:
    player.gierwinkel += 90

carSurface_rotated = None
carSurface_rotated_rect = None
# Change this line to pass the screen instead of carSurface
automation = automation(player)


running = True
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_e):
                if einspur:
                    einspur = False
                elif not einspur:
                    einspur = True
            if (event.key == pygame.K_s): # Klassisches XOR, falls 1, dann 0, falls 0 dann 1
                if showSpawn:
                    showSpawn = False
                elif not showSpawn:
                    showSpawn = True
    col = automation.detectCollision(parkedSurface, carSurface_rotated, carSurface_rotated_rect)
    if col != None:
        running = False
    
    moved = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_h]:
        player.rotate(1001,right=True)
    if keys[pygame.K_DOWN]:
        player.move_backward()
        moved = True
    if keys[pygame.K_UP]:
        player.move_forward()
        moved = True
    if keys[pygame.K_LEFT]:
        player.rotateTire(0.7, left=True)
        player.angle
    if keys[pygame.K_RIGHT]: 
        player.rotateTire(0.7, right=True)
    if not moved and player.vel > 0:
        player.reduce_speed()
    if not moved and player.vel < 0:
        player.reduce_speed_backwards()

    pygame.draw.ellipse(carSurface, cameraColor, ellipse)       # Zeichnen der Kamera
    spawnArea_instance.showSpawn(showSpawn)                     # Zeige den Spawn an, falls showSpawn == True

    player.draw_parked_car(carSurface, einspur)            # Zeichnen auf Surface (bis jetzt noch nicht angezeigt)

    # creating the front tire
    if einspur:
        frontTire_rotated = pygame.transform.rotate(player.frontTire, player.angle)
        frontTire_rotated_rect = frontTire_rotated.get_rect(center=player.frontTireCenter)
    
        carSurface.blit(frontTire_rotated, frontTire_rotated_rect)
    
    # rotating the carSurface
    carSurface_rotated = pygame.transform.rotate(carSurface, player.gierwinkel)             # Rotieren das Surface, falls nötig (Lenkung)
    carSurface_rotated_rect = carSurface_rotated.get_rect(center=(player.surfaceX, player.surfaceY)) # Zentrum das Autos


    # Update the player's collision rectangle before checking collisions
    player.car = pygame.Rect(carSurface_rotated_rect.x, carSurface_rotated_rect.y, 
                             carSurface_rotated_rect.width, carSurface_rotated_rect.height)
    # Move the collision check to after blitting all surfaces to screen
    # but before display.flip() to make sure the rectangles are visible    
    
    polygonScreen.blit(parkedSurface, (0,0))
    screen.blit(polygonScreen, (0,0))
    screen.blit(carSurface_rotated, carSurface_rotated_rect) # Anzeigen der Surface mit der mitte vom Auto, um die rotation mittig zu halten
    pygame.display.flip()

waiting = True
while waiting:
    screen.fill("black")
    screen.blit(GAME_OVER, GAME_OVER_POSITION)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting = False
    
    clock.tick(30)  # Control the frame rate during waiting

pygame.quit()