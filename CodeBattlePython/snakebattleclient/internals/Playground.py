import numpy as np
import time
import matplotlib.pyplot as plt
import random


class Field:
    def __init__(self, cells=None, walls=None, apples=None, stones=None, golds=None, fp=None):
        self.cells = cells
        self.walls = walls
        self.raw_matrix = None
        self.apples = apples
        self.golds = golds
        self.stones = stones
        if fp:
            self.read_from_file(fp)

    def read_from_file(self, fp):
        with open(fp) as f:
            rows = f.readlines()
            splited_rows = [list(r.strip()) for r in rows]
            matr = np.array(splited_rows).astype(int)
            self.raw_matrix = matr
            walls_array = np.argwhere(matr == 1)
            self.walls = set(tuple(wa) for wa in walls_array)
            cells_array = np.argwhere(matr == 0)
            self.cells = set(tuple(wa) for wa in cells_array)

    def generate_apple(self, snakes):
        snakes_coords = set()
        apples_array = np.argwhere(self.raw_matrix == 4)
        apples = set(tuple(wa) for wa in apples_array)
        for snake in snakes:
            snakes_coords = snakes_coords.union(set(snake.coords))
        available_points = self.cells - snakes_coords - apples
        new_apple = random.choice(list(available_points))
        self.raw_matrix[new_apple] = 4



class Playground:
    def __init__(self, size=None, snakes=None, fp=None):
        if fp:
            self.field = Field(fp=fp)
        if not snakes:
            walls = self.field.walls
            coords1 = [(4, 7), (5, 7), (6, 7), (6, 8), (6, 9)]
            coords2 = [(2, 4)]
            coords3 = [(5, 6)]
            self.snakes = [Snake(coords=coords3), Snake(coords=coords2)]

        self.pg_fig = plt.figure()
        self.pg_ax = self.pg_fig.add_subplot()
        plt.ion()
        plt.show()

    def init_snakes(self, fp):
        pass

    def make_step(self):
        for snake in self.snakes:
            if snake.alive == True:
                snake.make_step(self.field, snakes=self.snakes)

    def count_alive_snakes(self):
        c = 0
        for snake in self.snakes:
            if snake.alive == True:
                c += 1
        return c

    def check_collisions(self):
        walls = self.field.walls
        for i, snake in enumerate(self.snakes):
            head = snake.coords[0]
            others_snakes = set()
            for enemy in self.snakes[:i]+self.snakes[i+1:]:
                others_snakes = others_snakes.union(set(enemy.coords))
            if head in walls.union(others_snakes):
                #print('collision', 'walls:', head in walls, 'snakes:', head in others_snakes)
                print('snake id:', i)
                #snake.die()
            if self.field.raw_matrix[head] == 4:
                self.field.raw_matrix[head] = 0
                self.field.generate_apple(self.snakes)

    def draw_pg(self, cool=False):
        pg_matrix = self.field.raw_matrix.copy()
        for snake in self.snakes:
            if snake.alive == True:
                for snake_piece in snake.coords:
                    pg_matrix[snake_piece] = 2

        #print(pg_matrix)
        self.pg_ax.matshow(pg_matrix)
        #plt.draw()
        plt.pause(0.0000001)


    def run(self, delay=1, draw=False, max_steps=50):
        j = 0
        self.draw_pg()
        while self.count_alive_snakes() > 0 and j < max_steps:
            self.make_step()
            self.check_collisions()
            time.sleep(delay)
            if draw == True:
                self.draw_pg()
            j += 1


if __name__ == '__main__':
    PG = Playground(fp='testmap.txt')
    PG.run(delay=0.000001, draw=True)





