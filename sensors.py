import math

def get_line_intersection(p1, p2, p3, p4):
    """
    Find intersection between line segment p1-p2 (ray) and p3-p4 (wall).
    p1, p2, p3, p4 are (x, y) tuples.
    Returns (x, y) if intersection exists and is within segments, else None.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:
        return None  # Parallel

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    if 0 <= ua <= 1 and 0 <= ub <= 1:
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return (x, y)
    return None

class Sensors:
    def __init__(self, ray_length=150):
        self.ray_length = ray_length
        # Angles relative to car heading: Left, Center, Right
        self.angles = [-45, 0, 45]

    def get_readings(self, car_pos, car_angle, walls):
        """
        Cast rays and return normalized distances [0, 1].
        1.0 means no wall in range.
        0.0 means touching wall.
        """
        readings = []
        center_x, center_y = car_pos
        
        for angle in self.angles:
            # Calculate ray end point
            rad = math.radians(car_angle + angle)
            end_x = center_x + math.cos(rad) * self.ray_length
            end_y = center_y + math.sin(rad) * self.ray_length
            
            # Check intersection with all walls
            closest_dist = self.ray_length
            
            for wall in walls:
                # Wall is a rect, check 4 sides
                lines = [
                    ((wall.left, wall.top), (wall.right, wall.top)),
                    ((wall.right, wall.top), (wall.right, wall.bottom)),
                    ((wall.right, wall.bottom), (wall.left, wall.bottom)),
                    ((wall.left, wall.bottom), (wall.left, wall.top))
                ]
                
                for p3, p4 in lines:
                    intersect = get_line_intersection(car_pos, (end_x, end_y), p3, p4)
                    if intersect:
                        dist = math.hypot(intersect[0] - center_x, intersect[1] - center_y)
                        if dist < closest_dist:
                            closest_dist = dist
                            
            # Normalize: 0 = collision (dist=0), 1 = max range (dist=ray_length)
            # Actually usually networks like larger values for closer objects or vice versa.
            # Prompt says: "Normalized distance to nearest wall in range [0, 1]"
            # Usually strict NEAT implies input is what it sees. 
            # If 1 is far and 0 is close? Or 1 is close and 0 is far?
            # Prompt: "distance to nearest wall" -> so 0 if close, 1 if far (clamped at ray_length)
            readings.append(closest_dist / self.ray_length)
            
        return readings

    def draw(self, screen, car_pos, car_angle):
        # Optional debug draw
        pass
