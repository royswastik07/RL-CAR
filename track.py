import pygame

class Track:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.walls = []
        self.start_pos = (100, 300)
        self.start_angle = 0
        self.buttons = [] # Store UI button rects
        
        # Pre-define layouts
        self.layouts = [self.track_1_rect, self.track_2_chicane, self.track_3_s_bend,
                        self.track_4_pillars, self.track_5_narrow, self.track_6_u_turn,
                        self.track_7_maze_lite, self.track_8_box, self.track_9_cross,
                        self.track_10_hard]
        
        # Initialize buttons for UI
        btn_w = 40
        btn_h = 30
        margin = 10
        for i in range(10):
            x = margin + i * (btn_w + margin)
            y = 10 
            rect = pygame.Rect(x, y, btn_w, btn_h)
            self.buttons.append((rect, f"{i+1}"))
            
        self.set_track(0)

    def set_track(self, index):
        if 0 <= index < len(self.layouts):
            self.walls = []
            # Always add outer boundary
            self.walls.append(pygame.Rect(0, 50, self.width, 50)) # Top (below buttons)
            self.walls.append(pygame.Rect(0, self.height-50, self.width, 50)) # Bottom
            self.walls.append(pygame.Rect(0, 50, 50, self.height-50)) # Left
            self.walls.append(pygame.Rect(self.width-50, 50, 50, self.height-50)) # Right
            
            # Call layout function
            self.layouts[index]()

    def draw(self, screen):
        screen.fill((50, 50, 50)) # Grey road
        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, (200, 200, 200), wall)
            
        # Draw UI
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, self.width, 50)) # Header bar
        for rect, label in self.buttons:
            pygame.draw.rect(screen, (100, 100, 200), rect)
            font = pygame.font.SysFont('Arial', 20)
            text = font.render(label, True, (255, 255, 255))
            screen.blit(text, (rect.x + 12, rect.y + 5))

    # --- Layouts ---
    def track_1_rect(self):
        # Basic loop
        self.walls.append(pygame.Rect(150, 150, self.width-300, self.height-300))
        self.start_pos = (100, 300)
        self.start_angle = 90
        
    def track_2_chicane(self):
        # The complex one we made
        self.walls.append(pygame.Rect(150, 150, 200, 300))
        self.walls.append(pygame.Rect(500, 0, 100, 400))
        self.walls.append(pygame.Rect(450, 500, 300, 50))
        self.walls.append(pygame.Rect(650, 200, 50, 50))
        self.start_pos = (100, 130) # Moved down
        self.start_angle = 90

    def track_3_s_bend(self):
        # Snake pattern
        self.walls.append(pygame.Rect(200, 50, 50, 400))
        self.walls.append(pygame.Rect(400, 150, 50, 400))
        self.walls.append(pygame.Rect(600, 50, 50, 400))
        self.start_pos = (100, 130) # Moved down
        self.start_angle = 90

    def track_4_pillars(self):
        # Open field with pillars
        for x in range(150, 700, 150):
            for y in range(150, 500, 150):
                self.walls.append(pygame.Rect(x, y, 60, 60))
        self.start_pos = (80, 130) # Moved down
        self.start_angle = 45

    def track_5_narrow(self):
        # Narrow corridor loop
        self.walls.append(pygame.Rect(100, 100, 600, 400)) # Big block
        self.walls.append(pygame.Rect(180, 180, 440, 240)) # Hollow center (removed by draw order? No, walls are added)
        # Actually we need to add walls to BLOCK, not carve.
        # So "Narrow" means big inner island
        self.walls = [] # Reset for this specific one to be cleaner
        # Re-add borders
        self.walls.append(pygame.Rect(0, 50, self.width, 50)) 
        self.walls.append(pygame.Rect(0, self.height-50, self.width, 50)) 
        self.walls.append(pygame.Rect(0, 50, 50, self.height-50)) 
        self.walls.append(pygame.Rect(self.width-50, 50, 50, self.height-50)) 
        
        self.walls.append(pygame.Rect(120, 120, 560, 360)) # Huge center
        self.start_pos = (85, 300)
        self.start_angle = 90

    def track_6_u_turn(self):
        # Needs to go up, turn around, come back
        self.walls.append(pygame.Rect(350, 150, 100, 350)) # Divider
        self.start_pos = (200, 500)
        self.start_angle = 270 # Up

    def track_7_maze_lite(self):
        self.walls.append(pygame.Rect(200, 50, 20, 300))
        self.walls.append(pygame.Rect(400, 250, 20, 300))
        self.walls.append(pygame.Rect(600, 50, 20, 300))
        self.walls.append(pygame.Rect(100, 350, 100, 20))
        self.walls.append(pygame.Rect(500, 150, 100, 20))
        self.start_pos = (100, 130) # Moved down
        self.start_angle = 90

    def track_8_box(self):
        # Just a box, easiest
        self.walls.append(pygame.Rect(300, 250, 200, 100))
        self.start_pos = (150, 300)
        self.start_angle = 0

    def track_9_cross(self):
        # A cross shape in middle
        self.walls.append(pygame.Rect(350, 150, 100, 300))
        self.walls.append(pygame.Rect(250, 250, 300, 100))
        self.start_pos = (100, 130) # Moved down
        self.start_angle = 45

    def track_10_hard(self):
        # Random scattering
        import random
        random.seed(42) # Fixed for consistency
        for _ in range(20):
            x = random.randint(100, 700)
            y = random.randint(150, 500) # Avoid top area
            self.walls.append(pygame.Rect(x, y, 40, 40))
        self.start_pos = (80, 130) # Safe start
        self.start_angle = 0
