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
            model.click_check_slot(event.button, event.pos)
    balls = model.ball_motion()
    aim_drower(balls)
    text1 = FONT1.render(str(model.counter), False, (0, 0, 0))  # задаём счётчик
    screen.blit(text1, (10, 10))  # отображаем счётчик
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()
