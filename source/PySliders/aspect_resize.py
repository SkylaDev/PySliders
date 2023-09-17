import pygame

def aspect_resize(surface: pygame.Surface, rect):
    """
    Resize a surface to fit in a square area while keeping its aspect ratio

    :param surface: pygame.Surface object
    :param rect: A tuple of the x and y size of the rect (eg: [100, 150] or (100, 150))
    :return: pygame.Surface object
    """
    surface_x, surface_y = surface.get_size()

    if surface_x > surface_y:
        resize_scale_factor = rect[0] / float(surface_x)
        new_y = resize_scale_factor * surface_y

        if new_y > rect[1]:
            scale_factor = rect[1] / float(surface_y)
            new_x = scale_factor * surface_x
            new_y = rect[1]
        else:
            new_x = rect[0]

    else:
        scale_factor = rect[1] / float(surface_y)
        new_x = scale_factor * surface_x

        if new_x > rect[0]:
            scale_factor = rect[0] / float(surface_x)
            new_y = scale_factor * surface_y
            new_x = rect[0]
        else:
            new_y = rect[1]

    return pygame.transform.scale(surface, (int(new_x), int(new_y)))
