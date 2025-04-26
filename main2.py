import pygame
import sys
from car import Car

height = 900
width = 1600

def main():
    # Pygame initialization
    pygame.init()

    # Screen setup
    screen_width, screen_height = 1600, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Pygame Window")

    # Clock for framerate
    clock = pygame.time.Clock()
    # Creating payer
    av = pygame.Rect(100,100,225,125)
    
    # parkinng spaces definitions
    horiz1 = pygame.Rect(width/10, height/10, width/10*8, 10)
    horiz2 = pygame.Rect(width/10, height/10*9-10, width/10*8, 10)
    # Define vertical lines rectangles outside the loop as well
    vert_lines1 = []
    vert_lines2 = []
    for i in range(5):
        vert1 = pygame.Rect(width/10 + width/10*8*i/4, height/10, 10, 160)
        vert2 = pygame.Rect(width/10 + width/10*8*i/4, height/10*8-70, 10, 160)
        vert_lines1.append(vert1)
        vert_lines2.append(vert2)

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic here (update things)

        # Drawing
        screen.fill("darkslategray")  # Background color

        # Draw parking spaces
        pygame.draw.rect(screen, "white", horiz1)
        pygame.draw.rect(screen, "white", horiz2)
        for i in range(5):
            pygame.draw.rect(screen, "white", vert_lines1[i])
            pygame.draw.rect(screen, "white", vert_lines2[i])

        pygame.draw.rect(screen, "black", av)
        # Show everything
        pygame.display.flip()

        # Limit FPS
        clock.tick(60)

    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()