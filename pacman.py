import copy
import random
import numpy as np
import time


class Pacman:
    def __init__(self, position, map_):
        self.map = copy.copy(map_)
        self.position = position
        self.eaten_points = 0
        self.h = 0
        self.score = 0
        self.hold = 0

    def move(self, current_state):
        depth = 4
        map_ = copy.copy(current_state.map)
        max_ = float('-inf')
        pos_ = current_state.pacman
        state_ = self.State(current_state.pacman, current_state.ghost1, current_state.ghost2, map_, current_state.score)
        for i in (state_.eval_available_moves(current_state.pacman)):
            state = self.State(current_state.pacman, current_state.ghost1, current_state.ghost2, map_, current_state.score)
            if map_[i[0]][i[1]] == 1:
                state.score = state.score + 5
            else:
                state.score = state.score - 1
            state.map[i[0], i[1]] = 0
            state.pacman = [i[0], i[1]]
            hold = self.minimax(2, 1, depth, state)
            # print([i[0], i[1]], ":", hold)
            if hold > max_:
                max_ = hold
                pos_ = i
        return pos_

    def minimax(self, agent, current_depth, depth, state):
        status = state.won_or_lost()
        if status == 0:
            return float('-inf')
        if status == 1:
            return float('+inf')
        if current_depth == depth:
            return state.e_utility()
        if agent == 1:
            max_value = float('-inf')
            for i in state.eval_available_moves(state.pacman):
                hold = self.minimax(2, current_depth + 1, depth, self.new_state(state, 0, copy.copy(i)))
                if max_value < hold:
                    max_value = hold
            return max_value
        if agent == 2:
            min_value = float('+inf')
            for i in state.eval_available_moves(state.ghost1):
                hold = self.minimax(3, current_depth + 1, depth, self.new_state(state, 1, copy.copy(i)))
                if hold < min_value:
                    min_value = hold
            return min_value
        if agent == 3:
            min_value = float('+inf')
            for i in state.eval_available_moves(state.ghost2):
                hold = self.minimax(1, current_depth + 1, depth, self.new_state(state, 2, copy.copy(i)))
                if hold < min_value:
                    min_value = hold
            return min_value

    def new_state(self, state, agent, new_position):
        map_ = copy.copy(state.map)
        if agent == 1:
            new_state_ = self.State(copy.copy(state.pacman), new_position, copy.copy(state.ghost2), map_, state.score)
        elif agent == 2:
            new_state_ = self.State(copy.copy(state.pacman), copy.copy(state.ghost1), new_position, map_, state.score)
        else:
            if map_[new_position[0]][new_position[1]] == 1:
                score = state.score + 5
            else:
                score = state.score - 1
            map_[new_position[0]][new_position[1]] = 0
            new_state_ = self.State(new_position, copy.copy(state.ghost1), copy.copy(state.ghost2), map_, score)
        return new_state_

    class State:
        def __init__(self, pacman, ghost1, ghost2, map_, score):
            self.map = copy.copy(map_)
            self.pacman = pacman
            self.ghost1 = ghost1
            self.ghost2 = ghost2
            self.score = score

        def e_utility(self):
            manhattan_dist = self.manhattan_distance()
            nearest_dot = self.dist_to_nearest_dot()
            dots = self.count_dots()
            # print(self.score)
            # print(self.ghost1 ,self.ghost2, self.pacman, manhattan_dist, nearest_dot, self.score)
            return manhattan_dist * 5 - nearest_dot * 10 + self.score * 10 + dots * -100

        def dist_to_nearest_dot(self):
            map_ = copy.copy(self.map)
            position = self.pacman
            visited = {(position[0], position[1])}
            queue = [[position, 0]]
            while True:
                current = queue.pop(0)
                if map_[current[0][0]][current[0][1]] == 1:
                    return current[1]
                if map_[current[0][0] + 1][current[0][1]] != -1:
                    if not visited.__contains__((current[0][0] + 1, current[0][1])):
                        queue.append([[current[0][0] + 1, current[0][1]], current[1] + 1])
                        visited.add((current[0][0] + 1, current[0][1]))
                if map_[current[0][0] - 1][current[0][1]] != -1:
                    if not visited.__contains__((current[0][0] - 1, current[0][1])):
                        queue.append([[current[0][0] - 1, current[0][1]], current[1] + 1])
                        visited.add((current[0][0] - 1, current[0][1]))
                if map_[current[0][0]][current[0][1] + 1] != -1:
                    if not visited.__contains__((current[0][0], current[0][1] + 1)):
                        queue.append([[current[0][0], current[0][1] + 1], current[1] + 1])
                        visited.add((current[0][0], current[0][1] + 1))
                if map_[current[0][0]][current[0][1] - 1] != -1:
                    if not visited.__contains__((current[0][0], current[0][1] - 1)):
                        queue.append([[current[0][0], current[0][1] - 1], current[1] + 1])
                        visited.add((current[0][0], current[0][1] - 1))

        def manhattan_distance(self):
            min_ = float('+inf')
            for i in [self.ghost1, self.ghost2]:
                hold = abs(self.pacman[0] - i[0]) + abs(self.pacman[1] - i[1])
                if min_ > hold:
                    min_ = hold
            return min_

        def won_or_lost(self):
            if self.pacman == self.ghost1 or self.pacman == self.ghost2 or self.score <= 0:
                return 0
            elif self.count_dots() == 0:
                return 1
            else:
                return 2

        def count_dots(self):
            count = 0
            for i in self.map:
                for j in i:
                    if j == 1:
                        count += 1
            return count

        def eval_available_moves(self, position):
            available_moves = []
            if self.map[position[0]][position[1] - 1] != -1:
                available_moves.append([position[0], position[1] - 1])
            if self.map[position[0] - 1][position[1]] != -1:
                available_moves.append([position[0] - 1, position[1]])
            if self.map[position[0]][position[1] + 1] != -1:
                available_moves.append([position[0], position[1] + 1])
            if self.map[position[0] + 1][position[1]] != -1:
                available_moves.append([position[0] + 1, position[1]])
            return available_moves
