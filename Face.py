import numpy as np

from Vertex import Vertex


class Face:
    def __init__(self):
        self.halfedge = None  # 指向构成该面的任意一个半边

    def normal(self):
        # 获取三个顶点
        v1 = self.halfedge.vertex
        v2 = self.halfedge.next.vertex
        v3 = self.halfedge.next.next.vertex

        # 计算两个向量
        vec1 = Vertex.subtract(v2, v1)
        vec2 = Vertex.subtract(v3, v1)

        # 计算叉积
        normal_vector = np.cross(vec1, vec2)

        # 归一化法线向量
        norm = np.linalg.norm(normal_vector)
        if norm == 0:
            return normal_vector  # 避免除零错误
        return normal_vector / norm

    def __str__(self):
        return "Face"

    def generate_next_vertex(self):
        vertices = [self.halfedge.vertex]
        edge_count = 1
        total_length = self.halfedge.length()
        halfedge = self.halfedge.next
        while halfedge != self.halfedge:
            total_length += halfedge.length()
            vertices.append(halfedge.vertex)
            edge_count += 1
            halfedge = halfedge.next

        avg_length = total_length / edge_count
        center = Vertex.center(vertices)
        normal = self.normal()

        new_position = center - normal * avg_length
        return Vertex(new_position[0], new_position[1], new_position[2])


