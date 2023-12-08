import random

import world as w

ghost_test = [(1, 2), (1, 3), (2, 4), (2, 8), (3, 4),
              (3, 8), (4, 2), (4, 3), (5, 4), (5, 6),
              (6, 4), (6, 8), (7, 4), (7, 8), (8, 7),
              (8, 8), (9, 5), (9, 10), (10, 6), (10, 16)]
pacman_test = [(1, 1), (2, 1), (3, 1), (4, 1),
               (5, 1), (6, 1), (7, 1), (3, 12),
               (8, 4), (9, 1), (10, 1), (1, 8)]
world = w.WorldState(random.choice(pacman_test), random.choice(ghost_test), random.choice(ghost_test), False)
world.start()

# wins = 0
# step = 0
# for i in range(100):
#     test_world = w.WorldState(random.choice(pacman_test), random.choice(ghost_test), random.choice(ghost_test), True)
#     step = step + 1
#     if test_world.start():
#         print(step, " :", "\033[92m" + " win!" + "\033[0m")
#         wins = wins + 1
#     else:
#         print(step, " :", "\033[91m" +  "lose!" + "\033[0m")
# print("win ratio:", (wins / 100) * 100, "percent")
