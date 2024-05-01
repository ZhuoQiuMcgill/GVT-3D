from Face import Face
from Edge import Edge
from HalfEdge import HalfEdge
from Vertex import Vertex
import numpy as np
import random


class Mesh:
    def __init__(self, vertices, faces):
        self.vertices = [Vertex(x, y, z) for x, y, z in vertices]
        self.faces = []
        self.halfedges = {}

        self.build_faces(faces)
        self.link_halfedges()

    def build_faces(self, faces):
        for face_indices in faces:
            face = Face()
            self.faces.append(face)
            first_halfedge = None
            last_halfedge = None

            num_vertices = len(face_indices)
            for i in range(num_vertices):
                start_vertex_index = face_indices[i]
                end_vertex_index = face_indices[(i + 1) % num_vertices]
                start_vertex = self.vertices[start_vertex_index]
                end_vertex = self.vertices[end_vertex_index]

                halfedge = HalfEdge()
                halfedge.vertex = end_vertex
                halfedge.face = face

                if first_halfedge is None:
                    first_halfedge = halfedge
                if last_halfedge is not None:
                    last_halfedge.next = halfedge
                last_halfedge = halfedge

                self.halfedges[(start_vertex_index, end_vertex_index)] = halfedge

                if start_vertex.halfedge is None:
                    start_vertex.halfedge = halfedge

            last_halfedge.next = first_halfedge
            face.halfedge = first_halfedge

    def get_all_edges(self):
        edge_set = set()
        for halfedge_key, halfedge in self.halfedges.items():
            start_vertex_index = self.vertices.index(halfedge.vertex)
            end_vertex_index = self.vertices.index(halfedge.next.vertex)
            if (end_vertex_index, start_vertex_index) not in edge_set:
                edge_set.add((start_vertex_index, end_vertex_index))
        return np.array(list(edge_set), dtype=np.int32)

    def get_all_vertices(self):
        vertices_array = [(vertex.x, vertex.y, vertex.z) for vertex in self.vertices]
        return np.array(vertices_array, dtype=np.float32)

    def select_random_edge(self):
        return random.choice(list(self.halfedges.values()))

    def link_halfedges(self):
        # Link opposite and previous halfedges
        for key, halfedge in self.halfedges.items():
            # Set twin (opposite) halfedges
            opposite_key = (key[1], key[0])
            if opposite_key in self.halfedges:
                halfedge.opposite = self.halfedges[opposite_key]

            # Set previous halfedges
            # Previous halfedge of the current halfedge's next is the current halfedge
            if halfedge.next:  # Ensure next is not None
                halfedge.next.prev = halfedge

    def __str__(self):
        return f"Mesh with {len(self.vertices)} vertices and {len(self.faces)} faces"
