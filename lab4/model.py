from random import randint

global BALL_RADIUS_RANGE, BALL_VELOCITY_RANGE, BALLS_AMOUNT, COLORS, SCREEN_SIZE, counter
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

counter = 0

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

def ball_motion():
    '''
    функция отвечает за движение шарика, аргумент balls - двумерный массив с началньным
    состоянием шариков, возвращает конечное
    '''
    for i in range(0, BALLS_AMOUNT):  # для каждого шарика осуществим эволюцию параметров
        x = balls[i][0]  # переобозначим параметры шарика
        y = balls[i][1]
        v_x = balls[i][2]
        v_y = balls[i][3]
        r = balls[i][4]
        if (x < r - v_x):  # здесь реализуется случайное отражение от стен
            v_x = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        elif (SCREEN_SIZE[0] - x - v_x < r):
            v_x = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        if (y < r - v_y):
            v_y = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        elif (SCREEN_SIZE[1] - y - v_y < r):
            v_y = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        x += v_x  # осуществляется перемещение шарика
        y += v_y
        balls[i][0] = x
        balls[i][1] = y
        balls[i][2] = v_x
        balls[i][3] = v_y
        balls[i][4] = r
    return balls

def click_check_slot(mouse_button, mouse_coords=()):
    '''
    функция проверяет, попал ли пользователь в шарик. Если попал - возвращается номер шарика,
    в который попал пльзователь, иначе - -1
    :param balls: - двумерный массив с параметрами шариков
    :param BALLS_AMOUNT: - количество шариков
    :param mouse_coords: - координаты нажатия
    :param mouse_button: - номер нажатой кнопки
    '''
    global counter
    aimed_ball = -1
    for i in range(0, BALLS_AMOUNT):
        distance = int(((balls[i][0] - mouse_coords[0]) ** 2 + (balls[i][1] - mouse_coords[1]) ** 2) ** 0.5)
        if (balls[i][4] >= distance):  # balls[i][4] - радиус i шарика
            aimed_ball = i
            break
    if (aimed_ball != -1):
        counter += 1
        balls[aimed_ball] = ball_create(BALL_RADIUS_RANGE, SCREEN_SIZE, BALL_VELOCITY_RANGE)