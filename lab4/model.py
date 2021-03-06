'''
далее все размеры в мм, все времена в с
'''

from random import randint

# задание констант и переменных
global BALL_RADIUS_RANGE, BALL_VELOCITY_RANGE, BALLS_AMOUNT, COLORS, MODEL_SIZE, counter, dT, BALLS_PARAMAMOUNT
BALL_RADIUS_RANGE = [40, 70]  # минимальный и максимальный размеры шарика
BALL_VELOCITY_RANGE = [30, 200]  # минимальная и максимальная скорость шарика
BALLS_AMOUNT = 6  # количество шариков
MODEL_SIZE = (1000, 1000)  # размеры модели
dT = 0.01
BALLS_PARAMAMOUNT = 7 # количетво параметров, которым обладает каждый шарик

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, BLACK]  # список всех возможных окрасок шариков

counter = 0


def ball_create():
    '''
    создаёт параметры шарика и возврашает их массивом, последний параметр массива - указания типа шарика,
    все шарики создаваемые этой функцией нулевого типа
    BALL_RADIUS_RANGE = [] [min_ball_radius, max_ball_radius]
    MODEL_SIZE размер области движения шарика
    BALL_VELOCITY_RANGE - диапозон скоростей шарика по оси (в пикселях/ фрейм)

    шарик случайного цвета из списка создаётся в случайном месте на поле, со скоростью из диапозона
    '''
    ball_radius = randint(BALL_RADIUS_RANGE[0], BALL_RADIUS_RANGE[1])
    ball_x = randint(ball_radius, MODEL_SIZE[0] - ball_radius)
    ball_y = randint(ball_radius, MODEL_SIZE[1] - ball_radius)
    ball_v_x = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    ball_v_y = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1]) * ((-1) ** randint(1, 2))
    color = COLORS[randint(0, len(COLORS) - 1)]
    ball = [ball_x, ball_y, ball_v_x, ball_v_y, ball_radius, color, 0]
    return ball


def model_init():
    '''
    иниуиализация модели: создание двумерного массива с параметрами шариков
    '''
    global balls
    balls = [[] * BALLS_PARAMAMOUNT] * BALLS_AMOUNT  # создаём начальную систему шариков
    for i in range(0, BALLS_AMOUNT):
        balls[i] = ball_create()


def ball_motion():
    '''
    функция отвечает за движение шарика
    при соприкасновении скорость по соответствующей оси меняется на случайную скорость
    из диапозона, направленную от границы соприкасновения
    '''
    for i in range(0, BALLS_AMOUNT):  # для каждого шарика осуществим эволюцию параметров
        x = balls[i][0]  # переобозначим параметры шарика
        y = balls[i][1]
        v_x = balls[i][2]
        v_y = balls[i][3]
        r = balls[i][4]
        # здесь реализуется случайное отражение от стен
        if (x < r - v_x * dT):  # проверка на соприкасновение с левой границей области
            v_x = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        elif (MODEL_SIZE[0] - x - v_x * dT < r): # проверка на соприкасновение с правой границей области
            v_x = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        if (y < r - v_y * dT): # проверка на соприкасновение с верхней границей области
            v_y = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        elif (MODEL_SIZE[1] - y - v_y * dT < r): # проверка на соприкасновение с нижней границей области
            v_y = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        x += v_x * dT  # осуществляется перемещение шарика
        y += v_y * dT
        balls[i][0] = x
        balls[i][1] = y
        balls[i][2] = v_x
        balls[i][3] = v_y
        balls[i][4] = r
    return balls


def click_check_slot(mouse_button, click_coords=()):
    '''
    функция проверяет, попал ли пользователь в шарик и увеичивает очки в случае попадания
    balls - двумерный массив с параметрами шариков
    BALLS_AMOUNT - количество шариков
    :param click_coords: - координаты нажатия
    :param mouse_button: - номер нажатой кнопки
    '''
    global counter
    aimed_ball = -1
    for i in range(0, BALLS_AMOUNT):
        # по теореме поифагора вычислим расстояние от клика до центра шарика и сравним с радиусом
        distance = int(((balls[i][0] - click_coords[0]) ** 2 + (balls[i][1] - click_coords[1]) ** 2) ** 0.5)
        if (balls[i][4] >= distance):  # balls[i][4] - радиус i шарика
            aimed_ball = i
            break
    if (aimed_ball != -1):
        counter += 1
        balls[aimed_ball] = ball_create()
