import numpy as np
import argparse
import igl
import polyscope as ps
from Mesh import Mesh
import random
import keyboard

POINT_COLOR = (0.2, 0.2, 0.2)
POINT_RADIUS = 0.005
EDGE_COLOR = (0.2, 0.2, 0.2)
EDGE_RADIUS = 0.0025

RED = (1.0, 0.0, 0.0)
BACKGROUND_COLOR = (0.0, 0.0, 0.0)
GROUND_PLANE_MODE = 'none'
SSAA_FACTOR = 4

DATA_DIR = 'data'
DATA_FILE = 'icosphere.obj'

DIFFUSE_POINT_CLOUD_REGISTERED = False
DIFFUSE_CURVE_NETWORK_REGISTERED = False

RUNNING = True
MESH = None
CURRENT_EDGE = None


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default=DATA_DIR + "/" + DATA_FILE)
    args = parser.parse_args()

    # 从.obj文件中读取顶点和面
    V, _, _, F, _, _ = igl.read_obj(args.file)

    # 准备网络数据
    mesh = Mesh(V, F)
    print(mesh)

    global MESH
    MESH = mesh

    # 初始化
    init_ps()
    init_keyboard_setting()
    init_mesh(mesh)

    # 主程序
    while RUNNING:
        ps.frame_tick()

    clear_keyboard_setting()


def on_esc_press():
    global RUNNING
    RUNNING = False


def on_r_press():
    global CURRENT_EDGE, MESH
    if MESH is not None:
        CURRENT_EDGE = MESH.select_random_edge()
        render_half_edge(CURRENT_EDGE)


def on_a_press():
    global CURRENT_EDGE

    if CURRENT_EDGE is not None:
        CURRENT_EDGE = CURRENT_EDGE.prev
        render_half_edge(CURRENT_EDGE)


def on_d_press():
    global CURRENT_EDGE

    if CURRENT_EDGE is not None:
        CURRENT_EDGE = CURRENT_EDGE.next
        render_half_edge(CURRENT_EDGE)


def on_space_press():
    global CURRENT_EDGE

    if CURRENT_EDGE is not None:
        CURRENT_EDGE = CURRENT_EDGE.opposite
        render_half_edge(CURRENT_EDGE)


def init_keyboard_setting():
    keyboard.add_hotkey('esc', on_esc_press)
    keyboard.add_hotkey('r', on_r_press)
    keyboard.add_hotkey('d', on_d_press)
    keyboard.add_hotkey('a', on_a_press)
    keyboard.add_hotkey('space', on_space_press)


def clear_keyboard_setting():
    keyboard.clear_hotkey('esc')
    keyboard.clear_hotkey('r')


def init_ps():
    ps.set_program_name("GVT-3D")
    ps.init()
    ps.set_background_color(BACKGROUND_COLOR)
    ps.set_ground_plane_mode(GROUND_PLANE_MODE)
    ps.set_SSAA_factor(SSAA_FACTOR)


def init_mesh(mesh):
    edges = mesh.get_all_edges()
    vertices = mesh.get_all_vertices()

    print(vertices)

    point_cloud = ps.register_point_cloud("Original Vertices", vertices)
    point_cloud.set_color(POINT_COLOR)
    point_cloud.set_radius(POINT_RADIUS)

    curve_network = ps.register_curve_network("Original Edges", vertices, edges)
    curve_network.set_color(EDGE_COLOR)
    curve_network.set_radius(EDGE_RADIUS)


def render_half_edge(halfedge):
    vertices = halfedge.get_vertices()
    head = halfedge.vertex.get_position()

    point_cloud = ps.register_point_cloud("Head Vertex", np.array([head]))
    point_cloud.set_color(RED)
    point_cloud.set_radius(POINT_RADIUS * 2)

    curve_network = ps.register_curve_network("Half Edges", vertices, np.array([[0, 1]]))
    curve_network.set_color(RED)
    curve_network.set_radius(EDGE_RADIUS * 1.2)

    print(halfedge.length())


if __name__ == "__main__":
    main()
