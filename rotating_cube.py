import pygame
import math

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.text = text
        self.dragging = False
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        # Draw text
        label = self.font.render(f"{self.text}: {self.val:.2f}", True, (255, 255, 255))
        screen.blit(label, (self.rect.x, self.rect.y - 25))

        # Draw track
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        
        # Calculate knob position
        val_norm = (self.val - self.min_val) / (self.max_val - self.min_val)
        knob_x = self.rect.x + val_norm * self.rect.width
        knob_rect = pygame.Rect(knob_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        
        # Draw knobs
        color = (200, 200, 200) if not self.dragging else (255, 255, 255)
        pygame.draw.rect(screen, color, knob_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                # Check if click is near the knob or on track (slight padding for easier grab)
                val_norm = (self.val - self.min_val) / (self.max_val - self.min_val)
                knob_x = self.rect.x + val_norm * self.rect.width
                knob_rect = pygame.Rect(knob_x - 10, self.rect.y - 10, 20, self.rect.height + 20)
                
                if knob_rect.collidepoint(mouse_pos) or self.rect.collidepoint(mouse_pos):
                    self.dragging = True
                    self.update_val(mouse_pos[0])

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_val(event.pos[0])

    def update_val(self, mouse_x):
        # Clamp mouse_x to slider rect
        x = max(self.rect.x, min(mouse_x, self.rect.right))
        norm = (x - self.rect.x) / self.rect.width
        self.val = self.min_val + norm * (self.max_val - self.min_val)


class RotatingCube:
    def __init__(self):
        pygame.init()
        self.width = 1000  # Wider to fit sliders
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rotating 3D Cube with Sliders")
        self.clock = pygame.time.Clock()
        
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
        # Sliders
        # x, y, w, h, min, max, initial, text
        self.sliders = [
            Slider(50, 50, 200, 10, 0, 0.2, 0.01, "Speed X"),
            Slider(50, 100, 200, 10, 0, 0.2, 0.01, "Speed Y"),
            Slider(50, 150, 200, 10, 0, 0.2, 0.005, "Speed Z"),
            Slider(50, 200, 200, 10, 50, 300, 100, "Scale"),
        ]

    def run(self):
        running = True
        
        # Cube vertices
        points = []
        # [-1, 1] combinatorics for x, y, z
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    points.append([x, y, z])

        while running:
            self.clock.tick(60)
            self.screen.fill((20, 20, 20)) # Dark gray background
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                # Update sliders
                for slider in self.sliders:
                    slider.handle_event(event)

            # Get values from sliders
            speed_x = self.sliders[0].val
            speed_y = self.sliders[1].val
            speed_z = self.sliders[2].val
            scale = self.sliders[3].val

            # Update rotation angles
            self.angle_x += speed_x
            self.angle_y += speed_y
            self.angle_z += speed_z

            rotation_x = [
                [1, 0, 0],
                [0, math.cos(self.angle_x), -math.sin(self.angle_x)],
                [0, math.sin(self.angle_x), math.cos(self.angle_x)]
            ]

            rotation_y = [
                [math.cos(self.angle_y), 0, math.sin(self.angle_y)],
                [0, 1, 0],
                [-math.sin(self.angle_y), 0, math.cos(self.angle_y)]
            ]

            rotation_z = [
                [math.cos(self.angle_z), -math.sin(self.angle_z), 0],
                [math.sin(self.angle_z), math.cos(self.angle_z), 0],
                [0, 0, 1]
            ]
            
            projected_points = []
            
            # Offset center of drawing to right side to not overlap sliders
            offset_x = self.width // 2 + 100
            offset_y = self.height // 2
            
            for point in points:
                rotated_2d = self.multiply_matrix(rotation_x, point)
                rotated_2d = self.multiply_matrix(rotation_y, rotated_2d)
                rotated_2d = self.multiply_matrix(rotation_z, rotated_2d)
                
                # Projection
                distance = 4
                z = 1 / (distance - rotated_2d[2])
                
                projection_matrix = [
                    [z, 0, 0],
                    [0, z, 0]
                ]
                
                projected_2d = self.multiply_matrix(projection_matrix, rotated_2d)
                
                x = int(projected_2d[0] * scale) + offset_x
                y = int(projected_2d[1] * scale) + offset_y
                
                projected_points.append((x, y))
                pygame.draw.circle(self.screen, (255, 100, 100), (x, y), 5)

            # Draw edges for Cube
            # Points are ordered:
            # 0: -1,-1,-1
            # 1: -1,-1, 1
            # 2: -1, 1,-1
            # 3: -1, 1, 1
            # 4:  1,-1,-1
            # 5:  1,-1, 1
            # 6:  1, 1,-1
            # 7:  1, 1, 1
            
            # Connect logic: 
            # Each point connects to 3 neighbors (flip one coordinate)
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    # Check if points differ by exactly 1 coordinate
                    diff_count = 0
                    p1 = points[i]
                    p2 = points[j]
                    for k in range(3):
                        if p1[k] != p2[k]:
                            diff_count += 1
                    
                    if diff_count == 1:
                        self.connect_points(i, j, projected_points)

            # Draw Sliders
            for slider in self.sliders:
                slider.draw(self.screen)

            pygame.display.update()
            
        pygame.quit()

    def multiply_matrix(self, a, b):
        if isinstance(b[0], (int, float)):
             rows_a = len(a)
             cols_a = len(a[0])
             rows_b = len(b)
             if cols_a != rows_b:
                 raise ValueError("Columns of A must match rows of B")
             result = [0] * rows_a
             for i in range(rows_a):
                 sum_val = 0
                 for j in range(cols_a):
                     sum_val += a[i][j] * b[j]
                 result[i] = sum_val
             return result
        return []

    def connect_points(self, i, j, points):
        pygame.draw.line(self.screen, (255, 255, 255), points[i], points[j], 2)

if __name__ == "__main__":
    app = RotatingCube()
    app.run()
