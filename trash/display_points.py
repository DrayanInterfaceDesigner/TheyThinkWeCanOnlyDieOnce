import cv2
import numpy as np
from multiprocessing.connection import Client
import pygame
from pygame.locals import QUIT

# Establish a connection for inter-process communication
address = ('localhost', 6000)
conn = Client(address, authkey=b'secret_key')

pygame.init()

# Create Pygame window and set background image
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Facial Landmarks with Images")
img = 255 * np.ones((480, 640, 3), dtype=np.uint8)
img_surface = pygame.surfarray.make_surface(img)
screen.blit(img_surface, (0, 0))
pygame.display.flip()

def lerp(start, end, alpha):
    return start * (1 - alpha) + end * alpha

def draw_images_on_points(positions, image_path, image_size=(50, 50), smoothing=0.1):
    # Clear the screen by filling it with the background color
    screen.fill((255, 255, 255))

    # Ensure that there is a previous position for each point
    if not hasattr(draw_images_on_points, 'prev_positions'):
        draw_images_on_points.prev_positions = [(0, 0) for _ in positions]

    for i, position in enumerate(positions):
        x, y = position
        image = pygame.image.load(image_path).convert_alpha()

        # Adjust the position to center the image on the point
        x -= image_size[0] // 2
        y -= image_size[1] // 2

        # Ensure the image stays within the frame
        x = max(0, min(x, img.shape[1] - image_size[0]))
        y = max(0, min(y, img.shape[0] - image_size[1]))

        # Smoothly move the image to the new position using lerp
        current_x, current_y = draw_images_on_points.prev_positions[i]
        target_x, target_y = x, y

        current_x = lerp(current_x, target_x, smoothing)
        current_y = lerp(current_y, target_y, smoothing)

        draw_images_on_points.prev_positions[i] = (current_x, current_y)

        # Resize the image
        image = pygame.transform.scale(image, image_size)

        # Draw the resized image onto the screen
        screen.blit(image, (current_x, current_y))

    pygame.display.flip()


while True:
    # Receive facial landmarks positions from the other script
    landmarks = conn.recv()

    # Draw circles at the received positions
    for landmark in landmarks:
        cv2.circle(img, landmark, 3, (0, 255, 0), -1)

    # Draw images on the points with a specified image path
    draw_images_on_points(landmarks, image_path='left_eye_image.png')

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            conn.close()
            exit()

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pygame.quit()
        conn.close()
        break
