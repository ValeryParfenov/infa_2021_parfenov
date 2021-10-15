import pygame
import model
from pygame.draw import *
from random import randint

pygame.init()
model.model_init()
balls = model.balls
BALLS_AMOUNT = model.BALLS_AMOUNT
BALL_VELOCITY_RANGE = model.BALL_VELOCITY_RANGE

# Задание констант
FPS = 30  # частота обновления экрана
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (700, 700)  # параметры размера экранов
screen = pygame.display.set_mode(SCREEN_SIZE)
FONT1 = pygame.font.Font(None, 40)  # шрифт для счётчика

WHITE = (255, 255, 255)

# задаём пеоеменные
counter = 0  # счётчик очков


def click_check_slot(balls, BALLS_AMOUNT, mouse_button, mouse_coords=()):
    '''
    функция проверяет, попал ли пользователь в шарик. Если попал - возвращается номер шарика,
    в который попал пльзователь, иначе - -1
    :param balls: - двумерный массив с параметрами шариков
    :param BALLS_AMOUNT: - количество шариков
    :param mouse_coords: - координаты нажатия
    :param mouse_button: - номер нажатой кнопки
    '''
    for i in range(0, BALLS_AMOUNT):
        distance = int(((balls[i][0] - mouse_coords[0]) ** 2 + (balls[i][1] - mouse_coords[1]) ** 2) ** 0.5)
        if (balls[i][4] >= distance):  # balls[i][4] - радиус i шарика
            return i
    return -1


def ball_motion(balls, BALLS_AMOUNT, screensize=[]):
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
        elif (screensize[0] - x - v_x < r):
            v_x = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        if (y < r - v_y):
            v_y = randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        elif (screensize[1] - y - v_y < r):
            v_y = -1 * randint(BALL_VELOCITY_RANGE[0], BALL_VELOCITY_RANGE[1])
        x += v_x  # осуществляется перемещение шарика
        y += v_y
        balls[i][0] = x
        balls[i][1] = y
        balls[i][2] = v_x
        balls[i][3] = v_y
        balls[i][4] = r
    return balls


def aim_drower(balls):
    '''
    отрисовывпем шарики
    :param balls: двумерный массив с параметрами шариков, которые нужно отрисовать [5] - цвет, [0] - координата центра
    по x, [1] - по y, [4] - радиус
    '''
    for ball in balls:
        circle(screen, ball[5], (ball[0], ball[1]), ball[4])


screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()
finished = False  # флажок, показывающий, не произошёл ли QUIT

while not finished:  # главный цикл
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверка на QUIT
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатия мыши
            ball_id = click_check_slot(balls, BALLS_AMOUNT, event.button, event.pos)
            if (ball_id != -1):
                counter += 1
                balls[ball_id] = ball_create(BALL_RADIUS_RANGE, SCREEN_SIZE, BALL_VELOCITY_RANGE)
    balls = ball_motion(balls, BALLS_AMOUNT, SCREEN_SIZE)
    aim_drower(balls)
    text1 = FONT1.render(str(counter), False, (0, 0, 0))  # задаём счётчик
    screen.blit(text1, (10, 10))  # отображаем счётчик
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()
