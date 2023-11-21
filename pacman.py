class Pacman:
    def __init__(self, position, map_):
        self.map = map_
        self.position = position
        self.eaten_points = 0

    class State:
        def __init__(self, state):
            self.map = state.map
            self.pacman = state.pacman
            self.ghost1 = state.ghost1
            self.ghost2 = state.ghost2

    def move(self, CurrentState):
        state = self.State(CurrentState)
        if self.map[self.position[0]][self.position[1] - 1] != 0:
            d = self.minimax(2, 1, 10, state)
        else:
            d = 0
        if self.map[self.position[0] + 1][self.position[1]] != 0:
            r = self.minimax(2, 1, 10, state)
        else:
            r = 0
        if self.map[self.position[0]][self.position[1] + 1] != 0:
            u = self.minimax(2, 1, 10, state)
        else:
            u = 0
        if self.map[self.position[0] - 1][self.position[1]] != 0:
            l = self.minimax(2, 1, 10, state)
        else:
            l = 0
        direction = max(d, r, u, l)
        if direction == d:
            return [self.position[0], self.position[1] - 1]
        elif direction == r:
            return [self.position[0] + 1, self.position[1]]
        elif direction == u:
            return [self.position[0], self.position[1] + 1]
        elif direction == l:
            return [self.position[0] - 1, self.position[1]]

    def minimax(self, agent, current_depth, depth, state):
        status = self.won_or_lost(state)
        if current_depth == depth:
            return self.e_utility(state)
        if status == 0:
            return float('-inf')
        elif status == 1:
            return float('inf')
        if agent == 1:
            available_moves = self.eval_available_moves(state, state.pacman)
            max_value = float('-inf')
            for i in available_moves:
                hold = self.minimax(2, current_depth + 1, depth, self.new_state(state, 1, i))
                max_value = max(max_value, hold)
            return max_value
        if agent == 2:
            available_moves = self.eval_available_moves(state, state.ghost1)
            min_value = float('inf')
            for i in available_moves:
                hold = self.minimax(3, current_depth + 1, depth, self.new_state(state, 2, i))
                min_value = min(min_value, hold)
            return min_value
        if agent == 3:
            available_moves = self.eval_available_moves(state, state.ghost2)
            min_value = float('inf')
            for i in available_moves:
                hold = self.minimax(1, current_depth + 1, depth, self.new_state(state, 3, i))
                min_value = min(min_value, hold)
            return min_value

    def e_utility(self, state):
        manhattan_dist = self.manhattan_distance(state)
        dots = self.count_dots(state)
        nearest_dot = self.dist_to_nearest_dot(state)
        return dots * -1 + nearest_dot * -10 + manhattan_dist * 100

    def new_state(self, state, agent, new_position):
        if agent == 1:
            state.ghost1 = new_position
        elif agent == 2:
            state.ghost2 = new_position
        else:
            state.map[state.pacman[0]][state.pacman[1]] = 0
            state.pacman = new_position
        return state

    def manhattan_distance(self, state):
        sum_ = 0
        ghosts = [state.ghost1, state.ghost2]
        pacman = state.pacman
        for i in ghosts:
            sum_ = sum_ + pacman[0] - i[0] + pacman[1] - i[1]
        return sum_

    def won_or_lost(self, state):
        if state.pacman == state.ghost1 or state.pacman == state.ghost2:
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

    def dist_to_nearest_dot(self, state):
        position = state.pacman
        count = 0
        stack = [[position, 0]]
        while True:
            if count > 50:
                return 20
            current = stack.pop()
            if state.map[current[0][0]][current[0][1]]:
                return current[1]
            else:
                stack.append([[current[0][0] + 1, current[0][1]], current[1] + 1])
                stack.append([[current[0][0] - 1, current[0][1]], current[1] + 1])
                stack.append([[current[0][0], current[0][1] + 1], current[1] + 1])
                stack.append([[current[0][0], current[0][1] - 1], current[1] + 1])
            count = count + 1

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
