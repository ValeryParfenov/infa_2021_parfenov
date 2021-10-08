import pygame
from pygame.draw import *
from random import randint

pygame.init()

# Задание констант
FPS = 2 # частота обновления экрана
screen_width, screen_height = screen_size = (700, 700) # параметры размера экранов
screen = pygame.display.set_mode(screen_size)
BALL_RADIUS_RANGE = [10, 50] # минимальный и максимальный размеры шарика

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, BLACK] #список всех возможных окрасок шариков

def new_ball(BALL_RADIUS_RANGE = []):
    '''рисует новый шарик
    :param BALL_RADIUS_RANGE = []: [mib_ball_radius, max_ball_radius]
    '''
    r = randint(BALL_RADIUS_RANGE[0], BALL_RADIUS_RANGE[1])
    x = randint(r, screen_width - r)
    y = randint(r, screen_height - r)
    color = COLORS[randint(0, len(COLORS) - 1)]
    circle(screen, color, (x, y), r)


screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()
finished = False # флажок, показывающий, не произошёл ли QUIT

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
    new_ball(BALL_RADIUS_RANGE)
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()
