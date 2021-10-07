import pygame
def load_image(image_path, screen_size):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, screen_size)
    return image