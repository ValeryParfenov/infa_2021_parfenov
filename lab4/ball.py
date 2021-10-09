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
BALL_LIFE_TIME = 200  # время жизни шарика в фреймах
BALL_VELOCITY_RANGE = [1, 10]  # минимальная и максимальная скорость шарика

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


def ball_create(BALL_RADIUS_RANGE=[], screen_size=(), BALL_VELOCITY_RANGE=[]):
    '''создаёт параметры шарика и возврашает их массивом
    :param BALL_RADIUS_RANGE = []: [min_ball_radius, max_ball_radius]
    :param BALL_VELOCITY_RANGE: - диапозон скоростей скоростей шарика по оси (в пикселях/ фрейм)
    '''
    global ball_radius, ball_x, ball_y
    ball_radius = randint(BALL_RADIUS_RANGE[0], BALL_RADIUS_RANGE[1])
    ball_x = randint(ball_radius, screen_size[0] - ball_radius)
    ball_y = randint(ball_radius, screen_size[1] - ball_radius)
    ball_v_x = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    ball_v_y = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    color = COLORS[randint(0, len(COLORS) - 1)]
    return [ball_x, ball_y, ball_v_x, ball_v_y, ball_radius, color]


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


def ball_motion(ball=[], screensize=[]):
    '''функция отвечает за движение шарика, аргумент - начальное состояние, возвращает коекчное
    ball[0] - координата шарика по x
    balll[1] - координата y
    ball[2] - скорость по x
    ball[3] - скорость по y
    '''
    if (ball[0] < ball[4] - ball[2]):  # здесь реализуется случайное отражение от стен
        ball[2] = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
    elif (screensize[0] - ball[0] - ball[2] < ball[4]):
        ball[2] = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
    if (ball[1] < ball[4] - ball[3]):
        ball[3] = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
    elif (screensize[1] - ball[1] - ball[3] < ball[4]):
        ball[3] = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
    ball[0] += ball[2] # осуществляется перемещение шарика
    ball[1] += ball[3]
    return ball


screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()
finished = False  # флажок, показывающий, не произошёл ли QUIT
ball = ball_create(BALL_RADIUS_RANGE, screen_size, BALL_VELOCITY_RANGE)  # создаём первый шарик
local_time = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверка на QUIT
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатия мыши
            if (click_check_slot(ball[0], ball[1], ball[4], event.button, event.pos) == 1):
                counter += 1
                ball = ball_create(BALL_RADIUS_RANGE, screen_size, BALL_VELOCITY_RANGE)
                local_time = 0
                break
    if (local_time == BALL_LIFE_TIME):
        ball = ball_create(BALL_RADIUS_RANGE, screen_size, BALL_VELOCITY_RANGE)  # создаём шарик
        local_time = 0
    else:
        ball = ball_motion(ball, screen_size)
    circle(screen, ball[5], (ball[0], ball[1]), ball[4])  # отрисовываем шарик
    text1 = font1.render(str(counter), False, (0, 0, 0))  # задаём счётчик
    screen.blit(text1, (10, 10))  # отображаем счётчик
    pygame.display.update()
    screen.fill(WHITE)
    local_time += 1

pygame.quit()
