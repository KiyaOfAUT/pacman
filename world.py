import numpy as np
from pacman import Pacman
from ghost import Ghost
import os
import time


class WorldState:
    def __init__(self, pacman_p, ghost1_p, ghost2_p):
        self.state = self.State([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                                 [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
                                 [-1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1],
                                 [-1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1],
                                 [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
                                 [-1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1],
                                 [-1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1],
                                 [-1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, -1, -1],
                                 [-1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1],
                                 [-1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1],
                                 [-1, 1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1],
                                 [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
                                 [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
                                , pacman_p, ghost1_p, ghost2_p)
        self.dotsCount = self.count_dots()
        self.status = 2

    class State:
        def __init__(self, map_, pacman, ghost1, ghost2):
            self.map = map_
            self.pacman = pacman
            self.ghost1 = ghost1
            self.ghost2 = ghost2

    def update(self, pacman, ghost1, ghost2):
        if self.state.map[pacman[0]][pacman[1]] == 1:
            self.dotsCount = self.dotsCount + 1
        self.state.map[self.state.pacman[0]][self.state.pacman[1]] = 0
        self.state.pacman = pacman
        self.state.ghost1 = ghost1
        self.state.ghost2 = ghost2

    def start(self):
        pacman1 = Pacman(self.state.pacman, self.state.map)
        ghost1 = Ghost(self.state.ghost1, self.state.map)
        ghost2 = Ghost(self.state.ghost2, self.state.map)
        while self.status == 2:
            hold_pacman = pacman1.move(self.state)
            hold_ghost1 = ghost1.move()
            hold_ghost2 = ghost2.move()
            self.update(hold_pacman, hold_ghost1, hold_ghost2)
            self.eval_game_status()
            self.print()

    def print(self):
        position = [0, 0]
        for row in self.state.map:
            row_str = ""
            for house in row:
                if house == -1:
                    row_str += "# "
                elif house == 0:
                    row_str += "  "
                elif house == 1:
                    row_str += "o "
                elif self.state.pacman == position:
                    row_str += "P "
                elif self.state.ghost1 == position:
                    row_str += "G "
                elif self.state.ghost2 == position:
                    row_str += "G "
                position = [position[0] + 1, position[1]]
            print(row_str)
            position[0] = 0
            position = [position[0], position[1] + 1]

        time.sleep(10)
        os.system('cls' if os.name == 'nt' else 'clear')

    def eval_game_status(self):
        if self.state.pacman == self.state.ghost1 or self.state.pacman == self.state.ghost2:
            return 0
        elif self.count_dots() == 0:
            return 1
        else:
            return 2

    def count_dots(self):
        count = 0
        for i in self.state.map:
            for j in i:
                if j == 1:
                    count = count + 1
        return count
