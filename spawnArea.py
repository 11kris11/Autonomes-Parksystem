import pygame


# Diese Klasse definiert den Bereich, in dem das Auto zu Beginn erscheint
# und bietet Funktionen zum Anzeigen dieses Bereichs während des Spiels
class spawnArea:
    # Koordinaten für die Begrenzung des Spawn-Bereichs
    x1 = None  # Linke Grenze
    x2 = None  # Rechte Grenze
    y1 = None  # Obere Grenze
    y2 = None  # Untere Grenze
    screen = None  # Bildschirm, auf dem gezeichnet wird
    selectedPolygon = None  # Ausgewählter Parkplatztyp

    def __init__(self, screen, polNum):
        # Speichern des Hauptbildschirms und des Polygon-Typs
        self.screen = screen
        self.selectedPolygon = polNum
        # Transparente Oberfläche für die Darstellung des Spawn-Bereichs
        self.selfScreen = pygame.Surface((1600, 900), pygame.SRCALPHA)

        # Festlegen der Spawn-Bereichsgrenzen je nach Polygon-Typ
        if polNum == 1:
            # Vertikaler Korridor für Rückwärtsparken (Polygon 1)
            self.x1 = 600
            self.x2 = 1000
            self.y1 = 0
            self.y2 = 900
        elif polNum == 2:
            # Horizontaler Korridor für seitliches Parken (Polygon 2)
            self.x1 = 0
            self.x2 = 1600
            self.y1 = 300
            self.y2 = 600

    def showSpawn(self, hmm):
        # Überprüfen der Pixelfarbe an der Spawn-Bereichsecke
        pixel_color = self.screen.get_at((self.x1 + 1, self.y1 + 1))

        # Wenn hmm=True, zeige den Spawn-Bereich in Rot an
        if hmm:
            pygame.draw.rect(
                self.selfScreen,
                "red",
                (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1),
            )
            self.screen.blit(self.selfScreen, (0, 0))
        # Andernfalls, wenn hmm=False und die Farbe nicht grau ist, zeige den Bereich in Grau an
        elif not hmm and pixel_color != (190, 190, 190, 255):
            pygame.draw.rect(
                self.selfScreen,
                "grey",
                (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1),
            )
            self.screen.blit(self.selfScreen, (0, 0))
            # probe
