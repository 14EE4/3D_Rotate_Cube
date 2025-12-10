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
        label = self.font.render(f"{self.text}: {self.val:.3f}", True, (255, 255, 255))
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
        x = max(self.rect.x, min(mouse_x, self.rect.right))
        norm = (x - self.rect.x) / self.rect.width
        self.val = self.min_val + norm * (self.max_val - self.min_val)


class RotatingTesseract:
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rotating Tesseract with Sliders")
        self.clock = pygame.time.Clock()
        
        self.angle_zw = 0
        self.angle_xw = 0
        self.angle_xy = 0
        
        self.sliders = [
            Slider(50, 50, 200, 10, 0, 0.1, 0.02, "Speed ZW (4D)"),
            Slider(50, 100, 200, 10, 0, 0.1, 0.00, "Speed XW (4D)"),
            Slider(50, 150, 200, 10, 0, 0.1, 0.00, "Speed XY (3D)"),
            Slider(50, 200, 200, 10, 50, 1000, 250, "Scale"),
        ]
        
    def run(self):
        running = True
        
        # Tesseract vertices (16 points)
        points = []
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    for w in [-1, 1]:
                        points.append([x, y, z, w])

        while running:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0)) # Black background
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                for slider in self.sliders:
                    slider.handle_event(event)

            # Update angles
            self.angle_zw += self.sliders[0].val
            self.angle_xw += self.sliders[1].val
            self.angle_xy += self.sliders[2].val
            scale = self.sliders[3].val

            # 4D Rotation Matrices
            rot_zw = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, math.cos(self.angle_zw), -math.sin(self.angle_zw)],
                [0, 0, math.sin(self.angle_zw), math.cos(self.angle_zw)]
            ]
            
            rot_xw = [
                [math.cos(self.angle_xw), 0, 0, -math.sin(self.angle_xw)],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [math.sin(self.angle_xw), 0, 0, math.cos(self.angle_xw)]
            ]
            
            rot_xy = [
                [math.cos(self.angle_xy), -math.sin(self.angle_xy), 0, 0],
                [math.sin(self.angle_xy), math.cos(self.angle_xy), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
            
            projected_2d_points = []
            
            offset_x = self.width // 2 + 100
            offset_y = self.height // 2
            
            for point in points:
                # Apply rotations
                rotated = self.multiply_matrix_4d(rot_zw, point)
                rotated = self.multiply_matrix_4d(rot_xw, rotated)
                rotated = self.multiply_matrix_4d(rot_xy, rotated)
                
                # 4D to 3D Projection
                distance = 3
                w = 1 / (distance - rotated[3])
                
                projection_4d = [
                    [w, 0, 0, 0],
                    [0, w, 0, 0],
                    [0, 0, w, 0]
                ]
                
                projected_3d = self.multiply_matrix(projection_4d, rotated)
                
                # 3D to 2D Projection
                distance_2 = 4
                z = 1 / (distance_2 - projected_3d[2])
                
                projection_3d = [
                    [z, 0, 0],
                    [0, z, 0]
                ]
                
                projected_2d = self.multiply_matrix(projection_3d, projected_3d)
                
                x = int(projected_2d[0] * scale) + offset_x
                y = int(projected_2d[1] * scale) + offset_y
                
                projected_2d_points.append((x, y))
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 3)
            
            # Draw edges
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    diff_count = 0
                    p1 = points[i]
                    p2 = points[j]
                    for k in range(4):
                        if p1[k] != p2[k]:
                            diff_count += 1
                    
                    if diff_count == 1:
                         self.connect_points(i, j, projected_2d_points)

            # Draw Sliders
            for slider in self.sliders:
                slider.draw(self.screen)

            pygame.display.update()
            
        pygame.quit()

    def multiply_matrix_4d(self, a, b):
        result = [0] * 4
        for i in range(4):
            sum_val = 0
            for j in range(4):
                sum_val += a[i][j] * b[j]
            result[i] = sum_val
        return result

    def multiply_matrix(self, a, b):
         rows_a = len(a)
         cols_a = len(a[0])
         result = [0] * rows_a
         for i in range(rows_a):
             sum_val = 0
             for j in range(cols_a):
                 sum_val += a[i][j] * b[j]
             result[i] = sum_val
         return result

    def connect_points(self, i, j, points):
        pygame.draw.line(self.screen, (100, 255, 100), points[i], points[j], 1)

if __name__ == "__main__":
    app = RotatingTesseract()
    app.run()
