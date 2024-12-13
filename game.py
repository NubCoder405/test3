import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('game')

# Define colors
border_color = (40, 40, 40)  # Lighter color for the border
border_thickness = 15  # Thickness of the border

# Box dimensions
box_width = 700  # Width of the box
box_height = 400  # Height of the box
box_x = (width - box_width) // 2  # Centering the box
box_y = (height - box_height) // 2  # Centering the box

# Load image for the floor
image = pygame.image.load('floor1.png').convert()
scaled_image = pygame.transform.scale(image, (box_width, box_height))

class Dot():
    def __init__(self, color, radius, x, y, speed):
        self.color = color
        self.radius = radius
        self.x = x
        self.y = y
        self.speed = speed

    def move(self, direction):
        # Movement logic with boundary checks
        if direction == 'left':
            self.x -= self.speed
            if self.x < box_x + self.radius:
                self.x = box_x + self.radius
        elif direction == 'right':
            self.x += self.speed
            if self.x > (box_x + box_width) - self.radius:
                self.x = (box_x + box_width) - self.radius
        elif direction == 'up':
            self.y -= self.speed
            if self.y < box_y + self.radius:
                self.y = box_y + self.radius
        elif direction == 'down':
            self.y += self.speed
            if self.y > (box_y + box_height) - self.radius:
                self.y = (box_y + box_height) - self.radius
    
    def draw(self, surface):
        """ Draw dot in the surface """
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

class Bullet():
    def __init__(self):
        self.radius = 5
        self.color = (255, 0, 0)
        # Choose random side
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(0, width)
            self.y = 0
        elif side == 'bottom':
            self.x = random.randint(0, width)
            self.y = height
        elif side == 'left':
            self.x = 0
            self.y = random.randint(0, height)
        else:  # right
            self.x = width
            self.y = random.randint(0, height)
        
        # Movement speed towards the center
        self.speed_x = random.uniform(-2, 8)
        self.speed_y = random.uniform(-2, 8)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, dot):
        # Simple collision detection between the bullet and the dot
        distance = ((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2) ** 0.5
        return distance < (self.radius + dot.radius)

# Instantiate the dot
dot = Dot(color=(255, 255, 255), radius=8.5, x=width // 2, y=height // 2, speed=4)
bullets = []

clock = pygame.time.Clock()

# Initialize variables for bullet spawn probability
base_probability = 0.05  # Base probability
time_increment = 0.01  # Increment in probability per frame
max_probability = 1  # Maximum bullet spawn probability
elapsed_time = 0  # Track the elapsed time

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Move the dot based on key presses
    if keys[pygame.K_LEFT]:
        dot.move("left")
    if keys[pygame.K_RIGHT]:
        dot.move("right")
    if keys[pygame.K_UP]:
        dot.move('up')
    if keys[pygame.K_DOWN]:
        dot.move('down')

    # Update the elapsed time
    elapsed_time += clock.get_time() / 1000.0  # Convert milliseconds to seconds

    # Adjust bullet spawn probability based on time
    current_probability = min(base_probability + elapsed_time * time_increment, max_probability)

    # Randomly spawn bullets based on the adjusted probability
    if random.random() < current_probability:  
        bullets.append(Bullet())

    # Draw everything
    screen.fill((0, 200, 200))
    pygame.draw.rect(screen, border_color, (box_x - border_thickness, box_y - border_thickness, box_width + border_thickness * 2, box_height + border_thickness * 2))
    screen.blit(scaled_image, (box_x, box_y))
    dot.draw(screen)

    for bullet in bullets:
        bullet.move()
        bullet.draw(screen)
        if bullet.check_collision(dot):
            print("Game Over!")
            pygame.quit()
            sys.exit()
        if bullet.x < 0 or bullet.x > width or bullet.y < 0 or bullet.y > height:
            bullets.remove(bullet)

    pygame.display.flip()
    clock.tick(60)
