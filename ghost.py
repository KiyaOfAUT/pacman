import random


class Ghost:
    def __init__(self, position, map_):
        self.position = position
        self.map = map_
        self.available_moves = []
        self.eval_available_moves()

    def move(self):
        if not self.available_moves:
            self.eval_available_moves()
        return random.choices(self.available_moves)
    
    def eval_available_moves(self):
        if self.map[self.position[0]][self.position[1] - 1] != 0:
            self.available_moves.append([self.position[0], self.position[1] - 1])
        if self.map[self.position[0] - 1][self.position[1]] != 0:
            self.available_moves.append([self.position[0] - 1, self.position[1]])
        if self.map[self.position[0]][self.position[1] + 1] != 0:
            self.available_moves.append([self.position[0], self.position[1] + 1])
        if self.map[self.position[0] + 1][self.position[1]] != 0:
            self.available_moves.append([self.position[0] + 1, self.position[1]])
