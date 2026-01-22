import math
import pygame
from sensors import Sensors

class Car:
    def __init__(self, start_pos, start_angle):
        self.x, self.y = start_pos
        self.angle = start_angle # Degrees
        self.speed = 0
        self.width = 20
        self.height = 10
        self.sensors = Sensors()
        self.alive = True
        self.distance = 0 # Fitness metric
        
        # Physics constants
        self.max_speed = 10
        self.friction = 0.1
        self.acceleration = 1.0
        self.rotation_speed = 5

    def update(self, steering, throttle, walls):
        if not self.alive:
            return

        # 1. Apply controls
        # Steering: -1 (left) to 1 (right)
        self.angle += steering * self.rotation_speed
        
        # Throttle: 0 to 1
        if throttle > 0:
            self.speed += throttle * self.acceleration
        
        # 2. Apply physics
        self.speed = max(0, self.speed - self.friction) # Friction
        self.speed = min(self.speed, self.max_speed)
        
        # Move
        rad = math.radians(self.angle)
        dx = math.cos(rad) * self.speed
        dy = math.sin(rad) * self.speed
        
        self.x += dx
        self.y += dy
        self.distance += self.speed # Simple fitness accumulation
        
        # 3. Collision check
        # Create a rotated rect for collision (simplified to bounding box for now, or just center point check)
        # Detailed rect collision is better.
        car_rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        # Note: Pygame rects don't rotate. For strict collision we need masks or polygon checks.
        # But prompt said "Simple wall collision (bounding box)".
        # So we use axis-aligned bounding box (AABB) centered at x,y.
        
        for wall in walls:
            if car_rect.colliderect(wall):
                self.alive = False
                self.distance -= 50 # Penalty
                break
                
    def get_data(self, walls):
        return self.sensors.get_readings((self.x, self.y), self.angle, walls)
        
    def draw(self, screen):
        # Draw a simple rotated rectangle
        # Create a surface for the car
        car_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        car_surf.fill((0, 255, 0)) # Green car
        
        # Rotate it
        rotated_surf = pygame.transform.rotate(car_surf, -self.angle)
        rect = rotated_surf.get_rect(center=(self.x, self.y))
        screen.blit(rotated_surf, rect)
