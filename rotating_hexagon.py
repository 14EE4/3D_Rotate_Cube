import pygame
import math

class RotatingHexagon:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rotating 3D Hexagon")
        self.clock = pygame.time.Clock()
        
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
    def run(self):
        running = True
        scale = 100
        
        # Hexagonal prism vertices
        # Two hexagons (front and back/top and bottom depending on orientation)
        points = []
        
        # Create vertices for a hexagon
        for i in range(6):
            # Angle for each vertex (60 degrees = pi/3 radians)
            theta = i * (2 * math.pi / 6)
            x = math.cos(theta)
            y = math.sin(theta)
            
            # Add two points per vertex for the prism thickness (z-axis)
            points.append([x, y, -0.5]) # Back face
            points.append([x, y, 0.5])  # Front face

        while running:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0)) # Black background
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Update rotation angles
            self.angle_x += 0.01
            self.angle_y += 0.01
            self.angle_z += 0.005

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
            
            for point in points:
                rotated_2d = self.multiply_matrix(rotation_x, point)
                rotated_2d = self.multiply_matrix(rotation_y, rotated_2d)
                rotated_2d = self.multiply_matrix(rotation_z, rotated_2d)
                
                # Projection (simple orthographic-like with distance scaling)
                distance = 4
                z = 1 / (distance - rotated_2d[2])
                
                projection_matrix = [
                    [z, 0, 0],
                    [0, z, 0]
                ]
                
                projected_2d = self.multiply_matrix(projection_matrix, rotated_2d)
                
                x = int(projected_2d[0] * scale) + self.width // 2
                y = int(projected_2d[1] * scale) + self.height // 2
                
                projected_points.append((x, y))
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 5)

            # Draw edges
            # Points are stored as [back_vertex_i, front_vertex_i, back_vertex_i+1, front_vertex_i+1...]
            # Actually I stored them as:
            # i=0: [x,y,-0.5], [x,y,0.5]
            # i=1: [x,y,-0.5], [x,y,0.5]
            # ...
            # So projected_points matches this order.
            
            for i in range(6):
                # Indices for current pair
                p1_idx = i * 2         # Back face vertex
                p2_idx = i * 2 + 1     # Front face vertex
                
                # Indices for next pair (wrapping around)
                p3_idx = ((i + 1) * 2) % 12      # Next Back face vertex
                p4_idx = ((i + 1) * 2 + 1) % 12  # Next Front face vertex
                
                # Connect front to back (prism sides)
                self.connect_points(p1_idx, p2_idx, projected_points)
                
                # Connect back to next back (back face edges)
                self.connect_points(p1_idx, p3_idx, projected_points)
                
                # Connect front to next front (front face edges)
                self.connect_points(p2_idx, p4_idx, projected_points)

            pygame.display.update()
            
        pygame.quit()

    def multiply_matrix(self, a, b):
        # Matrix multiplication implementation
        # a is matrix (list of lists), b is vector (list) or matrix
        
        # If b is a 1D list (vector)
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
             
        # If b is a matrix (not needed for this simple projection but good for completeness if expanded)
        # keeping it simple for vector mult only as that's what we use.
        return []

    def connect_points(self, i, j, points):
        pygame.draw.line(self.screen, (255, 255, 255), points[i], points[j], 2)

if __name__ == "__main__":
    app = RotatingHexagon()
    app.run()
