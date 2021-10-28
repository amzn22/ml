import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

matrix = np.zeros((5, 5))
iso = 5


class Point:
    def __init__(self, x, y, cluster=-1, isolated=True, connected=None):
        self.x = x
        self.y = y
        self.cluster = cluster
        self.isolated = isolated
        self.connected = connected or set()


def show_points(points, title=None):
    clusters = set(list(map(lambda p: p.cluster, points)))
    colors = cm.rainbow(np.linspace(0, 1, len(clusters)))
    plt.scatter(
        list(map(lambda p: p.x, points)),
        list(map(lambda p: p.y, points)),
        color=list(map(lambda p: colors[p.cluster], points)),
    )
    for i in range(len(points)):
        for conn in points[i].connected:
            plt.plot([points[i].x, points[conn].x], [points[i].y, points[conn].y])

    plt.title(title)
    plt.show()
    plt.close()


def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def rand_points(n):
    points = []
    for i in range(n):
        point = Point(np.random.randint(0, 100), np.random.randint(0, 100))
        points.append(point)
    return points


def fill_matrix(points):
    for i in range(len(points)):
        for j in range(len(points)):
            if i == j:
                matrix[i][i] = 1000
            else:
                matrix[i][j] = dist(points[i], points[j])


def find_min_and_connect(points):
    i_i = 0
    j_j = 0
    min = 10000
    for i in range(len(points)):
        for j in range(len(points)):
            if matrix[i][j] < min:
                min = matrix[i][j]
                i_i = i
                j_j = j

    global iso
    iso -= 2
    points[i_i].connected.add(j_j)
    points[j_j].connected.add(i_i)
    points[i_i].isolated = False
    points[j_j].isolated = False


def find_other_points_and_connect(points):
    global iso
    while (iso != 0):
        for i in range(len(points)):
            if (points[i].isolated == False):
                min = 10000
                minpoint_indx = -20
                for j in range(len(points)):
                    if (points[j].isolated == True) and (dist(points[i], points[j]) < min):
                        min = dist(points[i], points[j])
                        minpoint_indx = j

                if minpoint_indx != -20:
                    points[minpoint_indx].isolated = False
                    iso -= 1
                    points[minpoint_indx].connected.add(i)
                    points[i].connected.add(minpoint_indx)
    show_points(points)


def find_max_and_remove(points):
    max = 0
    i_i = -1
    j_j = -1
    for i in range(len(points)):
        for conn in points[i].connected:
            if dist(points[i], points[conn]) > max:
                i_i = i
                j_j = conn
                max = dist(points[i], points[conn])
    points[i_i].connected.remove(j_j)
    points[j_j].connected.remove(i_i)
    show_points(points)


def find_point_cluster_spread_on_connected(point_index, cluster, points):
    points[point_index].cluster = cluster
    for i in range(len(points[point_index].connected)):
        current = points[point_index].connected.pop()
        points[current].cluster = cluster
        points[current].connected.remove(point_index)
        find_point_cluster_spread_on_connected(current, cluster, points)


def devide_points_on_clusters(points):
    clst = 0
    for j in range(len(points)):
        if points[j].cluster == -1:
            find_point_cluster_spread_on_connected(j, clst, points)
            clst += 1
    show_points(points)


def devide_on_clusters(clusters, points):
    clusters_real = clusters - 1
    for i in range(clusters_real):
        find_max_and_remove(points)
    devide_points_on_clusters(points)


def print_points(points):
    for i in range(len(points)):
        print(i, points[i].connected, points[i].cluster)


if __name__ == "__main__":
    points = rand_points(5)
    fill_matrix(points)
    print(matrix)
    find_min_and_connect(points)
    find_other_points_and_connect(points)
    devide_on_clusters(2, points)
    print_points(points)
    show_points(points)
