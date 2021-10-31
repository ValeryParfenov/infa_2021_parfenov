import math
import random
import random as rnd
from random import choice
import pygame

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
TARGET_SCORES = 1  # Количество очков, даваемое за цель класса Target
TARGET_VELOCITY_RANGE = [5, 30]  # диапозон скоростей мишени
FPS = 30
MAX_BALL_LIVES = 80  # время жизни снаряда в кадрах
G = 2  # аналог ускорения свободного падения
WIDTH = 800  # параметры экрана
HEIGHT = 600


class Bullet:
    def __init__(self, G, MAX_BULLET_LIVES, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса Bullet
        x - начальное положение снаряда по горизонтали
        y - начальное положение снаряда по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 15
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
        self.fire_power = 10 # мощность выстрела
        self.is_targetting = 0 # флажок, показывающий, началось ли прицеливание
        self.angle = 1 # угол с горизонтом под которым находится дуло пушки
        self.color = GREY

    def fire2_start(self):
        self.is_targetting = 1

    def fire2_end(self, mouseposision=[]):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Bullet(G, MAX_BALL_LIVES, self.screen)
        self.angle = math.atan2((mouseposision[1] - new_ball.y), (mouseposision[0] - new_ball.x))
        new_ball.vx = self.fire_power * math.cos(self.angle)
        new_ball.vy = - self.fire_power * math.sin(self.angle)
        self.is_targetting = 0
        self.fire_power = 10
        return new_ball

    def targetting(self, mouseposision=[]):
        """Прицеливание. Зависит от положения мыши."""
        if ((mouseposision[0] - 20) != 0):
            self.angle = math.atan((mouseposision[1] - 450) / (mouseposision[0] - 20))
        else:
            self.angle = -1 * math.pi / 2

    def draw(self):
        pygame.draw.line(self.screen, self.color, (40, 450), (40 + (20 + self.fire_power) * math.cos(self.angle),
                                                              450 + (20 + self.fire_power) * math.sin(self.angle)), 5)

    def power_up(self):
        '''Накапливает силу выстрела при зажатой кнопке, делает цвет пушки красным при зажатой кнопке
        '''
        if self.is_targetting:
            if self.fire_power < 100:
                self.fire_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface, TARGET_VELOCITY_RANGE=[]):
        '''Конструктор класса Target
        Создаёт мишень в случайном месте экрана, со случайной скоростью из диапозона
        :param screen: экран
        :param TARGET_VELOCITY_RANGE: диапозон скоростей мишени
        '''
        self.x = rnd.randint(600, 780)
        self.y = rnd.randint(300, 550)
        self.r = rnd.randint(15, 50)
        self.color = RED
        self.screen = screen
        self.live = 1
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


class Game_manager():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.FONT_FOR_COUNTER = pygame.font.Font(None, 40)
        self.bullets = []  # здесь будут храниться экземпляры класса Bullet

        self.clock = pygame.time.Clock()
        self.gun = Gun(self.screen)  # конструируем пушку
        self.target = Target(self.screen, TARGET_VELOCITY_RANGE)  # конструируем первую цель
        self.finished = False  # флажок, показывающий, что пора выходить из цикла
        self.scores = 0

    def mainloop(self):
        while not self.finished:
            self.screen.fill(WHITE)
            text1 = self.FONT_FOR_COUNTER.render(str(self.scores), False, (0, 0, 0))  # задаём счётчик
            self.screen.blit(text1, (10, 10))  # отображаем счётчик
            # далее отрисовка объектов
            self.gun.draw()
            self.target.draw()
            for b in self.bullets:
                b.draw()
                if (b.live <= 0):
                    self.bullets.remove(b)

            pygame.display.update()

            self.clock.tick(FPS)
            # обрабатываем события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # проверка на выход
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие на кнопку мыши
                    self.gun.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:  # отпускание кнопки мыши
                    self.bullets.append(self.gun.fire2_end((event.pos[0], event.pos[1])))
                elif event.type == pygame.MOUSEMOTION:  # передвижение курсора
                    self.gun.targetting((event.pos[0], event.pos[1]))

            # перемещение объектов
            self.target.move()
            for b in self.bullets:
                b.move()
                if b.hittest(self.target):  # проверка на попадание снарядом в цель
                    self.scores += TARGET_SCORES
                    self.target.new_target(TARGET_VELOCITY_RANGE)
                    self.bullets.remove(b)
            self.gun.power_up()
        pygame.quit()


game = Game_manager()
game.mainloop()
