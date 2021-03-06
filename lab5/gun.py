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
MAX_BULLET_LIVES = 80  # время жизни снаряда в кадрах
LASER_LIFETIME = 4  # время отображения лазера
G = 2  # аналог ускорения свободного падения
WIDTH = 800  # параметры экрана
HEIGHT = 600


class Laser:
    def __init__(self, screen):
        '''
        конструктор класса Laser
        self.start_coords - координаты начала лазерного луча
        self.angle - угол, под которым распространяется луч
        '''
        self.screen = screen
        self.start_coords = [0, 0]
        self.angle = 1
        self.live = LASER_LIFETIME

    def draw(self):
        pygame.draw.line(self.screen, RED, self.start_coords,
                         [WIDTH, self.start_coords[1] + ((WIDTH - self.start_coords[0]) * math.tan(self.angle))], 3)


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


class Gun:
    def __init__(self, screen):
        '''Конструктор класса Gun
        '''
        self.screen = screen
        self.fire_power = 10  # мощность выстрела
        self.is_targetting = 0  # флажок, показывающий, началось ли прицеливание
        self.angle = 1  # угол с горизонтом под которым находится дуло пушки
        self.color = GREY

    def fire2(self):
        lasershot = Laser(self.screen)
        lasershot.angle = self.angle
        lasershot.start_coords = [40, 450]
        return lasershot

    def fire1_start(self):
        self.is_targetting = 1

    def fire1_end(self, mouseposision=[]):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_bullet = Bullet(G, MAX_BULLET_LIVES, self.screen)
        self.angle = math.atan2((mouseposision[1] - new_bullet.y), (mouseposision[0] - new_bullet.x))
        new_bullet.vx = self.fire_power * math.cos(self.angle)
        new_bullet.vy = - self.fire_power * math.sin(self.angle)
        self.is_targetting = 0
        self.fire_power = 10
        return new_bullet

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
        self.r = rnd.randint(15, 50)
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
        self.lasershot = Laser(self.screen)
        self.lasershot.live = 0

    def hittest_bullet_target(self):
        '''проверяет поражезние цели шариком, перебирая весь массив bullets
        '''
        for bullet in self.bullets:
            distance = ((bullet.x - self.target.x) ** 2 + (bullet.y - self.target.y) ** 2) ** 0.5
            if (distance <= self.target.r + bullet.r):
                return True
        return False

    def hittest_laser_target(self):
        '''
        проверка на поражение цели лазером
        '''
        n = [math.tan(self.lasershot.angle), -1]  # вектор нормали к лазерному лучу
        # найдём расстояние через скалярное произведение вектора нормали на радиусвектор мишени в СО с началом в пушке
        distance = abs((n[0] * (self.target.x - self.lasershot.start_coords[0])
                        + n[1] * (self.target.y - self.lasershot.start_coords[1]))) / ((n[1] ** 2 + n[0] ** 2) ** 0.5)
        return (distance <= self.target.r)

    def mainloop(self):
        while not self.finished:
            self.screen.fill(WHITE)
            text1 = self.FONT_FOR_COUNTER.render(str(self.scores), False, (0, 0, 0))  # задаём счётчик
            self.screen.blit(text1, (10, 10))  # отображаем счётчик
            # далее отрисовка объектов
            self.gun.draw()
            self.target.draw()
            if (self.lasershot.live > 0):
                self.lasershot.draw()
                self.lasershot.live -= 1
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
                    if (event.button == 1):
                        self.gun.fire1_start()
                    elif (event.button == 3):
                        self.lasershot = self.gun.fire2()
                elif event.type == pygame.MOUSEBUTTONUP:  # отпускание кнопки мыши
                    if (event.button == 1):
                        self.bullets.append(self.gun.fire1_end((event.pos[0], event.pos[1])))
                elif event.type == pygame.MOUSEMOTION:  # передвижение курсора
                    self.gun.targetting((event.pos[0], event.pos[1]))

            # перемещение объектов
            self.target.move()
            for b in self.bullets:
                b.move()
            if (self.hittest_laser_target() and self.lasershot.live > 0):
                self.scores += TARGET_SCORES
                self.target.new_target(TARGET_VELOCITY_RANGE)
            elif self.hittest_bullet_target():
                self.scores += TARGET_SCORES
                self.target.new_target(TARGET_VELOCITY_RANGE)
                self.bullets.remove(b)
            self.gun.power_up()
        pygame.quit()


game = Game_manager()
game.mainloop()
