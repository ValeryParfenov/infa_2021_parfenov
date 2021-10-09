import pygame
from pygame.draw import *
from random import randint

pygame.init()

# Задание констант
FPS = 30  # частота обновления экрана
screen_width, screen_height = screen_size = (700, 700)  # параметры размера экранов
screen = pygame.display.set_mode(screen_size)
BALL_RADIUS_RANGE = [30, 50]  # минимальный и максимальный размеры шарика
font1 = pygame.font.Font(None, 40)  # шрифт для счётчика
BALL_VELOCITY_RANGE = [3, 20]  # минимальная и максимальная скорость шарика
BALLS_AMOUNT = 6 # количество шариков на экране

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
    '''
    создаёт параметры шарика и возврашает их массивом, последний параметр массива - указания типа шарика,
    все шарики создаваемые этой функцией нулевого типа
    :param BALL_RADIUS_RANGE = []: [min_ball_radius, max_ball_radius]
    :param BALL_VELOCITY_RANGE: - диапозон скоростей скоростей шарика по оси (в пикселях/ фрейм)
    '''
    ball_radius = randint(BALL_RADIUS_RANGE[0], BALL_RADIUS_RANGE[1])
    ball_x = randint(ball_radius, screen_size[0] - ball_radius)
    ball_y = randint(ball_radius, screen_size[1] - ball_radius)
    ball_v_x = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    ball_v_y = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    color = COLORS[randint(0, len(COLORS) - 1)]
    balls = [ball_x, ball_y, ball_v_x, ball_v_y, ball_radius, color, 0]
    return balls


def click_check_slot(balls, BALLS_AMOUNT, mouse_button, mouse_coords=()):
    '''
    функция проверяет, попал ли пользователь в шарик. Если попал - возвращается 1, иначе - 0
    :param ball_x: - координата шарика х
    :param ball_y: - координата шарика у
    :param ball_r: - радиус шарика
    :param mouse_coords: - координаты нажатия
    :param mouse_button: - номер нажатой кнопки
    '''
    for i in range(0, BALLS_AMOUNT):
        distance = int(((balls[i][0] - mouse_coords[0]) ** 2 + (balls[i][1] - mouse_coords[1]) ** 2) ** 0.5)
        if (balls[i][4] >= distance):
            return i
    return -1


def ball_motion(balls, BALLS_AMOUNT, screensize=[]):
    '''
    функция отвечает за движение шарика, аргумент - начальное состояние, возвращает коекчное
    balls[0] - координата шарика по x
    balls[1] - координата y
    balls[2] - скорость по x
    balls[3] - скорость по y
    '''
    for i in range(0, BALLS_AMOUNT):
        if (balls[i][0] < balls[i][4] - balls[i][2]):  # здесь реализуется случайное отражение от стен
            balls[i][2] = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        elif (screensize[0] - balls[i][0] - balls[i][2] < balls[i][4]):
            balls[i][2] = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        if (balls[i][1] < balls[i][4] - balls[i][3]):
            balls[i][3] = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        elif (screensize[1] - balls[i][1] - balls[i][3] < balls[i][4]):
            balls[i][3] = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        balls[i][0] += balls[i][2]  # осуществляется перемещение шарика
        balls[i][1] += balls[i][3]
    return balls


screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()
finished = False  # флажок, показывающий, не произошёл ли QUIT

balls = [[] * 7] * BALLS_AMOUNT
for i in range(0, BALLS_AMOUNT):
    balls[i] = ball_create(BALL_RADIUS_RANGE, screen_size, BALL_VELOCITY_RANGE)


while not finished: # главный цикл
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверка на QUIT
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатия мыши
            ball_id = click_check_slot(balls, BALLS_AMOUNT, event.button, event.pos)
            if (ball_id != -1):
                counter += 1
                balls[ball_id] = ball_create(BALL_RADIUS_RANGE, screen_size, BALL_VELOCITY_RANGE)
    balls = ball_motion(balls, BALLS_AMOUNT, screen_size)
    for i in range(0, BALLS_AMOUNT): # отрисовываем шарики
        circle(screen, balls[i][5], (balls[i][0], balls[i][1]), balls[i][4])
    text1 = font1.render(str(counter), False, (0, 0, 0))  # задаём счётчик
    screen.blit(text1, (10, 10))  # отображаем счётчик
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()
