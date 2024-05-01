import numpy as np


class Vertex:
    def __init__(self, x, y, z):
        self.x = x  # x坐标
        self.y = y  # y坐标
        self.z = z  # z坐标
        self.halfedge = None  # 指向一个以该顶点为起点的半边

    def __str__(self):
        return f"Vertex({self.x}, {self.y}, {self.z})"

    def get_position(self):
        return np.array([self.x, self.y, self.z])

    @staticmethod
    def subtract(v1, v2):
        return np.array([v1.x - v2.x, v1.y - v2.y, v1.z - v2.z])

    @staticmethod
    def add(v1, v2):
        return np.array([v1.x + v2.x, v1.y + v2.y, v1.z + v2.z])

    @staticmethod
    def center(vertices):
        total_x = 0
        total_y = 0
        total_z = 0
        count = 0
        for vertex in vertices:
            total_x += vertex.x
            total_y += vertex.y
            total_z += vertex.z
            count += 1

        if count == 0:
            return np.array([0, 0, 0])
        return np.array([total_x / count, total_y / count, total_z / count])
