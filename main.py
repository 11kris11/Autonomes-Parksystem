import pygame
from polygon import Polygon
from intro import Intro
from spawnArea import spawnArea
import random
from car import Car
from automation import automation

pygame.init()

# Zur globalen Speicherung
height = 900
width = 1600
einspur = False
running = True
showSpawn =  False
carSurface_rotated = None
carSurface_rotated_rect = None
GAME_OVER = pygame.image.load(r"Autonomes-Parksystem\src\gameOver.jpg")
GAME_OVER_POSITION = (width / 2 - GAME_OVER.get_width() / 2, height / 2 - GAME_OVER.get_height() / 2)
clock = pygame.time.Clock()
ellipse = pygame.Rect(0,0,550,450)
cameraColor = (173, 216, 230, 100)
font = pygame.font.SysFont(None, 60)                                                          # mögliche Richtungen

# Screens und Surfaces
screen = pygame.display.set_mode((width, height))
polygonScreen = pygame.Surface((width, height), pygame.SRCALPHA)
parkedSurface = pygame.Surface((width, height), pygame.SRCALPHA)
carSurface = pygame.Surface((550,450), pygame.SRCALPHA)         # Definition der Surface für das Auto mit den perfekten Masen

def getKeyInput():
    global einspur
    global running
    global showSpawn

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
    moved = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        player.move_backward()
        moved = True
    if keys[pygame.K_UP]:
        player.move_forward()
        moved = True
    if keys[pygame.K_LEFT]:
        player.rotateTire(1, left=True)
    if keys[pygame.K_RIGHT]: 
        player.rotateTire(1, right=True)
    if not moved and player.vel > 0:
        player.reduce_speed()
    if not moved and player.vel < 0:
        player.reduce_speed_backwards()

def selectPolygon():
    selectedPolygon = Intro(screen, font).run()
    return selectedPolygon

def createPolygon():
    polygon = Polygon(polygonScreen, width, height, selectedPolygon)
    polygon.drawPolygon()
    polygon.park_cars(parkedSurface)
    return polygon

def initPlayer():
    player = Car(0, 0, "right", carSurface, "red", "white")
    player.center = (carSurface.get_rect().center[0] - player.car_length / 2, carSurface.get_rect().center[1] - player.car_width / 2)
    player.x = player.center[0] 
    player.y = player.center[1]
    player.surfaceX = random.randint(spawnArea_instance.x1, spawnArea_instance.x2) # Definieren des genauen Startpunktes (Zufällig im Spawn
    player.surfaceY = random.randint(spawnArea_instance.y1, spawnArea_instance.y2) # Bereich -> Offset dient zur verkleinerung der Spawns,
    if selectedPolygon == 1:
        player.gierwinkel += 90
    return player
def gameOver():
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


# Auswahl des poligons und zeichnen der parkenden Autos
selectedPolygon = selectPolygon()
polygon = createPolygon()

# Definition der spawns
spawnArea_instance = spawnArea(polygonScreen, selectedPolygon)
player = initPlayer()
pygame.draw.ellipse(carSurface, cameraColor, ellipse)       # Zeichnen der Kamera


# Change this line to pass the screen instead of carSurface
automation = automation(player)


while running:
    screen.fill((0,0,0,0))
    # Schaue ob es eine kollision gab und falls ja Stop das Spiel
    col = automation.detectCollision(parkedSurface, carSurface_rotated, carSurface_rotated_rect)
    if col != None:
        running = False
    getKeyInput() # Schau ob es ein Key Input gab und reagiere
    spawnArea_instance.showSpawn(showSpawn)  # Zeige den Spawn an, falls showSpawn == True

    # Zeichnen das spielers und der camera 
    player.draw_parked_car(carSurface, einspur)       
    if einspur:
        frontTire_rotated = pygame.transform.rotate(player.frontTire, player.angle)
        frontTire_rotated_rect = frontTire_rotated.get_rect(center=player.frontTireCenter)
    
        carSurface.blit(frontTire_rotated, frontTire_rotated_rect)
    
    # Auto rotieren
    carSurface_rotated = pygame.transform.rotate(carSurface, player.gierwinkel)             # Rotieren das Surface, falls nötig (Lenkung)
    carSurface_rotated_rect = carSurface_rotated.get_rect(center=(player.surfaceX, player.surfaceY)) # Zentrum das Autos
    
    # Alles auf den Mainn Screen zeichnen
    polygonScreen.blit(parkedSurface, (0,0))
    screen.blit(polygonScreen, (0,0))
    screen.blit(carSurface_rotated, carSurface_rotated_rect) # Anzeigen der Surface mit der mitte vom Auto, um die rotation mittig zu halten
    automation.searchParkingSpot(screen, carSurface_rotated)
    pygame.display.flip()
gameOver() # Zeige Game Over an

pygame.quit()