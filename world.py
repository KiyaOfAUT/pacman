import numpy as np
from pacman import Pacman
from ghost import Ghost
import os
import time


class WorldState:
    def __init__(self, pacman_p, ghost1_p, ghost2_p, test):
        self.state = self.State(np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
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
                                          [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]])
                                , pacman_p, ghost1_p, ghost2_p, 0)
        self.status = 2
        self.test = test
        self.pacman1 = None

    class State:
        def __init__(self, map_, pacman, ghost1, ghost2, score):
            self.map = map_
            self.pacman = pacman
            self.ghost1 = ghost1
            self.ghost2 = ghost2
            self.score = score

    def start(self):
        self.pacman1 = Pacman(self.state.pacman, self.state.map)
        ghost1 = Ghost(self.state.ghost1, self.state.map)
        ghost2 = Ghost(self.state.ghost2, self.state.map)
        self.update(self.pacman1.position, 1)
        while self.status == 2:
            # hold_pacman = self.pacman1.move(self.state)
            self.update(self.pacman1.move(self.state), 1)
            if not self.eval_game_status():
                return 0
            if self.eval_game_status() == 1:
                return 1
            hold_ghost1 = ghost1.move()
            self.update(hold_ghost1, 2)
            hold_ghost2 = ghost2.move()
            self.update(hold_ghost2, 3)
            if self.eval_game_status() == 2:
                pass
            else:
                return 0

    def update(self, position, agent):
        if agent == 1:
            if self.state.map[position[0]][position[1]] == 1:
                self.state.score = self.state.score + 5
                self.state.map[position[0]][position[1]] = 0
            else:
                self.state.score = self.state.score - 1
            self.state.pacman = position
        if agent == 2:
            self.state.ghost1 = position
        if agent == 3:
            self.state.ghost2 = position

    def print(self):
        position = [0, 0]
        for row in self.state.map:
            row_str = ""
            for house in row:
                if self.state.pacman == position:
                    if self.state.pacman == self.state.ghost1 or self.state.pacman == self.state.ghost2 or self.state.score < 0:
                        row_str += "☠️"
                    else:
                        row_str += "😃"
                elif self.state.ghost1 == position:
                    row_str += "👻"
                elif self.state.ghost2 == position:
                    row_str += "👻"
                elif house == -1:
                    row_str += "\033[94m" + '■' + "\033[0m" + " "
                elif house == 0:
                    row_str += "  "
                elif house == 1:
                    row_str += "\033[93m" + '•' + "\033[0m" + " "
                position = [position[0], position[1] + 1]
            print(row_str)
            position[1] = 0
            position = [position[0] + 1, position[1]]
        print("\n\n score: ", self.state.score)
        time.sleep(0.1)

    def eval_game_status(self):
        if self.state.pacman == self.state.ghost1 or self.state.pacman == self.state.ghost2 or self.state.score < 0:
            if not self.test:
                self.print()
                self.lost()
            return 0
        elif self.count_dots() == 0:
            if not self.test:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.print()
                self.won()
            return 1
        else:
            if not self.test:
                self.print()
                os.system('cls' if os.name == 'nt' else 'clear')
            return 2

    def count_dots(self):
        count = 0
        for i in self.state.map:
            for j in i:
                if j == 1:
                    count = count + 1
        return count

    def lost(self):
        color_red = "\033[91m"  # Red color
        color_reset = "\033[0m"  # Reset color to default
        letter_L = [
            "#       ",
            "#       ",
            "#       ",
            "#       ",
            "#       ",
            "#       ",
            "####### "
        ]

        letter_O = [
            " #####  ",
            "#     # ",
            "#     # ",
            "#     # ",
            "#     # ",
            "#     # ",
            " #####  "
        ]

        letter_S = [
            " #####  ",
            "#     # ",
            "#       ",
            " #####  ",
            "      # ",
            "#     # ",
            " #####  "
        ]

        letter_T = [
            "########",
            "   #    ",
            "   #    ",
            "   #    ",
            "   #    ",
            "   #    ",
            "   #    "
        ]

        letter_ = [
            "   #     ",
            "   #    ",
            "   #    ",
            "   #    ",
            "   #    ",
            "       ",
            "   #    "
        ]
        lost_text = [letter_L, letter_O, letter_S, letter_T, letter_]
        print("\n\n\n\n\n\n")
        for line in range(len(letter_L)):
            for letter in lost_text:
                print(color_red + letter[line] + "  " + color_reset, end="")
            print()
        print(self.pacman1.h)

    def won(self):
        # Define the word
        color_green = "\033[92m"  # Green color
        color_reset = "\033[0m"   # color reset

        letter_W = [
            "#       ##       # ",
            " #     #  #     #  ",
            "  #   #    #   #   ",
            "   # #      # #    ",
            "    #        #     ",
        ]

        letter_O = [
            " #####  ",
            "#     # ",
            "#     # ",
            "#     # ",
            " #####  "
        ]

        letter_N = [
            "#    # ",
            "##   # ",
            "# #  # ",
            "#  # # ",
            "#   ## "
        ]

        letter_ = [
            "   #     ",
            "   #    ",
            "   #    ",
            "       ",
            "   #    "
        ]

        lost_text = [letter_W, letter_O, letter_N, letter_]
        print("\n\n\n\n\n\n")
        for line in range(len(letter_W)):
            for letter in lost_text:
                print(color_green + letter[line] + "  " + color_reset, end="")
            print()
        print("\n\n\n\n\n\n")
