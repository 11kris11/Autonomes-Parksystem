import pygame
import math
from screens import Screens
from pathfinding.core.grid import Grid

class automation:
    def __init__(self, car, polygon, screen, carSurface):
        self.car = car 
        self.polygon = polygon
        self.screen = screen
        self.carSurface = carSurface
        self.screenMask = self.createMask(screen, color=(255, 255, 255, 255), treshold=(10,10,10,10))
        self.grid_resolution = 5
        self.matrix = []

    def initGrid(self):
        rect = self.screen.get_rect()
        for y in range(0, rect.height, self.grid_resolution):
            row = []
            for x in range(0, rect.width, self.grid_resolution):
                color = self.screen.get_at((x,y))[:3]
                if color != (190,190,190) or color != (255,255,255):
                    walkable = 1
                else: 
                    walkable = 0
                row.append(walkable)
            self.matrix.append(row)
        if self.matrix:
            self.grid = Grid(matrix=self.matrix)
    
    
    def createMask(self, surface, color=None, treshold=127):
        if color == None:
            mask = pygame.mask.from_surface(surface, treshold)
        else:
            mask = pygame.mask.from_threshold(surface, color, treshold)
        return mask
    
    def detectCollision(self, screen, carRect):
        if screen == None or self.carSurface == None or carRect == None:
            return None
        mask1 = self.createMask(screen)
        mask2 = self.createMask(self.carSurface)
        
        offset = (carRect.x, carRect.y)

        collision = mask1.overlap(mask2, offset)

        return collision
    
    def searchParkingSpot(self):
        s = 0


    def checkParkingSpot(self, screen, rect, font):
        x = 0
        y = 0
        center = rect.center
        offset = (rect.left, rect.top)
        points = []
        carMask = self.createMask(self.carSurface, treshold=0)
        overlapMask = self.screenMask.overlap_mask(carMask, offset)
        #print(self.carMask.count(), " car")
        #print(self.screenMask.count())

        if overlapMask.count() > 0: # Only draw if there is an overlap
# --- Visualize the overlapMask ---          Aufgrund Performanz ausgenommen
            try:
             #   # Create a surface from the overlap mask
              #  # Set bits (overlap area) will be green, unset bits transparent
                overlap_viz_surface = overlapMask.to_surface(setcolor=(0, 255, 0, 180), # Semi-transparent green
                                                             unsetcolor=(0, 0, 0, 0)) 
                
                # Draw the visualization onto surface1 (the screen) at origin (0,0)
                # The overlapMask coordinates are relative to surface1's origin
                screen.blit(overlap_viz_surface, (0, 0)) 
            except Exception as e:
                print(f"Error visualizing overlapMask: {e}")
# --- End visualization ---
            maskComponents = overlapMask.connected_components()
            maskOutlines = []
            for mask in maskComponents:
                maskOutlines.append(mask.outline())
            points = []
            for i in range(0, len(maskOutlines)):
                tempMask = maskOutlines[i]
                temp = []
                for pixel in tempMask:
                    distance = math.dist(center, pixel)
                    temp.append((distance, pixel))
                
                temp.sort(key=lambda element: element[0])
                points.append(temp[0])
            if points:
                points.sort(key=lambda element:element[0])
            twoClosest = []
            for i in range(0,len(points)):
                twoClosest.append(points[i][1])
            twoClosest = twoClosest[:2]
            if len(twoClosest) == 1:
                pygame.draw.circle(screen, "black", twoClosest[0], 5)
            elif len(twoClosest) == 2:
                pygame.draw.circle(screen, "black", twoClosest[0], 5)
                pygame.draw.circle(screen, "black", twoClosest[1], 5)

            if len(twoClosest) == 2:
                distance = math.dist(twoClosest[0], twoClosest[1])
                if twoClosest[0][0] == twoClosest[1][0]:
                    if self.car.surfaceX > twoClosest[0][0]:
                        x = twoClosest[0][0] - self.polygon.parkingSpaceWidth / 2
                        y = min(twoClosest[0][1], twoClosest[1][1]) + distance / 2
                    elif self.car.surfaceX < twoClosest[0][0]:
                        x = twoClosest[0][0] + self.polygon.parkingSpaceWidth / 2
                        y = min(twoClosest[0][1], twoClosest[1][1]) + distance / 2
                elif twoClosest[0][1] == twoClosest[1][1]:
                    if self.car.surfaceY > twoClosest[0][1]:
                        x = min(twoClosest[0][0], twoClosest[1][0]) + distance / 2
                        y = twoClosest[0][1] - self.polygon.parkingSpaceWidth / 2
                    elif self.car.surfaceY < twoClosest[0][1]:
                        x = min(twoClosest[0][0], twoClosest[1][0]) + distance / 2
                        y = twoClosest[0][1] + self.polygon.parkingSpaceWidth / 2

            
            if x != 0 and y != 0 and y != 449.5:
                self.x = x
                self.y = y
                self.park(self.checkParkingSpace(x,y), font)


    def checkParkingSpace(self, x,y):
            pixel_color = self.screen.get_at((int(x), int(y)))
            if pixel_color == (190,190,190,255):
                return (x,y)
            else:
                return None


    def park(self, spaceCenter, font):
        screens = Screens(self.screen, font)
        if spaceCenter:
            self.text = False
            screens.showMsg(self.text)
        else: 
            self.text = True
            screens.showMsg(self.text)



    def backwardsParking(self):
        print("backwards")
    
    
    def sideParking(self):
        print("side")

