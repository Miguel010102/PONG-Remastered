import pygame
from psutil import Process
import os

def get_memory_usage() -> float:
    process: Process = Process(os.getpid())
    megabytes: float = process.memory_info().rss / (1024 * 1024)
    return megabytes

def draw_text(surface, text, font_size, x, y, color):
    # create a font object
    font = pygame.font.Font(None, font_size)
    # create a text surface objects:
    text_surface = font.render(text, True, color)
    # get the size of the text surface
    text_rect = text_surface.get_rect()
    # center the text surface on the given coordinates
    text_rect.center = (x, y)
    # draw the text surface onto the given surface
    surface.blit(text_surface, text_rect)


def draw_button(surface, text, font_size, x, y, width, height, color):
    # create a button surface object
    button_surface = pygame.Surface((width, height))
    button_surface.fill((255, 255, 255))
    # create a font object
    font = pygame.font.Font(None, font_size)
    # create a text surface object
    text_surface = font.render(text, True, color)
    button_surface.blit(
        text_surface, text_surface.get_rect(center=(width / 2, height / 2))
    )
    # get the size of the button surface
    button_rect = button_surface.get_rect()
    # center the button surface on the given coordinates
    button_rect.center = (x, y)
    # draw the button surface onto the given surface
    surface.blit(button_surface, button_rect)
    # return the button object
    return button_rect