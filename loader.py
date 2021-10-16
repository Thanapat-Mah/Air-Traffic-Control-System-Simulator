import pygame
class Loader:

    def load_image(self, image_path, screen_size, scale):
        screen_size_scaled = (screen_size[0]*scale, screen_size[1]*scale)
        image_loaded = pygame.image.load(image_path)
        return pygame.transform.scale(image_loaded, screen_size_scaled)

    def adjust_size(self, icon, height_limit):
        width, height = icon.get_size()
        scale = height_limit/height
        return(pygame.transform.scale(icon, (int(width*scale), int(height*scale))))

    # load icons used in button
    def load_icons(self, height_limit, *name):
        icons_tuple = tuple(self.adjust_size(pygame.image.load("assets/icons/"+n), height_limit) for n in name)
        return(icons_tuple)