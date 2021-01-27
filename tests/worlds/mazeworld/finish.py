"""
Script that, given an environment (MazeWorld-FinishMazeSphere), will navigate the maze
"""


def navigate(env, callback):
    for _ in range(10):
        callback(env.step(0))

    for _ in range(4):
        callback(env.step(3))

    for _ in range(34):
        callback(env.step(0))

    for _ in range(6):
        callback(env.step(2))

    for _ in range(20):
        callback(env.step(0))

    for _ in range(5):
        callback(env.step(2))

    for _ in range(38):
        callback(env.step(0))

    for _ in range(7):
        callback(env.step(3))

    for _ in range(50):
        callback(env.step(0))

    for _ in range(9):
        callback(env.step(3))

    for _ in range(60):
        callback(env.step(0))

    for _ in range(9):
        callback(env.step(2))

    for _ in range(80):
        callback(env.step(0))

    for _ in range(9):
        callback(env.step(2))

    for _ in range(20):
        callback(env.step(0))

    for _ in range(9):
        callback(env.step(3))

    for _ in range(120):
        callback(env.step(0))

    for _ in range(9):
        callback(env.step(2))

    for _ in range(20):
        callback(env.step(0))
        