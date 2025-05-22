import pygame
import math
from screens import Screens
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class automation:
    def __init__(self, car, polygon, screen, carSurface):
        self.car = car 
        self.polygon = polygon
        self.screen = screen
        self.carSurface = carSurface
        self.screenMask = self.createMask(screen, color=(255, 255, 255, 255), treshold=(10,10,10,10))
        self.grid_resolution = 5
        self.matrix = []
        self.showMsg = False
        self.color = "red"
        self.x = 0 
        self.y = 0
        self.parkingSpaceRect = None
        self.path = []
        self.initGrid()

    def initGrid(self):
        rect = self.screen.get_rect()
        self.matrix = []  # Clear any existing matrix
        for y in range(0, rect.height, self.grid_resolution):
            row = []
            for x in range(0, rect.width, self.grid_resolution):
                try:
                    color = self.screen.get_at((x, y))[:3]
                    # Mark as walkable (1) if it's a drivable area (grey)
                    if color == (190, 190, 190):
                        walkable = 1
                    else:
                        walkable = 0
                except IndexError:
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

    def findPath(self, start_pos, end_pos):
        # Convert pixel coordinates to grid coordinates
        start_x, start_y = int(start_pos[0] / self.grid_resolution), int(start_pos[1] / self.grid_resolution)
        end_x, end_y = int(end_pos[0] / self.grid_resolution), int(end_pos[1] / self.grid_resolution)
        
        # Check boundaries
        if not self.matrix:
            return []
        if start_x < 0 or start_x >= len(self.matrix[0]) or start_y < 0 or start_y >= len(self.matrix):
            return []
        if end_x < 0 or end_x >= len(self.matrix[0]) or end_y < 0 or end_y >= len(self.matrix):
            return []
        
        # Create start and end nodes
        start = self.grid.node(start_x, start_y)
        end = self.grid.node(end_x, end_y)
        
        # Create A* finder and find path
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, self.grid)
        
        # Reset grid for future path searches
        self.grid.cleanup()
        
        # Convert grid coordinates back to pixel coordinates
        pixel_path = []
        for node in path:
            # Check the type of node and handle accordingly
            if hasattr(node, 'x') and hasattr(node, 'y'):
                # It's a GridNode object
                x = node.x * self.grid_resolution + self.grid_resolution // 2
                y = node.y * self.grid_resolution + self.grid_resolution // 2
            else:
                # It's a tuple or list
                x = node[0] * self.grid_resolution + self.grid_resolution // 2
                y = node[1] * self.grid_resolution + self.grid_resolution // 2
            pixel_path.append((x, y))
        
        return pixel_path
    
    def drawPath(self, screen, path, color=(0, 0, 255), radius=3):
        for point in path:
            pygame.draw.circle(screen, color, point, radius)
    
    def checkParkingSpot(self, screen, rect):
        x = 0
        y = 0
        center = rect.center
        offset = (rect.left, rect.top)
        points = []
        carMask = self.createMask(self.carSurface, treshold=0)
        overlapMask = self.screenMask.overlap_mask(carMask, offset)

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
            self.twoClosest = []
            for i in range(0,len(points)):
                self.twoClosest.append(points[i][1])
            self.twoClosest = self.twoClosest[:2]
            if len(self.twoClosest) == 1:
                pygame.draw.circle(screen, "black", self.twoClosest[0], 5)
            #elif len(twoClosest) == 2:

            if len(self.twoClosest) == 2:
                self.lineDistance = math.dist(self.twoClosest[0], self.twoClosest[1])
                if self.twoClosest[0][0] == self.twoClosest[1][0]:
                    if self.car.surfaceX > self.twoClosest[0][0]:
                        x = self.twoClosest[0][0] - self.polygon.parkingSpaceWidth / 2
                        y = min(self.twoClosest[0][1], self.twoClosest[1][1]) + self.lineDistance / 2
                    elif self.car.surfaceX < self.twoClosest[0][0]:
                        x = self.twoClosest[0][0] + self.polygon.parkingSpaceWidth / 2
                        y = min(self.twoClosest[0][1], self.twoClosest[1][1]) + self.lineDistance / 2
                elif self.twoClosest[0][1] == self.twoClosest[1][1]:
                    if self.car.surfaceY > self.twoClosest[0][1]:
                        x = min(self.twoClosest[0][0], self.twoClosest[1][0]) + self.lineDistance / 2
                        y = self.twoClosest[0][1] - self.polygon.parkingSpaceLength / 2
                    elif self.car.surfaceY < self.twoClosest[0][1]:
                        x = min(self.twoClosest[0][0], self.twoClosest[1][0]) + self.lineDistance / 2
                        y = self.twoClosest[0][1] + self.polygon.parkingSpaceLength / 2
            if x != 0 and y != 0 and y != 449.5:
                self.x = x
                self.y = y
                self.park(self.checkParkingSpace(x,y))

    def checkParkingSpace(self, x,y):
            pixel_color = self.screen.get_at((int(x), int(y)))
            if pixel_color == (190,190,190,255):
                return (x,y)
            else:
                return None
            
    def park(self, spaceCenter):
        if spaceCenter:
            self.showMsg = False
            if self.parkingSpaceRect:
                self.parkingSpaceRect.center = (self.x,self.y)
            else:
                self.parkingSpaceRect = pygame.Rect(self.x, self.y, self.polygon.parkingSpaceWidth, self.polygon.parkingSpaceLength)
                self.parkingSpaceRect.center = spaceCenter
            
            # Find path from car to parking spot
            car_pos = (self.car.surfaceX, self.car.surfaceY)
            self.path = self.findPath(car_pos, spaceCenter)
        else: 
            self.showMsg = True
            self.path = []
    
    def update(self, screen):
        # Draw the path if it exists
        if self.path:
            self.drawPath(screen, self.path)




