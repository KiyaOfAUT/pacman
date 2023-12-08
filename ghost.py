import random


class Ghost:
    def __init__(self, position, map_):
        self.position = position
        self.map = map_
        self.available_moves = []

    def move(self):
        self.eval_available_moves()
        self.position = random.choice(self.available_moves)
        return self.position
    
    def eval_available_moves(self):
        self.available_moves.clear()
        if self.map[self.position[0]][self.position[1] - 1] != -1:
            self.available_moves.append([self.position[0], self.position[1] - 1])
        if self.map[self.position[0] - 1][self.position[1]] != -1:
            self.available_moves.append([self.position[0] - 1, self.position[1]])
        if self.map[self.position[0]][self.position[1] + 1] != -1:
            self.available_moves.append([self.position[0], self.position[1] + 1])
        if self.map[self.position[0] + 1][self.position[1]] != -1:
            self.available_moves.append([self.position[0] + 1, self.position[1]])
