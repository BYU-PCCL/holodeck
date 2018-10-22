"""
Arrow up/down for pitch.
Arrow left/right for roll.
Space to go up.
a/d to turn left/right.
"""

import argparse
import time

import pygame

from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_SPACE
from pygame.locals import K_UP
from pygame.locals import K_r
from pygame.locals import K_a
from pygame.locals import K_d

import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck.sensors import Sensors


class HolodeckGame(object):
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def execute(self):
        pygame.init()
        pygame.display.set_mode((1,1))

        self._on_new_episode()

        try:
            while all(e.type != pygame.QUIT for e in pygame.event.get()):
                self._on_loop()
        finally:
            pygame.quit()

    def _on_new_episode(self):
        self.agent.reset()

        self.env.reset()
        self.env.set_control_scheme('uav0', ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

    def _on_loop(self):
        states = self.env.tick()

        state = states['uav0']

        reward = state[Sensors.REWARD]
        location = state[Sensors.LOCATION_SENSOR]

        if state[Sensors.COLLISION_SENSOR]:
            print('ouch.')

        control = self.agent.act(state)

        if control is None:
            self._on_new_episode()
        else:
            self.env.act('uav0', control)


class ManualAgent(object):
    def __init__(self):
        self.control = None

        self.reset()

    def reset(self):
        self.control = np.array([0.0, 0.0, 0.0, 0.0])

    def act(self, state):
        return self._get_keyboard_control(pygame.key.get_pressed())

    def _get_keyboard_control(self, keys):
        if keys[K_r]:
            return None

        if keys[K_LEFT]:
            self.control[0] -= 0.1
        if keys[K_RIGHT]:
            self.control[0] += 0.1
        if keys[K_UP]:
            self.control[1] -= 0.08
        if keys[K_DOWN]:
            self.control[1] += 0.08
        if keys[K_a]:
            self.control[2] -= 0.2
        if keys[K_d]:
            self.control[2] += 0.2
        if keys[K_SPACE]:
            self.control[3] += 0.3

        self.control[0] /= 1.1
        self.control[1] /= 1.1
        self.control[2] /= 1.1
        self.control[3] /= 1.1

        return self.control


def main():
    env = holodeck.make('InfiniteForest')
    agent = ManualAgent()

    game = HolodeckGame(env, agent)
    game.execute()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye.')
