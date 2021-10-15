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
SCREEN_SIZE = (700, 700)  # параметры размера экранов
screen = pygame.display.set_mode(SCREEN_SIZE)
FONT1 = pygame.font.Font(None, 40)  # шрифт для счётчика

WHITE = (255, 255, 255)

view_scale_coefficient = SCREEN_SIZE[0] / model.MODEL_SIZE[0]
time_scale = 10


def aim_drower(balls, view_scale_coefficient):
    '''
    отрисовывпем шарики
    :param balls: двумерный массив с параметрами шариков, которые нужно отрисовать [5] - цвет, [0] - координата центра
    по x, [1] - по y, [4] - радиус
    '''
    for ball in balls:
        x = int(view_scale_coefficient * ball[0])
        y = int(view_scale_coefficient * ball[1])
        r = int(view_scale_coefficient * ball[4])
        circle(screen, ball[5], (x, y), r)


screen.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()
finished = False  # флажок, показывающий, не произошёл ли QUIT

while not finished:  # главный цикл
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверка на QUIT
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатия мыши, сразу преобразую координаты
            x = event.pos[0] / view_scale_coefficient
            y = event.pos[1] / view_scale_coefficient
            cleek_coords = [x, y]
            model.click_check_slot(event.button, cleek_coords)
    for i in range(0, time_scale):
        balls = model.ball_motion()
    aim_drower(balls, view_scale_coefficient)
    text1 = FONT1.render(str(model.counter), False, (0, 0, 0))  # задаём счётчик
    screen.blit(text1, (10, 10))  # отображаем счётчик
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()
