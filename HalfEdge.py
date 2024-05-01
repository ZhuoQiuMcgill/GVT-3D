import numpy as np


class HalfEdge:
    def __init__(self):
        self.vertex = None  # 该半边指向的顶点（半边的终点）
        self.opposite = None  # 相对的半边
        self.next = None  # 下一个半边
        self.face = None  # 该半边所属的面

    def __str__(self):
        return f"HalfEdge(to {self.vertex})"

    def get_vertices(self):
        return np.array([self.vertex.get_position(), self.opposite.vertex.get_position()])

    def length(self):
        return np.linalg.norm(self.vertex.get_position() - self.opposite.vertex.get_position())

