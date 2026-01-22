import pygame

class Track:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.walls = []
        self.start_pos = (100, 300)
        self.start_angle = 0
        
        # Create a hollow rectangle track
        # Outer walls
        self.walls.append(pygame.Rect(0, 0, width, 50)) # Top
        self.walls.append(pygame.Rect(0, height-50, width, 50)) # Bottom
        self.walls.append(pygame.Rect(0, 0, 50, height)) # Left
        self.walls.append(pygame.Rect(width-50, 0, 50, height)) # Right
        
        # Inner block (island) to create a loop
        self.walls.append(pygame.Rect(150, 150, width-300, height-300))

    def draw(self, screen):
        screen.fill((50, 50, 50)) # Grey road
        for wall in self.walls:
            pygame.draw.rect(screen, (200, 200, 200), wall) # White walls
            
    def check_collision(self, car_rect):
        """Simple AABB collision check."""
        for wall in self.walls:
            if car_rect.colliderect(wall):
                return True
        return False
