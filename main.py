import pygame
from polygon import Polygon
from intro import Intro
from spawnArea import spawnArea

# pygame setup
pygame.init()
height = 900
width = 1600
screen = pygame.display.set_mode((width, height))
screen2 = pygame.Surface((width, height), pygame.SRCALPHA)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

# Auswahl des poligons und zeichnen der parkenden Autos
selectedPolygon = Intro(screen, font).run()
screen.fill("lightgrey")

polygon = Polygon(screen, width, height, selectedPolygon)
if selectedPolygon == 1:
        polygon.draw_polygon_1(screen)
elif selectedPolygon == 2:
    polygon.draw_polygon_2(screen)
polygon.park_cars()

# Definition der spawns
spawnArea_instance = spawnArea(screen2, selectedPolygon)
showSpawn =  "false"
running = True
player = spawnArea_instance.carToSpawn("left", "black", "white")
player.draw_parked_car(screen2)
x = 0
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_s):
                if (showSpawn == "false"):
                    showSpawn = "true"
                elif (showSpawn == "true"):
                    showSpawn = "false"
    
    spawnArea_instance.showSpawn(showSpawn)
    
    if x < 100:
        player.moveCarX()
        x = x + 1
    
    
    screen2.fill((0,0,0,0))
    
    player.draw_parked_car(screen2)
    
    screen.blit(screen2, (0,0))

    # Flip the display to put your work on screen
    pygame.display.flip()
pygame.quit()