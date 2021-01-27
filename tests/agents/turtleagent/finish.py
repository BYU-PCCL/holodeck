"""
Script that will navigate the "maze" in testworld
"""


def navigate(env, callback):

    for _ in range(100):
        callback(env.step([0, 0]))

    for _ in range(11):
        callback(env.step([0, -30]))

    for _ in range(10):
        callback(env.step([0, 0]))

    for _ in range(123):
        callback(env.step([80, 0]))

    for _ in range(26):
        callback(env.step([0, 0]))

    for _ in range(10):
        callback(env.step([0, 30]))

    for _ in range(100):
        callback(env.step([150, 0]))

    for _ in range(100):
        callback(env.step([0, 0]))

    for _ in range(10):
        callback(env.step([0, 30]))

    for _ in range(7):
        callback(env.step([0, 0]))

    for _ in range(100):
        callback(env.step([100, 0]))

    for _ in range(30):
        callback(env.step([0, 0]))
