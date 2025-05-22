import pygame

class Screens:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.running = True
        self.selected_level = None
        self.msgQueue = []

    def runIntro(self):
        text_lines = [
            "Select Level: Press 1 for Reverse Parking or 2 for Side Parking",
            " ",
            "Commands:",
            "    p: Checks if a parking space is in the \"Bekanntschaftsbereich\" and if",
            "        found, calculates the Path",
            "    e: Shows Einspurmodell (Bycicle Model aus Fahrzeugdynamik)",
            "    r: Shows the Spawn area of the Map",
            "    esc: Force Game Over, confirm with Space",
            "    Arrows (up, down, left, right): Realistic movement, recomended with \"e\"",
            "    WASD: Quick and Easy movement (not part of the finished model)"
        ]
        
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
            
            # Render and display each line separately
            y_offset = 100
            line_spacing = 70
            for line in text_lines:
                rendered_text = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(rendered_text, (50, y_offset))
                y_offset += line_spacing
                
            pygame.display.flip()

        return self.selected_level
