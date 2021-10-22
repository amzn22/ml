import pygame
import random
import numpy as np


class Point():
    def __init__(self, x, y, color=(0, 0, 0), cluster=-1):
        self.x = x
        self.y = y
        self.color = color
        self.cluster = cluster


def add_points(point):
    points.append(Point(point[0], point[1]))
    k = random.randint(1, 4)
    for i in range(k):
        d = random.randint(2 * r, 5 * r)
        alpha = random.random() * np.pi
        x_new = point[0] + d * np.sin(alpha)
        y_new = point[1] + d * np.cos(alpha)
        points.append(Point(x_new, y_new))


def pygame_draw():
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    screen.fill('WHITE')
    pygame.display.update()
    FPS = 30
    clock = pygame.time.Clock()
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    add_points(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    set_colors()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    find_clusters()
                    paint_points_by_cluster()
        screen.fill('WHITE')
        for point in points:
            pygame.draw.circle(screen, point.color, (point.x, point.y), r)
        pygame.display.update()
        clock.tick(FPS)


def set_colors():
    for i in range(len(points)):
        neighb = 0
        for j in range(len(points)):
            if i != j:
                if dist(points[i], points[j]) <= eps:
                    neighb += 1
        if neighb >= minPts:
            points[i].color = (0, 255, 0)
    for i in range(len(points)):
        if points[i].color != (0, 255, 0):
            for j in range(len(points)):
                if points[j].color == (0, 255, 0):
                    if dist(points[i], points[j]) <= eps:
                        points[i].color = (255, 165, 0)
    for i in range(len(points)):
        if points[i].color != (0, 255, 0):
            if points[i].color != (255, 165, 0):
                points[i].color = (255, 0, 0)


def join_green_points(point, excluded_points):
    for point_ch in points:
        if (point_ch not in excluded_points) and (point_ch.color == (0, 255, 0)) and (dist(point_ch, point) <= eps):
            point_ch.cluster = point.cluster
            new_excluded_points = excluded_points.copy()
            new_excluded_points.append(point_ch)
            join_green_points(point_ch, new_excluded_points)


def find_nearest_green(point_orange):
    greens = []
    minGreen = None
    minDist = 123123
    for point in points:
        if (point.color == (0, 255, 0)) and (dist(point_orange,point)<=eps):
            greens.append(point)
    for green in greens:
        if dist(green,point_orange)<minDist:
            minDist = dist(green,point_orange)
            minGreen = green
    return minGreen

def find_clusters():
    cluster_count = 0
    for point in points:
        if (point.color == (0, 255, 0)) and (point.cluster == -1):
            point.cluster = cluster_count
            excluded_points = [point]
            join_green_points(point, excluded_points)
            cluster_count += 1
    for point in points:
        if (point.color == (255, 165, 0)) and (point.cluster == -1):
            nearest_green = find_nearest_green(point)
            point.cluster = nearest_green.cluster


def paint_points_by_cluster():
    clusters = set(list(map(lambda p: p.cluster, points)))
    colorss = []
    for i in range(len(clusters)):
        colorss.append(np.random.choice(range(256), size=3))
    for point in points:
        if point.cluster == -1:
            point.color = 'black'
        else:
            point.color = colorss[point.cluster]


def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


if __name__ == "__main__":
    points = []
    r = 4
    minPts, eps = 3, 15
    pygame_draw()
