"""
PySliders 0.1
A slider add-on for PyGame
Made by SkylaDev
"""

import pygame
from pygame import gfxdraw

from PySliders.aspect_resize import aspect_resize


__title__ = 'PySlider'
__author__ = 'SkylaDev'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2019 SkylaDev'
__version__ = '0.1'
__URL__ = 'https://github.com/SkylaDev/PySliders'

# Set stretch types for the bar image setting
STRETCH = 0 # Stretch the image to fit the canvas
DUPLICATE = 1 # Fill the canvas with the image if its to small
FIT = 2 # Stretch the image to fit the canvas with original image ratio
CENTER = 3 # Keep image size and center it in the middle of the canvas


def show_stretch_types():
    """
    Shows the stretch/fit types used for some functions of the module
    """
    print("""
    {0}.STRETCH - Stretch the image to fit the canvas
    {0}.DUPLICATE - Fill the canvas with the image if its to small
    {0}.FIT - Stretch the image to fit the canvas with original image ratio
    {0}.CENTER - Keep image size and center it in the middle of the canvas
    """.format(__name__))


class HorizontalSlider:
    def __init__(self, lowest_number: int, highest_number: int, current_number: int, low_x: int, high_x: int):
        """
        Creates a horizontal slider object that can be used in a game window

        :param lowest_number: int of the lowest number the slider goes to (Going below 0 can cause problems)
        :param highest_number: int of the highest number the slider goes to (Can not be lower than lowest_number)
        :param current_number: int of the default/starting position of the slider (For large scales this may not work)
        :param low_x: int of the beginning point on the x axis that the slider is rendered to
        :param high_x: int of the end point on the x axis that the slider is rendered to (Can not be lower than low_x)
        """
        self.lowestValue = lowest_number
        self.highestValue = highest_number
        self.valueRange = int(self.highestValue - self.lowestValue)

        self.lowerX = low_x
        self.higherX = high_x
        self.barXWidth = int(self.higherX - self.lowerX)

        self.currentValue = current_number
        self.currentX = int(self.lowerX + (self.barXWidth / self.valueRange) * self.currentValue)

        self.barThickness = 10
        self.barUnfilledColour = (255, 255, 255)
        self.barFilledColour = (200, 200, 200)

        self.mouseDown = False
        self.clickedOn = False

        self.barRenderX = self.lowerX

        self.barWidth = int(self.higherX - self.lowerX)
        self.sliderRadius = 20
        self.sliderColour = (100, 100, 100)

        self.sliderUnfilledBar = self.render_bar(self.barUnfilledColour)
        self.sliderFilledBar = self.render_bar(self.barFilledColour)
        self.slider = self.render_slider(self.sliderColour)

        self.sliderX = int(self.currentX - (self.slider.get_width() / 2))
        self.sliderY = None

    def render_bar_end(self, colour: tuple):
        """
        Used by the render_bar function to render the rounded end of the default bar shape

        :param colour: tuple of the colour in RGB values
        :return: pygame.Surface of the generated bar end
        """
        circumference = int(self.barThickness * 2) + 1
        circle_render = pygame.Surface((circumference, circumference), pygame.SRCALPHA, 32)
        gfxdraw.filled_circle(circle_render, self.barThickness, self.barThickness, self.barThickness, colour)
        gfxdraw.aacircle(circle_render, self.barThickness, self.barThickness, self.barThickness, colour)

        return pygame.transform.smoothscale(circle_render, (self.barThickness, self.barThickness))

    def render_bar(self, colour: tuple):
        """
        Used to update the bar appearance when the colour is changed

        :param colour: tuple of the colour in RGB values
        :return: pygame.Surface of the generated bar
        """
        slider_bar = pygame.Surface((self.barWidth, self.barThickness), pygame.SRCALPHA, 32)
        slider_bar.convert_alpha()

        slider_bar_end = self.render_bar_end(colour)
        slider_bar.blit(slider_bar_end, [0, 0])
        slider_bar.blit(slider_bar_end, [int(self.barWidth - self.barThickness), 0])

        pygame.draw.rect(slider_bar, colour, pygame.Rect(int(self.barThickness / 2), 0,
                                                             self.barXWidth - self.barThickness, self.barThickness))

        return slider_bar

    def render_slider(self, colour: tuple):
        """
        Used to update the bar slider appearance when the colour is changed

        :param colour: tuple of the colour in RGB values
        :return: pygame.Surface of the generated slider
        """
        slider = pygame.Surface((self.sliderRadius * 2, self.sliderRadius * 2), pygame.SRCALPHA, 32)
        slider.convert_alpha()

        gfxdraw.aacircle(slider, self.sliderRadius, self.sliderRadius, self.sliderRadius, colour)
        gfxdraw.filled_circle(slider, self.sliderRadius, self.sliderRadius, self.sliderRadius, colour)

        return slider

    def render(self, window: pygame.Surface, y: int):
        """
        Renders the slider onto the target window/surface

        :param window: pygame.Surface of the target window/surface
        :param y: int of the y position of the bar
        """
        window.blit(self.sliderUnfilledBar.subsurface(int(self.currentX - self.lowerX), 0,
                                                      int(self.sliderUnfilledBar.get_width() -
                                                          int(self.currentX - self.lowerX)), self.barThickness),
                    [int(self.currentX - self.lowerX) + self.barRenderX, y])
        window.blit(self.sliderFilledBar.subsurface(0, 0, int(self.currentX - self.lowerX), self.barThickness),
                    [self.barRenderX, y])
        self.sliderX = int(self.currentX - (self.slider.get_width() / 2))
        self.sliderY = int((y + (self.barThickness / 2)) - (self.slider.get_height() / 2))
        window.blit(self.slider, [self.sliderX, self.sliderY])

    def update(self, mouse_position: tuple, mouse_status: tuple):
        """
        Update the bar to check for movements

        :param mouse_position: tuple of the mouse x and y position
        :param mouse_status: tuple of mouse status made by using pygame.mouse.get_pressed()
        """
        if self.sliderY is not None:
            if mouse_status[0] == 1:
                if not self.mouseDown:
                    if self.sliderX <= mouse_position[0] <= int(self.sliderX + self.slider.get_width()):
                        if self.sliderY <= mouse_position[1] <= int(self.sliderY + self.slider.get_height()):
                            self.clickedOn = True
                        else:
                            self.mouseDown = True
                    else:
                        self.mouseDown = True
            else:
                self.mouseDown = False
                self.clickedOn = False

        if self.clickedOn:
            new_x = mouse_position[0]
            if self.lowerX <= new_x <= self.higherX:
                self.currentX = new_x
            elif new_x < self.lowerX:
                self.currentX = self.lowerX
            elif new_x > self.higherX:
                self.currentX = self.higherX

        self.currentValue = int((self.valueRange / self.barXWidth) * (self.currentX - self.lowerX))

    def set_bar_unfilled_colour(self, colour: tuple):
        """
        Sets the unfilled bar colour and resets the unfilled bar appearance to the default one

        :param colour: tuple of the colour in RGB values
        """
        if type(colour) is int:
            raise ValueError("set_bar_unfilled_colour() expected a tuple with 3 RGB values from 0-255, got: {}".format(colour))
        if len(colour) != 3:
            raise ValueError("set_bar_unfilled_colour() expected a tuple with 3 RGB values from 0-255, got: {}".format(colour))
        for number in colour:
            if type(number) is not int:
                raise ValueError("set_bar_unfilled_colour() expected a tuple with 3 RGB values from 0-255, " +
                                 "got: {0} with invalid value: {1}".format(colour, number))
            if number >= 256 or number <= -1:
                raise ValueError("set_bar_unfilled_colour() expected a tuple with 3 RGB values from 0-255, " +
                                 "got: {0} with invalid value: {1}".format(colour, number))
        
        self.barUnfilledColour = colour
        self.sliderUnfilledBar = self.render_bar(self.barUnfilledColour)

    def set_bar_filled_colour(self, colour: tuple):
        """
        Sets the filled bar colour and resets the filled bar appearance to the default one

        :param colour: tuple of the colour in RGB values
        """
        if type(colour) is int:
            raise ValueError(
                "set_bar_filled_colour() expected a tuple with 3 RGB values from 0-255, got: {}".format(colour))
        if len(colour) != 3:
            raise ValueError(
                "set_bar_filled_colour() expected a tuple with 3 RGB values from 0-255, got: {}".format(colour))
        for number in colour:
            if type(number) is not int:
                raise ValueError("set_bar_filled_colour() expected a tuple with 3 RGB values from 0-255, " +
                                 "got: {0} with invalid value: {1}".format(colour, number))
            if number >= 256 or number <= -1:
                raise ValueError("set_bar_filled_colour() expected a tuple with 3 RGB values from 0-255, " +
                                 "got: {0} with invalid value: {1}".format(colour, number))

        self.barFilledColour = colour
        self.sliderFilledBar = self.render_bar(self.barFilledColour)

    def set_slider_colour(self, colour: tuple):
        """
        Sets the slider colour and resets the slider appearance to the default one

        :param colour: tuple of the colour in RGB values
        """
        if type(colour) is int:
            raise ValueError("set_bar_colour() expected a tuple with 3 RGB values from 0-255, got: {}".format(colour))
        if len(colour) != 3:
            raise ValueError("set_bar_colour() expected a tuple with 3 RGB values from 0-255, got: {}".format(colour))
        for number in colour:
            if type(number) is not int:
                raise ValueError("set_bar_colour() expected a tuple with 3 RGB values from 0-255, " +
                                 "got: {0} with invalid value: {1}".format(colour, number))
            if number >= 256 or number <= -1:
                raise ValueError("set_bar_colour() expected a tuple with 3 RGB values from 0-255, " +
                                 "got: {0} with invalid value: {1}".format(colour, number))

        self.sliderColour = colour
        self.slider = self.render_slider(self.sliderColour)

    def set_slider_image(self, image: pygame.Surface):
        """
        Sets the slider image to a custom one

        :param image: pygame.Surface object
        """
        self.slider = image

    def set_bar_image(self, unfilled_image: pygame.Surface, filled_image: pygame.Surface, stretch_type: int=STRETCH):
        """
        Sets the bar filled and unfilled images to a custom one with a custom fill/stretch type

        :param unfilled_image: pygame.Surface object
        :param filled_image: pygame.Surface object
        :param stretch_type: int of stretch types (0-3 or run PySliders.show_stretch_types() to see the names)
        """
        if stretch_type == STRETCH:
            self.sliderUnfilledBar = pygame.transform.scale(unfilled_image, [self.barWidth, self.barThickness])
            self.sliderFilledBar = pygame.transform.scale(filled_image, [self.barWidth, self.barThickness])

        elif stretch_type == DUPLICATE:
            y = 0
            unfilled_image_dimensions = unfilled_image.get_size()

            self.sliderUnfilledBar = pygame.Surface((self.barWidth, self.barThickness), pygame.SRCALPHA, 32)
            while y is not None:
                x = 0
                while x is not None:
                    self.sliderUnfilledBar.blit(unfilled_image, [x, y])
                    x += unfilled_image_dimensions[0]
                    if x > self.sliderUnfilledBar.get_width():
                        x = None

                y += unfilled_image_dimensions[1]
                if y > self.sliderUnfilledBar.get_height():
                    y = None

            y = 0
            filled_image_dimensions = filled_image.get_size()

            self.sliderFilledBar = pygame.Surface((self.barWidth, self.barThickness), pygame.SRCALPHA, 32)
            while y is not None:
                x = 0
                while x is not None:
                    self.sliderFilledBar.blit(filled_image, [x, y])
                    x += filled_image_dimensions[0]
                    if x > self.sliderFilledBar.get_width():
                        x = None

                y += filled_image_dimensions[1]
                if y > self.sliderFilledBar.get_height():
                    y = None

        elif stretch_type == FIT:
            resized_bar = aspect_resize(unfilled_image, [self.barWidth, self.barThickness])
            self.sliderUnfilledBar = pygame.Surface((self.barWidth, self.barThickness), pygame.SRCALPHA, 32)
            self.sliderUnfilledBar.blit(resized_bar, [int((self.barXWidth / 2) - (resized_bar.get_width() / 2)),
                                                      int((self.barThickness / 2) - (resized_bar.get_height() / 2))])
            resized_bar = aspect_resize(filled_image, [self.barWidth, self.barThickness])
            self.sliderFilledBar = pygame.Surface((self.barWidth, self.barThickness), pygame.SRCALPHA, 32)
            self.sliderFilledBar.blit(resized_bar, [int((self.barXWidth / 2) - (resized_bar.get_width() / 2)),
                                                    int((self.barThickness / 2) - (resized_bar.get_height() / 2))])

        elif stretch_type == CENTER:
            self.sliderUnfilledBar = pygame.Surface((self.barWidth, self.barThickness), pygame.SRCALPHA, 32)
            self.sliderUnfilledBar.blit(unfilled_image, [int((self.barWidth / 2) - (unfilled_image.get_width() / 2)),
                                                         int((self.barThickness / 2) -
                                                             (unfilled_image.get_height() / 2))])

            self.sliderFilledBar = pygame.Surface((self.barWidth, self.barThickness), pygame.SRCALPHA, 32)
            self.sliderFilledBar.blit(filled_image, [int((self.barWidth / 2) - (filled_image.get_width() / 2)),
                                                     int((self.barThickness / 2) - (filled_image.get_height() / 2))])

        else:
            raise ValueError("set_bar_image() expected a stretch_type of value 0-3 but got: {}, ".format(stretch_type) +
                             "run help({}) to see the names of the presets".format(__name__))


        #self.sliderUnfilledBar = unfilled_image
        #self.sliderFilledBar = filled_image

    def set_current_value(self, value: int):
        """
        Manually set the current value that the slider is set to

        :param value: int of value (must be within the current slider range)
        """
        if value >= self.highestValue + 1:
            raise ValueError("Value {0} is over the maximum value this slider is set to ({1})".format(value,
                                                                                                      self.highestValue
                                                                                                      ))
        if value <= self.lowestValue - 1:
            raise ValueError("Value {0} is under the minimum value this slider is set to ({1})".format(value,
                                                                                                       self.lowestValue
                                                                                                       ))
        self.currentValue = value
        self.currentX = int(self.lowerX + (self.barXWidth / self.valueRange) * self.currentValue)

    def set_bar_thickness(self, value: int):
        """
        Set the thickness of the bar

        :param value: int of the bar thickness (Must be 1+)
        """
        if value <= 0:
            raise ValueError("Value {0} is under the minimum value that is allowed (1)".format(value))

        self.barThickness = value

    def get_slider_image(self):
        """
        Get the current slider image

        :return: pygame.Surface object
        """
        return self.slider

    def get_bar_unfilled_image(self):
        """
        Get the current unfilled bar image

        :return: pygame.Surface object
        """
        return self.sliderUnfilledBar

    def get_bar_filled_image(self):
        """
        Get the current filled bar image

        :return: pygame.Surface object
        """
        return self.sliderFilledBar

    def get_current_value(self):
        """
        Get the current value that the slider is set to

        :return: int of the current value
        """
        return self.currentValue

    def get_lowest_value(self):
        """
        Get the lowest value of the slider

        :return: int of the lowest value
        """
        return self.lowestValue

    def get_highest_value(self):
        """
        Get the highest value of the slider

        :return: int of the highest value
        """
        return self.highestValue

    def get_current_x(self):
        """
        Get the current x position of the slider object

        :return: int of the current x position
        """
        return self.currentX

    def get_lowest_x(self):
        """
        Get the lowest x position of the slider bar

        :return: int of the lowest x position
        """
        return self.lowerX

    def get_higher_x(self):
        """
        Get the highest x position of the slider bar

        :return: int of the highest x position
        """
        return self.higherX
