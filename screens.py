import pygame

class Screens:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.running = True
        self.selected_level = None
        self.msgQueue = []

    def runIntro(self):
        text = "Select Level: Press 1 for Reverse Parking or 2 for Side Parking"
        rendered_text = self.font.render(text, True, (255, 255, 255))
        while self.running:
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None  # Exit the screens loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selected_level = 1
                        self.running = False
                    elif event.key == pygame.K_2:
                        self.selected_level = 2
                        self.running = False

            # Draw the screens screen
            self.screen.fill((30, 30, 30))
            self.screen.blit(rendered_text, (50, 100))
            pygame.display.flip()

        return self.selected_level
    