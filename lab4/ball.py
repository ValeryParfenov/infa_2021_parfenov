import pygame
from pygame.draw import *
from random import randint

pygame.init()

# Задание констант
FPS = 30  # частота обновления экрана
screen_width, screen_height = screen_size = (700, 700)  # параметры размера экранов
screen = pygame.display.set_mode(screen_size)
BALL_RADIUS_RANGE = [10, 50]  # минимальный и максимальный размеры шарика
font1 = pygame.font.Font(None, 40)  # шрифт для счётчика
BALL_LIFE_TIME = 60  # время жизни шарика в фреймах

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, BLACK]  # список всех возможных окрасок шариков

# задаём реоеменные
counter = 0  # счётчик очков


def ball_create(BALL_RADIUS_RANGE=[], screen_size=()):
    '''создаёт параметры шарика и возврашает их массивом
    :param BALL_RADIUS_RANGE = []: [min_ball_radius, max_ball_radius]
    '''
    global ball_radius, ball_x, ball_y
    ball_radius = randint(BALL_RADIUS_RANGE[0], BALL_RADIUS_RANGE[1])
    ball_x = randint(ball_radius, screen_size[0] - ball_radius)
    ball_y = randint(ball_radius, screen_size[1] - ball_radius)
    color = COLORS[randint(0, len(COLORS) - 1)]
    return [ball_x, ball_y, ball_radius, color]


def click_check_slot(ball_x, ball_y, ball_r, mouse_button, mouse_coords=()):
    '''
    функция проверяет, попал ли пользователь в шарик. Если попал - возвращается 1, иначе - 0
    :param ball_x: - координата шарика х
    :param ball_y: - координата шарика у
    :param ball_r: - радиус шарика
    :param mouse_coords: - координаты нажатия
    :param mouse_button: - номер нажатой кнопки
    '''
    distance = int(((ball_x - mouse_coords[0]) ** 2 + (ball_y - mouse_coords[1]) ** 2) ** 0.5)
    if (ball_r >= distance):
        return 1
    else:
        return 0


screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()
finished = False  # флажок, показывающий, не произошёл ли QUIT
ball = ball_create(BALL_RADIUS_RANGE, screen_size)  # создаём первый шарик
local_time = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверка на QUIT
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатия мыши
            if (click_check_slot(ball_x, ball_y, ball_radius, event.button, event.pos) == 1):
                counter += 1
                ball = ball_create(BALL_RADIUS_RANGE, screen_size)
                local_time = 0
                break
    if (local_time == BALL_LIFE_TIME):
        ball = ball_create(BALL_RADIUS_RANGE, screen_size)  # создаём шарик
        local_time = 0
    circle(screen, ball[3], (ball[0], ball[1]), ball[2])  # отрисовываем шарик
    text1 = font1.render(str(counter), False, (0, 0, 0))  # задаём счётчик
    screen.blit(text1, (10, 10))  # отображаем счётчик
    pygame.display.update()
    screen.fill(WHITE)
    local_time += 1

pygame.quit()
