import pygame
import math

# Diese Klasse soll ein generisches Auto auf eine bestimmte Fäche bauen können, in verschiedenen farben
class Car:
    # Masen 
    car_length = 225
    car_width = 125
    car_roof_length = 125
    car_roof_width = 100
    car = None
    angle = 0
    rotation_vel = 1

    def __init__(self, x, y, direction, screen, color, color2):
        self.x = x
        self.y = y
        self.color = color
        self.color2 = color2
        self.direction = direction
        self.screen = screen
        self.center = (x,y)
        self.acceleration = 0.1
        self.vel = 0
        self.max_vel = 2
        self.surfaceX = 0
        self.surfaceY = 0
    
    # Das auto besteht aus zwei Vierecken, die das Dach und den Körper darstellen sollen. Die Lichter sind für die Richtungsorientierung 
    def draw_parked_car(self, screen): 
        light1 = None
        light2 = None
        
        if self.direction == "up" or self.direction == "down":
            body = pygame.Rect(self.x, self.y, self.car_width, self.car_length)
            roof = pygame.Rect(self.x + 12.50, self.y + 50, self.car_roof_width, self.car_roof_length)
            pygame.draw.rect(screen, self.color, body, border_radius=15)
            pygame.draw.rect(screen, self.color2, roof, border_radius=10)
            
            if self.direction == "up":
                light1 = pygame.Rect(self.x, self.y, 20, 20)
                light2 = pygame.Rect(self.x + self.car_width - 20, self.y, 20, 20)
                pygame.draw.rect(screen, "yellow", light1, border_top_left_radius=15)
                pygame.draw.rect(screen, "yellow", light2, border_top_right_radius=15)
            
            elif self.direction == "down":
                light1 = pygame.Rect(self.x, self.y + self.car_length - 20, 20, 20)
                light2 = pygame.Rect(self.x + self.car_width - 20, self.y + self.car_length - 20, 20, 20)
                pygame.draw.rect(screen, "yellow", light1, border_bottom_left_radius=15)
                pygame.draw.rect(screen, "yellow", light2, border_bottom_right_radius=15)


        if self.direction == "right" or self.direction == "left":
        # Körper & Dach
            body = pygame.Rect(self.x, self.y, self.car_length, self.car_width)
            roof = pygame.Rect(self.x + 50, self.y + 12.5, self.car_roof_length, self.car_roof_width)
            pygame.draw.rect(screen, self.color, body, border_radius=15)
            pygame.draw.rect(screen, self.color2, roof, border_radius=10)
                
            # Lichter
            if self.direction == "right":
                light1 = pygame.Rect(self.x + self.car_length - 20, self.y + self.car_width - 20, 20, 20)
                light2 = pygame.Rect(self.x + self.car_length - 20, self.y, 20, 20)
                pygame.draw.rect(screen, "yellow", light1, border_bottom_right_radius=15)
                pygame.draw.rect(screen, "yellow", light2, border_top_right_radius=15)
            
            elif self.direction == "left":
                light1 = pygame.Rect(self.x, self.y, 20, 20)
                light2 = pygame.Rect(self.x, self.y + self.car_width - 20, 20, 20)
                pygame.draw.rect(screen, "yellow", light1, border_top_left_radius=15)
                pygame.draw.rect(screen, "yellow", light2, border_bottom_left_radius=15)
        self.car = body.unionall((roof, light1, light2))

    def getCarRect(self):
        return self.car
    
    def rotate(self, rotationVel, left=False, right=False, backwards=False):
        if backwards:
            if left:
                self.angle -= rotationVel
            if right:
                self.angle += rotationVel
        if not backwards:
            if left:
                self.angle += rotationVel
            if right:
                self.angle -= rotationVel

    def move_forward(self):                             # Wenn (self.vel + self.acceleration) größer als 
        self.vel = min(self.vel + self.acceleration, self.max_vel) # max_vel, dann max_vel sonst nicht
        self.move()
    
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def reduce_speed_backwards(self):
        self.vel = min(self.vel + self.acceleration / 2, 0)
        self.move()
    
    
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.surfaceY -= vertical
        self.surfaceX -= horizontal

    
    def updatePos(self):
        self.surfaceX = self.x
        self.surfaceY = self.y 
        self.x = self.center[0]
        self.y = self.center[1]

    