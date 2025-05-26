import pygame


# Klasse zur Verwaltung verschiedener Bildschirme und Textanzeigen im Spiel
class Screens:
    def __init__(self, screen, font):
        # Hauptbildschirm auf dem gezeichnet wird
        self.screen = screen
        # Schriftart für Textanzeigen
        self.font = font
        # Flag zur Steuerung der Hauptschleife
        self.running = True
        # Speichert die vom Benutzer ausgewählte Spielvariante
        self.selected_level = None
        # Queue für Nachrichten (aktuell nicht verwendet, für zukünftige Erweiterungen)
        self.msgQueue = []

    # Zeigt den Intro-Bildschirm mit Levelauswahl und Steuerungsanweisungen
    def runIntro(self):
        # Liste mit allen Textzeilen, die angezeigt werden sollen
        text_lines = [
            "Select Level: Press 1 for Reverse Parking or 2 for Side Parking",
            " ",
            "Commands:",
            '    p: Checks if a parking space is in the "Bekanntschaftsbereich" and if',
            "        found, calculates the Path",
            "    e: Shows Einspurmodell (Bycicle Model aus Fahrzeugdynamik)",
            "    r: Shows the Spawn area of the Map",
            "    esc: Force Game Over, confirm with Space",
            '    Arrows (up, down, left, right): Realistic movement, recomended with "e"',
            "    WASD: Quick and Easy movement (not part of the finished model)",
        ]

        # Hauptschleife für den Intro-Bildschirm
        while self.running:
            # Verarbeitung von Ereignissen (Benutzerinteraktionen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Spiel beenden, wenn das Fenster geschlossen wird
                    self.running = False
                    return None  # Exit the screens loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        # Level 1 ausgewählt (Rückwärtsparken)
                        self.selected_level = 1
                        self.running = False
                    elif event.key == pygame.K_2:
                        # Level 2 ausgewählt (Seitenparken)
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


# probe2
