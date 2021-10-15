from random import randint

global BALL_RADIUS_RANGE, BALL_VELOCITY_RANGE, BALLS_AMOUNT, COLORS, SCREEN_SIZE
BALL_RADIUS_RANGE = [30, 50]  # минимальный и максимальный размеры шарика
BALL_VELOCITY_RANGE = [3, 20]  # минимальная и максимальная скорость шарика
BALLS_AMOUNT = 6  # количество шариков
SCREEN_SIZE = (700, 700)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, BLACK]  # список всех возможных окрасок шариков

def ball_create(BALL_RADIUS_RANGE=[], SCREEN_SIZE=(), BALL_VELOCITY_RANGE=[]):
    '''
    создаёт параметры шарика и возврашает их массивом, последний параметр массива - указания типа шарика,
    все шарики создаваемые этой функцией нулевого типа
    :param BALL_RADIUS_RANGE = []: [min_ball_radius, max_ball_radius]
    :param SCREEN_SIZE: размер экрана
    :param BALL_VELOCITY_RANGE: - диапозон скоростей скоростей шарика по оси (в пикселях/ фрейм)
    '''
    ball_radius = randint(BALL_RADIUS_RANGE[0], BALL_RADIUS_RANGE[1])
    ball_x = randint(ball_radius, SCREEN_SIZE[0] - ball_radius)
    ball_y = randint(ball_radius, SCREEN_SIZE[1] - ball_radius)
    ball_v_x = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    ball_v_y = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    color = COLORS[randint(0, len(COLORS) - 1)]
    ball = [ball_x, ball_y, ball_v_x, ball_v_y, ball_radius, color, 0]
    return ball

def model_init():
    global balls
    balls = [[] * 7] * BALLS_AMOUNT  # создаём начальную систему шариков
    for i in range(0, BALLS_AMOUNT):
        balls[i] = ball_create(BALL_RADIUS_RANGE, SCREEN_SIZE, BALL_VELOCITY_RANGE)
