import pygame
class Loader:

    def load_image(image_path, screen_size):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, screen_size)
        return image

    def adjust_size(icon, height_limit):
        width, height = icon.get_size()
        scale = height_limit/height
        return(pygame.transform.scale(icon, (int(width*scale), int(height*scale))))

    # load icons used in button
    def load_icons(height_limit, *name):
        icons_tuple = tuple(adjust_size(pygame.image.load("assets/icons/"+n), height_limit) for n in name)
        return(icons_tuple)