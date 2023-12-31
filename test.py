import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pixel Movement")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up pixel properties
pixel_size = 20
pixel_x, pixel_y = width // 2, height // 2
speed = 1

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Calculate movement vector
    move_x = 0
    move_y = 0

    if keys[pygame.K_LEFT]:
        move_x = -speed
    elif keys[pygame.K_RIGHT]:
        move_x = speed

    if keys[pygame.K_UP]:
        move_y = -speed
    elif keys[pygame.K_DOWN]:
        move_y = speed

    # Normalize the movement vector
    magnitude = (move_x ** 2 + move_y ** 2) ** 0.5
    if magnitude != 0:
        move_x /= magnitude
        move_y /= magnitude

    # Update pixel position
    pixel_x += move_x * speed
    pixel_y += move_y * speed

    print(pixel_x, pixel_y)
    # Draw background
    screen.fill(white)

    # Draw pixel
    pygame.draw.rect(screen, black, (pixel_x, pixel_y, pixel_size, pixel_size))

    # Update display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(30)
