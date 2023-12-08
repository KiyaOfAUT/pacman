import random
import numpy as np
import time


class Pacman:
    def __init__(self, position, map_):
        self.map = map_
        self.position = position
        self.eaten_points = 0
        self.h = 0
        self.score = 0
        self.hold = 0
        self.h = []

    class State:
        def __init__(self, pacman, ghost1, ghost2, map_, score):
            self.map = map_
            self.pacman = pacman
            self.ghost1 = ghost1
            self.ghost2 = ghost2
            self.score = score

    def move(self, current_state):
        depth = 3
        map_ = np.copy(current_state.map)
        self.position = current_state.pacman
        ghost1hold = current_state.ghost1
        ghost2hold = current_state.ghost2
        moves = []
        if self.map[self.position[0] - 1][self.position[1]] != -1:
            state = self.State(self.position, ghost1hold, ghost2hold, map_, current_state.score)
            if self.map[self.position[0] - 1][self.position[1]] == 1:
                state.score = state.score + 5
            else:
                state.score = state.score - 1
            state.map[self.position[0] - 1, self.position[1]] = 0
            state.pacman = [self.position[0] - 1, self.position[1]]
            hold = self.minimax(2, 1, depth, state)
            moves.append([1, hold])
        if self.map[self.position[0]][self.position[1] + 1] != -1:
            state = self.State(self.position, ghost1hold, ghost2hold, map_, current_state.score)
            if self.map[self.position[0]][self.position[1] + 1] == 1:
                state.score = state.score + 5
            else:
                state.score = state.score - 1
            state.map[self.position[0], self.position[1] + 1] = 0
            state.pacman = [self.position[0], self.position[1] + 1]
            hold = self.minimax(2, 1, depth, state)
            moves.append([2, hold])
        if self.map[self.position[0] + 1][self.position[1]] != -1:
            state = self.State(self.position, ghost1hold, ghost2hold, map_, current_state.score)
            if self.map[self.position[0] + 1][self.position[1]] == 1:
                state.score = state.score + 5
            else:
                state.score = state.score - 1
            state.map[self.position[0] + 1, self.position[1]] = 0
            state.pacman = [self.position[0] + 1, self.position[1]]
            hold = self.minimax(2, 1, depth, state)
            moves.append([3, hold])
        if self.map[self.position[0]][self.position[1] - 1] != -1:
            state = self.State(self.position, ghost1hold, ghost2hold, map_, current_state.score)
            if self.map[self.position[0]][self.position[1] - 1] == 1:
                state.score = state.score + 5
            else:
                state.score = state.score - 1
            state.map[self.position[0], self.position[1] - 1] = 0
            state.pacman = [self.position[0], self.position[1] - 1]
            hold = self.minimax(2, 1, depth, state)
            moves.append([4, hold])
        max_ = float("-inf")
        dir_ = 0
        for i in moves:
            if i[1] > max_:
                max_ = i[1]
                dir_ = i[0]
        print(self.hold)
        print(moves)
        # time.sleep(0.4)
        self.h.append([self.hold, moves])
        self.hold = 0
        if dir_ == 0:
            return random.choice(self.eval_available_moves(current_state, current_state.pacman))
        elif dir_ == 1:
            return [self.position[0] - 1, self.position[1]]
        elif dir_ == 2:
            return [self.position[0], self.position[1] + 1]
        elif dir_ == 3:
            return [self.position[0] + 1, self.position[1]]
        elif dir_ == 4:
            return [self.position[0], self.position[1] - 1]

    def minimax(self, agent, current_depth, depth, state):
        status = self.won_or_lost(state)
        if current_depth == depth:
            return self.e_utility(state)
        if status == 0:
            return float('-inf')
        elif status == 1:
            return float('+inf')
        if agent == 1:
            available_moves = self.eval_available_moves(state, state.pacman)
            max_value = float('-inf')
            hold = []
            for i in available_moves:
                hold_state = self.new_state(state, 0, i)
                hold.append(self.minimax(2, current_depth + 1, depth, hold_state))
            for i in hold:
                max_value = max(max_value, i)
            return max_value
        if agent == 2:
            available_moves = self.eval_available_moves(state, state.ghost1)
            min_value = float('inf')
            hold = []
            for i in available_moves:
                hold_state = self.new_state(state, 1, i)
                hold.append(self.minimax(3, current_depth + 1, depth, hold_state))
            for i in hold:
                min_value = min(min_value, i)
            return min_value
        if agent == 3:
            available_moves = self.eval_available_moves(state, state.ghost2)
            min_value = float('inf')
            hold = []
            for i in available_moves:
                hold_state = self.new_state(state, 2, i)
                hold.append(self.minimax(1, current_depth + 1, depth, hold_state))
            for i in hold:
                min_value = min(min_value, i)
            return min_value

    def e_utility(self, state):
        manhattan_dist = self.manhattan_distance(state)
        nearest_dot = self.dist_to_nearest_dot(state)
        self.hold += 1
        return -1 * manhattan_dist / 10 + state.score * 100 - 1000 / nearest_dot

    def dist_to_nearest_dot(self, state):
        map_ = np.copy(state.map)
        position = state.pacman
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

    def new_state(self, state, agent, new_position):
        map_ = np.copy(state.map)
        if agent == 1:
            new_state_ = self.State(state.pacman, new_position, state.ghost2, map_, state.score)
        elif agent == 2:
            new_state_ = self.State(state.pacman, state.ghost1, new_position, map_, state.score)
        else:
            if map_[new_position[0]][new_position[1]] == 1:
                score = state.score + 5
            else:
                score = state.score - 1
            map_[new_position[0]][new_position[1]] = 0
            new_state_ = self.State(new_position, state.ghost1, state.ghost2, map_, score)
        return new_state_

    def manhattan_distance(self, state):
        sum_ = 0
        ghosts = [state.ghost1, state.ghost2]
        pacman = state.pacman
        for i in ghosts:
            sum_ = sum_ + abs(pacman[0] - i[0]) + abs(pacman[1] - i[1])
        return sum_

    def won_or_lost(self, state):
        if state.pacman == state.ghost1 or state.pacman == state.ghost2 or state.score <= 0:
            return 0
        elif self.count_dots(state) == 0:
            return 1
        else:
            return 2

    def count_dots(self, state):
        count = 0
        for i in state.map:
            for j in i:
                if j == 1:
                    count = count + 1
        return count


    def eval_available_moves(self, state, position):
        available_moves = []
        if state.map[position[0]][position[1] - 1] != -1:
            available_moves.append([position[0], position[1] - 1])
        if state.map[position[0] - 1][position[1]] != -1:
            available_moves.append([position[0] - 1, position[1]])
        if state.map[position[0]][position[1] + 1] != -1:
            available_moves.append([position[0], position[1] + 1])
        if state.map[position[0] + 1][position[1]] != -1:
            available_moves.append([position[0] + 1, position[1]])
        return available_moves


