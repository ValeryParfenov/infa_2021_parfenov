import pygame
from pygame.draw import *

# рисование

p = 3.14
fps = 1
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((450, 650))

brown_wall = (102, 77, 0)
brown_floor = (153, 115, 0)
cat_body_color = (255, 133, 51)
cat_ear_color = (255, 217, 179)
black = (40, 40, 40)  # зрачки кошки (в том числе)
cat_eye_color = (136, 204, 0)
window_glass_color = (51, 153, 255)
window_joint_color = (230, 238, 255)
ball_calor = (179, 179, 204)
blick_calor = (255, 255, 255)
mustache_calor = (153, 102, 0)
# здесь будут рисоваться фигуры
# стена + пол
rect(screen, brown_wall, (0, 0, 450, 300))
rect(screen, brown_floor, (0, 300, 450, 350))
# окно
rect(screen, window_joint_color, (245, 20, 200, 270))  # рама
rect(screen, window_glass_color, (255, 27, 83, 70))  # лев верх
rect(screen, window_glass_color, (352, 27, 83, 70))  # прав верх
rect(screen, window_glass_color, (255, 115, 83, 166))  # лев низ
rect(screen, window_glass_color, (352, 115, 83, 166))  # прав низ
# кот
# тело
ellipse(screen, cat_body_color, (33, 376, 36, 70))  # левая верхняя лапка
ellipse(screen, black, (33, 376, 36, 70), 1)

circle(screen, cat_body_color, (335, 360), 25) # хвост
circle(screen, black, (335, 360), 25, 1)

ellipse(screen, cat_body_color, (60, 320, 290, 145))  # тело
ellipse(screen, black, (60, 320, 290, 145), 1)

ellipse(screen, cat_body_color, (66, 428, 70, 38))  # левая нижняя лапка
ellipse(screen, black, (66, 428, 70, 38), 1)

circle(screen, cat_body_color, (325, 420), 39)  # правая лапка
circle(screen, black, (325, 420), 39, 1)
ellipse(screen, cat_body_color, (342, 431, 30, 62))
ellipse(screen, black, (342, 431, 30, 62), 1)
# голова
circle(screen, cat_body_color, (70, 375), 55)
circle(screen, black, (70, 375), 55, 1)

circle(screen, cat_eye_color, (49, 377), 15)  # глаза
circle(screen, cat_eye_color, (94, 377), 15)

# блики

ellipse(screen, black, (50, 369, 4, 21))  # зрачки
ellipse(screen, black, (94, 369, 4, 21))

polygon(screen, cat_body_color, [[45, 330], [22, 354], [22, 305]])  # левое ухо
polygon(screen, black, [[45, 330], [22, 354], [22, 305]], 1)
polygon(screen, cat_ear_color, [[40, 330], [27, 345], [26, 315]])

polygon(screen, cat_body_color, [[98, 333], [119, 359], [119, 309]])  # правое ухо
polygon(screen, black, [[98, 333], [119, 359], [119, 309]], 1)
polygon(screen, cat_ear_color, [[103, 333], [115, 349], [115, 320]])

polygon(screen, cat_ear_color, [[66, 395], [76, 395], [71, 402]]) # нос

aaline(screen, mustache_calor, [80,403], [130,390])
aaline(screen, mustache_calor, [82,405], [135,400])
aaline(screen, mustache_calor, [79,408], [128,414])
aaline(screen, mustache_calor, [63,403], [10,390])
aaline(screen, mustache_calor, [62,405], [5,400])
aaline(screen, mustache_calor, [66,408], [8,414])

# клубок
circle(screen, ball_calor, (290, 550), 40)
circle(screen, black, (290, 550), 40, 1)
arc(screen, black, (285, 535, 30, 30), -p / 4, p * 3 / 7)
arc(screen, black, (288, 532, 34, 34), -p * 1.12 / 4, p * 1.12 * 3 / 7)
arc(screen, black, (278, 564, 30, 30), p / 2, p)
arc(screen, black, (273, 559, 30, 30), p / 2, p)
arc(screen, black, (260, 530, 30, 30), p * 1.5 / 3, p * 3.5 / 3)

pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    clock.tick(fps)
