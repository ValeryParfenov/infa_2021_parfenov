import math
import random
import random as rnd
from random import choice
import pygame

pygame.init()

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

FONT_FOR_COUNTER = pygame.font.Font(None, 40)
TARGET_VELOCITY_RANGE = [5, 30]  # диапозон скоростей мишени
FPS = 30
MAX_BALL_LIVES = 80  # время жизни снаряда в кадрах
G = 2  # аналог ускорения свободного падения
WIDTH = 800  # параметры экрана
HEIGHT = 600


class Bullet:
    def __init__(self, G, MAX_BULLET_LIVES, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса Shot
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = MAX_BULLET_LIVES
        self.G = G

    def move(self):
        """
        Метод описывает перемещение снаряда за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if (self.x <= self.r):  # отражение от стен
            self.x = self.r
            self.vx = int(-0.9 * self.vx)
        elif (self.x >= WIDTH - self.r):
            self.vx = int(-0.9 * self.vx)
            self.x = WIDTH - self.r
        if (self.y <= self.r):
            self.y = self.r
            self.vy = int(-0.9 * self.vy)
        elif (self.y >= HEIGHT - self.r):
            self.vy = int(-0.9 * self.vy)
            self.y = HEIGHT - self.r

        self.x += self.vx  # эволюция параметров
        self.y -= self.vy - (self.G) / 2
        self.vy -= self.G

        self.live -= 1  # снаряд постарел на 1 кадр

    def draw(self):
        pygame.draw.circle(
            self.screen, self.color,
            (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        distance = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5
        return (distance <= self.r + obj.r)


class Gun:
    def __init__(self, screen):
        '''Конструктор класса Gun
        '''
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Bullet(G, MAX_BALL_LIVES, self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if ((event.pos[0] - 20) != 0):
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
            else:
                self.an = -1 * math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(screen, self.color, (40, 450), (40 + (20 + self.f2_power) * math.cos(self.an),
                                                         450 + (20 + self.f2_power) * math.sin(self.an)), 5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface, TARGET_VELOCITY_RANGE=[]):
        '''Конструктор класса Target

        :param screen: экран
        :param TARGET_VELOCITY_RANGE: диапозон скоростей мишени
        '''
        self.x = rnd.randint(600, 780)
        self.y = rnd.randint(300, 550)
        self.r = rnd.randint(2, 50)
        self.color = RED
        self.screen = screen
        self.live = 1
        self.points = 0  # количество очков, набранное игроком
        self.vx = random.randint(TARGET_VELOCITY_RANGE[0], TARGET_VELOCITY_RANGE[1])
        self.vy = random.randint(TARGET_VELOCITY_RANGE[0], TARGET_VELOCITY_RANGE[1])

    def new_target(self, TARGET_VELOCITY_RANGE):
        """ Инициализация новой цели. """
        self.x = rnd.randint(600, 780)
        self.y = rnd.randint(300, 550)
        self.r = rnd.randint(2, 50)
        self.color = RED
        self.vx = random.randint(TARGET_VELOCITY_RANGE[0], TARGET_VELOCITY_RANGE[1])
        self.vy = random.randint(TARGET_VELOCITY_RANGE[0], TARGET_VELOCITY_RANGE[1])

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        """
        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        и стен по краям окна (размер окна 800х600).
        """

        if (self.x <= self.r):  # отражение от стен
            self.x = self.r
            self.vx = int(-0.9 * self.vx)
        elif (self.x >= WIDTH - self.r):
            self.vx = int(-0.9 * self.vx)
            self.x = WIDTH - self.r
        if (self.y <= self.r):
            self.y = self.r
            self.vy = int(-0.9 * self.vy)
        elif (self.y >= HEIGHT - self.r):
            self.vy = int(-0.9 * self.vy)
            self.y = HEIGHT - self.r

        self.x += self.vx  # эволюция параметров
        self.y -= self.vy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []  # здесь будут храниться экземпляры класса Ball

clock = pygame.time.Clock()
gun = Gun(screen)  # конструируем пушку
target = Target(screen, TARGET_VELOCITY_RANGE)  # конструируем первую цель
finished = False  # флажок, показывающий, что пора выходить из цикла

while not finished:
    screen.fill(WHITE)
    text1 = FONT_FOR_COUNTER.render(str(target.points), False, (0, 0, 0))  # задаём счётчик
    screen.blit(text1, (10, 10))  # отображаем счётчик
    # далее отрисовка объектов
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
        if (b.live <= 0):
            balls.remove(b)

    pygame.display.update()

    clock.tick(FPS)
    # обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверка на выход
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие на кнопку мыши
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:  # отпускание кнопки мыши
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:  # передвижение курсора
            gun.targetting(event)

    # перемещение объектов
    target.move()
    for b in balls:
        b.move()
        if b.hittest(target):  # проверка на попадание снарядом в цель
            target.hit()
            target.new_target(TARGET_VELOCITY_RANGE)
            balls.remove(b)
    gun.power_up()

pygame.quit()
