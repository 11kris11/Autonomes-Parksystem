import pygame
class automation:
    def __init__(self, car):
        self.car = car 
    
    def createMask(self, surface):
        mask = pygame.mask.from_surface(surface)
        
        return mask
    def detectCollision(self, surface1, surface2, carRect):
        if surface1 == None or surface2 == None or carRect == None:
            return None
        mask1 = self.createMask(surface1)
        mask2 = self.createMask(surface2)
        
        offset = (carRect.x, carRect.y)

        collision = mask1.overlap(mask2, offset)

        return collision