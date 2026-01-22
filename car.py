import math
import pygame
from sensors import Sensors, get_line_intersection

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
        # Calculate the 4 corners of the rotated, centered car
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        hw = self.width / 2
        hh = self.height / 2
        
        # Local corners in order: FL, FR, BR, BL
        local_corners = [
            (hw, -hh),  # FL
            (hw, hh),   # FR
            (-hw, hh),  # BR
            (-hw, -hh)  # BL
        ]
        
        # Transform to world
        world_corners = []
        for lx, ly in local_corners:
            wx = self.x + (lx * cos_a - ly * sin_a)
            wy = self.y + (lx * sin_a + ly * cos_a)
            world_corners.append((wx, wy))
            
        self.corners = world_corners 
        
        # Check collision with walls (Line Intersection)
        car_lines = [
            (world_corners[0], world_corners[1]), # Front
            (world_corners[1], world_corners[2]), # Right
            (world_corners[2], world_corners[3]), # Back
            (world_corners[3], world_corners[0])  # Left
        ]
        
        for wall in walls:
            # Optimization: fast AABB check first
            if not wall.colliderect(pygame.Rect(self.x-20, self.y-20, 40, 40)): 
                continue
                
            wall_lines = [
                ((wall.left, wall.top), (wall.right, wall.top)),
                ((wall.right, wall.top), (wall.right, wall.bottom)),
                ((wall.right, wall.bottom), (wall.left, wall.bottom)),
                ((wall.left, wall.bottom), (wall.left, wall.top))
            ]
            
            for p1, p2 in car_lines:
                for p3, p4 in wall_lines:
                    if get_line_intersection(p1, p2, p3, p4):
                        self.alive = False
                        self.distance -= 50
                        break
                if not self.alive:
                    break
            if not self.alive:
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
