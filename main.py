import random

import pygame
from automation import automation
from car import Car
from polygon import Polygon
from screens import Screens
from spawnArea import spawnArea

pygame.init()

# Zur globalen Speicherung
height = 900
width = 1600
timeCounter = 0
showMsg = False
einspur = False
running = True
showSpawn = False
carSurface_rotated = None
carSurface_rotated_rect = None
GAME_OVER = pygame.image.load(r"src\gameOver.jpg")
GAME_OVER_POSITION = (
    width / 2 - GAME_OVER.get_width() / 2,
    height / 2 - GAME_OVER.get_height() / 2,
)
clock = pygame.time.Clock()
ellipse = pygame.Rect(0, 0, 550, 450)
cameraColor = (173, 216, 230, 100)
font = pygame.font.SysFont(None, 60)
timer = 0

# Screens und Surfaces
screen = pygame.display.set_mode((width, height))
polygonScreen = pygame.Surface((width, height), pygame.SRCALPHA)
parkedSurface = pygame.Surface((width, height), pygame.SRCALPHA)
carSurface = pygame.Surface(
    (550, 450), pygame.SRCALPHA
)  # Definition der Surface für das Auto mit den perfekten Masen
screens = Screens(screen, font)  # mögliche Richtungen


def getKeyInput():
    global einspur
    global running
    global showSpawn
    global showMsg
    global timer

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if einspur:
                    einspur = False
                elif not einspur:
                    einspur = True
            if (
                event.key == pygame.K_r
            ):  # Klassisches XOR, falls 1, dann 0, falls 0 dann 1
                if showSpawn:
                    showSpawn = False
                elif not showSpawn:
                    showSpawn = True  #
            if event.key == pygame.K_ESCAPE:
                running = False
    moved = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        car.move_backward()
        moved = True
    if keys[pygame.K_UP]:
        car.move_forward()
        moved = True
    if keys[pygame.K_LEFT]:
        car.rotateTire(1, left=True)
    if keys[pygame.K_RIGHT]:
        car.rotateTire(1, right=True)
    if not moved and car.vel > 0:
        car.reduce_speed()
    if not moved and car.vel < 0:
        car.reduce_speed_backwards()
    if keys[pygame.K_w]:
        car.surfaceY -= 4
    if keys[pygame.K_s]:
        car.surfaceY += 4
    if keys[pygame.K_a]:
        car.surfaceX -= 4
    if keys[pygame.K_d]:
        car.surfaceX += 4
    if keys[pygame.K_p]:
        auto.checkParkingSpot(screen, carSurface_rotated_rect)
        timer = 0


def countTime():
    global timeCounter
    timeCounter += 1


def selectPolygon():
    selectedPolygon = screens.runIntro()
    return selectedPolygon


def createPolygon():
    # Erstellt ein Polygon-Objekt mit den gewählten Einstellungen
    polygon = Polygon(polygonScreen, width, height, selectedPolygon)
    # Zeichnet das ausgewählte Polygon auf die Oberfläche
    polygon.drawPolygon()
    # Fügt zufällig platzierte geparkte Autos zur Parkfläche hinzu
    polygon.park_cars(parkedSurface)
    return polygon


def initcar():
    # Erstellt ein neues Auto-Objekt mit Standardeigenschaften
    car = Car(0, 0, "blue", "darkgrey")
    # Berechnet die Mittelposition des Autos auf der Surface
    car.center = (
        carSurface.get_rect().center[0] - car.car_length / 2,
        carSurface.get_rect().center[1] - car.car_width / 2,
    )
    # Setzt die Ausgangsposition des Autos
    car.x = car.center[0]
    car.y = car.center[1]
    # Platziert das Auto zufällig im definierten Spawn-Bereich
    car.surfaceX = random.randint(
        spawnArea_instance.x1, spawnArea_instance.x2
    )  # Definieren des genauen Startpunktes (Zufällig im Spawn
    car.surfaceY = random.randint(
        spawnArea_instance.y1, spawnArea_instance.y2
    )  # Bereich -> Offset dient zur verkleinerung der Spawns,
    # Bei Polygon-Typ 1 (Reverse Parking) das Auto um 90 Grad drehen
    if selectedPolygon == 1:
        car.gierwinkel += 90
    return car


def gameOver():
    # Game-Over-Zustand mit Wartebildschirm
    waiting = True
    while waiting:
        # Schwarzer Hintergrund für Game-Over-Anzeige
        screen.fill("black")
        # Game-Over-Bild anzeigen
        screen.blit(GAME_OVER, GAME_OVER_POSITION)
        # Bildschirm aktualisieren
        pygame.display.flip()
        # Auf Benutzeraktionen warten (Beenden oder Neustart)
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
car = initcar()
pygame.draw.ellipse(carSurface, cameraColor, ellipse)  # Zeichnen der Kamera

text = "Parklücke besetzt"

# Change this line to pass the screen instead of carSurface
auto = automation(car, polygon, polygonScreen, carSurface)

while running:
    screen.fill((0, 0, 0, 0))
    # Schaue ob es eine kollision gab und falls ja Stop das Spiel
    col = auto.detectCollision(parkedSurface, carSurface_rotated_rect)
    if col is not None:
        running = False
    getKeyInput()  # Schau ob es ein Key Input gab und reagiere
    spawnArea_instance.showSpawn(showSpawn)

    # Zeichnen das spielers und der camera
    car.draw_parked_car(carSurface, einspur)
    if einspur:
        frontTire_rotated = pygame.transform.rotate(car.frontTire, car.angle)
        frontTire_rotated_rect = frontTire_rotated.get_rect(center=car.frontTireCenter)

        carSurface.blit(frontTire_rotated, frontTire_rotated_rect)

    # Auto rotieren
    carSurface_rotated = pygame.transform.rotate(
        carSurface, car.gierwinkel
    )  # Rotieren das Surface, falls nötig (Lenkung)
    carSurface_rotated_rect = carSurface_rotated.get_rect(
        center=(car.surfaceX, car.surfaceY)
    )  # Zentrum das Autos
    auto.carSurface = carSurface_rotated
    # Alles auf den Mainn Screen zeichnen
    polygonScreen.blit(parkedSurface, (0, 0))
    screen.blit(polygonScreen, (0, 0))
    if auto.parkingSpaceRect:
        car.body.center = (car.surfaceX, car.surfaceY)
        if auto.parkingSpaceRect.contains(car.body):
            auto.color = "green"
        else:
            auto.color = "red"
        pygame.draw.rect(screen, auto.color, auto.parkingSpaceRect)
    if auto.showMsg and timer < 300:
        timer += 1
        rendered_text = font.render(text, True, (0, 0, 0))
        screen.blit(rendered_text, (50, 20))
    else:
        auto.showMsg = False
    screen.blit(carSurface_rotated, carSurface_rotated_rect)  # Anzeigen der Surface mit der mitte vom Auto, um die rotation mittig zu halten
    auto.update(screen)
    pygame.display.flip()
gameOver()  # Zeige Game Over an

pygame.quit()
# probe
