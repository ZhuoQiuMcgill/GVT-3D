from Vertex import *
import numpy as np


class Edge:
    def __init__(self, he1, he2):
        self.he1 = he1  # 一个方向的半边
        self.he2 = he2  # 另一个方向的半边

    def __str__(self):
        return f"Edge({self.he1}, {self.he2})"
