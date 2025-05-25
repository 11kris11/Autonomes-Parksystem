import pygame  # Hauptbibliothek für die Spieleentwicklung
import math    # Wird für trigonometrische Funktionen in der Bewegungsberechnung benötigt

# Diese Klasse erstellt ein generisches Auto mit anpassbarer Farbe und Position
# und implementiert die Einspurmodell-Physik für realistische Fahrbewegungen
class Car:
    # Standardabmessungen für das Auto (in Pixeln)
    car_length = 225      # Gesamtlänge des Autos
    car_width = 125       # Breite des Autos
    car_roof_length = 125 # Länge des Autodachs
    car_roof_width = 100  # Breite des Autodachs
    car = None            # Referenz auf das gesamte Auto-Rechteck (wird später initialisiert)
    angle = 0             # Aktueller Lenkwinkel der Vorderräder
    maxAngle = 45         # Maximaler Lenkeinschlag in Grad

    def __init__(self, x, y, direction, screen, color, color2):
        # Positionsparameter
        self.x = x            # X-Koordinate des Autos auf der Surface
        self.y = y            # Y-Koordinate des Autos auf der Surface
        self.color = color    # Hauptfarbe des Autos (für den Körper)
        self.color2 = color2  # Sekundärfarbe (für das Dach)
        self.screen = screen  # Surface, auf der das Auto gezeichnet wird
        self.center = (x,y)   # Zentrum des Autos (wird für Rotationen verwendet)
        
        # Bewegungsparameter
        self.acceleration = 0.5  # Beschleunigungsrate des Autos
        self.vel = 0            # Aktuelle Geschwindigkeit (positiv=vorwärts, negativ=rückwärts)
        self.max_vel = 15       # Maximale Geschwindigkeit in beide Richtungen
        self.surfaceX = 0       # X-Position des Autos auf dem Hauptbildschirm
        self.surfaceY = 0       # Y-Position des Autos auf dem Hauptbildschirm
        self.gierwinkel = 0     # Ausrichtung des Autos in Grad (0=rechts, 90=oben)
        self.axleLen = (135)    # Achsabstand für das Einspurmodell (beeinflusst den Wendekreis)
    
    # Zeichnet das Auto mit allen Komponenten (Körper, Dach, Lichter, optional Reifen)
    # Parameter:
    #   screen: Surface, auf der gezeichnet wird
    #   einspur: Wenn True, wird das Auto mit dem Einspurmodell (sichtbare Reifen) gezeichnet
    def draw_parked_car(self, screen, einspur=False): 
        light1 = None  # Referenz für das erste Rücklicht
        light2 = None  # Referenz für das zweite Rücklicht

        # Körper & Dach
        body = pygame.Rect(self.x, self.y, self.car_length, self.car_width)
        roof = pygame.Rect(self.x + 50, self.y + 12.5, self.car_roof_length, self.car_roof_width)
        pygame.draw.rect(screen, self.color, body, border_radius=15)
        pygame.draw.rect(screen, self.color2, roof, border_radius=10)
                
            # Lichter
        light1 = pygame.Rect(self.x + self.car_length - 20, self.y + self.car_width - 20, 20, 20)
        light2 = pygame.Rect(self.x + self.car_length - 20, self.y, 20, 20)
        pygame.draw.rect(screen, "yellow", light1, border_bottom_right_radius=15)
        pygame.draw.rect(screen, "yellow", light2, border_top_right_radius=15)
            
        self.car = body.unionall((roof, light1, light2))

        if einspur:
            temp = pygame.image.load(r"src\tire.png")
            width = temp.get_width() / 4
            height = temp.get_height() / 4
            tire = pygame.transform.scale(temp, (width, height))

            self.frontTire = pygame.Surface((tire.get_size()), pygame.SRCALPHA)
            self.rearTire = pygame.Surface((tire.get_size()), pygame.SRCALPHA)

            self.frontTireCenter = (self.x + self.car_length * 4/5, self.y + self.car_width / 2)
            self.rearTireCenter = (self.x + self.car_length * 1/5, self.y + self.car_width / 2)

            pygame.draw.rect(screen, "black", (self.rearTireCenter[0], self.rearTireCenter[1] - 5, self.frontTireCenter[0] - self.rearTireCenter[0], 10))
            self.frontTire.blit(tire, (0,0))
            self.rearTire.blit(tire, (0,0))
            screen.blit(self.rearTire, (self.rearTireCenter[0] - self.frontTire.get_width() / 2, self.rearTireCenter[1] - self.frontTire.get_height() / 2))

        self.body = body


    def getCarRect(self):
        return self.car
    
    def rotateTire(self, rotationVel, left=False, right=False):
        if left:
            self.angle = min(self.angle + rotationVel, self.maxAngle)
        if right:
            self.angle = max(self.angle - rotationVel, -self.maxAngle)

    def move_forward(self):                             # Wenn (self.vel + self.acceleration) größer als 
        self.vel = min(self.vel + self.acceleration, self.max_vel) # max_vel, dann max_vel sonst nicht
        self.move()
    
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel)
        self.move(backwards=True)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def reduce_speed_backwards(self):
        self.vel = min(self.vel + self.acceleration / 2, 0)
        self.move()
    
    
    def move(self, backwards=False):
        nextAngle = self.nextAngle()
        self.gierwinkel += nextAngle * 0.2
        self.gierwinkel %= 360

        pos = self.nextPos(backwards)

        self.surfaceX += (pos[0] * 0.2)
        self.surfaceY -= (pos[1] * 0.2)

    def schraeglaufwinkel(self):
        lenkwinkel = math.radians(self.angle)

        p1 = (self.axleLen/2)/self.axleLen
        p2 = math.tan(lenkwinkel)

        return math.atan(p1 * p2)
    
    def nextPos(self, backwards=False):
        winkel = math.radians(self.gierwinkel) + self.schraeglaufwinkel()
        
        if not backwards:
            x = self.vel * math.cos(winkel)
            y = self.vel * math.sin(winkel)
        else:
            x = self.vel * 2/3 * math.cos(winkel)
            y = self.vel * 2/3 * math.sin(winkel)

        return (x,y)
    
    def nextAngle(self):
        p1 = self.vel / self.axleLen
        p2 = math.sin(self.schraeglaufwinkel())

        return math.degrees(p1*p2)
# probe