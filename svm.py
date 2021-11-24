import numpy as np
import pygame
from dataclasses import dataclass
import random
from sklearn import svm

DEFAULT_COLOR = "black"
RED = "red"
BLUE = "blue"

colors = {0: RED, 1: BLUE}

@dataclass
class Point:
    x: int
    y: int
    cluster: int
    color: str

def generate_random_points_near_target(point: Point, n: int, r: int = 4):
    new_points = []

    new_points.append(point)

    k = random.randint(0, n)

    for i in range(k):
        d = random.randint(2 * r, 5 * r)
        alpha = random.random() * 2 * np.pi
        x_new = point.x + d * np.sin(alpha)
        y_new = point.y + d * np.cos(alpha)
        new_points.append(Point(x_new, y_new, point.cluster, point.color))

    return new_points

def change_cluster(points, cluster):
    for point in points:
        point.color = colors[cluster]
        point.cluster = cluster

def draw_pygame(points):
    pygame.init()

    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    play = True

    new_points = []
    predicted_points = []

    past_len_points = len(points)
    red_cluster_n = 0
    blue_cluster_n = 0

    clf = None

    while play:

        screen.fill('WHITE')

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                play = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_points = generate_random_points_near_target(Point(event.pos[0], event.pos[1], -1, DEFAULT_COLOR), 5)
                if event.button == 3:

                    if blue_cluster_n == 0 or red_cluster_n == 0:
                        print("Тренировочный датасет должен содержать хотя бы по одной точке для двух кластеров")

                    else:
                        p = Point(event.pos[0], event.pos[1], -1, DEFAULT_COLOR)
                        # обучаем модель только если кол-во тренировочных точек изменилось с последнего момента обучения
                        if past_len_points != len(points):
                            clf = svm.SVC(kernel='linear')

                            clf.fit([(p.x, p.y) for p in points], [p.cluster for p in points])

                            past_len_points = len(points)

                        y_pred = clf.predict([(p.x, p.y)])
                        p.cluster = y_pred[0]
                        p.color = colors[y_pred[0]]
                        predicted_points.append(p)

            # Назначаем цвет и кластер для точки
            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_r and event.key != pygame.K_b:
                    print("Команда не найдена, попробуйте еще раз")
                else:
                    # Клавиша R - 0 класс и красный цвет
                    if event.key == pygame.K_r:
                        change_cluster(new_points, 0)
                        red_cluster_n += 1
                    # Клавиша R - 1 класс и синий цвет
                    if event.key == pygame.K_b:
                        change_cluster(new_points, 1)
                        blue_cluster_n += 1
                    points.extend(new_points)
                    new_points = None

        for point in points:
            pygame.draw.circle(screen, point.color, (point.x, point.y), 5)

        if new_points is not None:
            for point in new_points:
                pygame.draw.circle(screen, point.color, (point.x, point.y), 5)

        for point in predicted_points:
            pygame.draw.circle(screen, point.color, (point.x, point.y), 5)

        pygame.display.update()

if __name__ == "__main__":
    points = []

    draw_pygame(points)