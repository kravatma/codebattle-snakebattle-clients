import numpy as np
import time
import matplotlib.pyplot as plt
import random
from snakebattleclient.internals.SnakeAction import SnakeAction


class Snake:
    def __init__(self, coords, strategy=None):
        self.coords = coords
        self.strategy = strategy
        self.route = None
        self.alive = True

    def length(self):
        return len(self.coords)

    def die(self):
        self.alive = False
        print('snake die, length =', self.length())
        return self.length()

    def move(self, direction, rise=False):
        head_y, head_x = self.coords[0]
        if direction == 'up':
            head_y -= 1
        if direction == 'down':
            head_y += 1
        if direction == 'left':
            head_x -= 1
        if direction == 'right':
            head_x += 1

        if (head_y, head_x) in self.coords[1:]:
            print('self eat:', (head_y, head_x), self.coords[1:])
            self.die()

        if rise == True:
            self.coords = [(head_y, head_x)] + self.coords
        else:
            self.coords = [(head_y, head_x)] + self.coords[:-1]

    def set_route(self, field, snakes=[], enemy_coords=[]):
        print('start route search')
        head_y, head_x = self.coords[0]
        wave_points = {(head_y, head_x): (0, None)}
        front = {(head_y, head_x)}

        if snakes:
            snakes_coords = set()
            for snake in snakes:
                snakes_coords=snakes_coords.union(set(snake.coords))
        else:
            snakes_coords = set(enemy_coords)

        #print(snakes_coords)
        l = 0
        doing = True
        got = False
        while doing == True:
            new_front = set()
            l += 1
            if l > 30:
                doing = False
            for p_point in front:
                y, x = p_point
                #if x < 0 or x > field.raw_matrix.shape[1] or y < 0 or y > field.raw_matrix.shape[0]:
                #    doing = False
                stones_and_walls = set(field.walls).union(field.stones)
                print('---------------')
                print('stone and walls:', stones_and_walls)
                print('self coords:', set(self.coords))
                print('wave:', set(wave_points.keys()))
                print('enemies:', snakes_coords)
                print('---------------')
                new_sub_front = {(y, x-1), (y, x+1), (y-1, x), (y+1, x)} - stones_and_walls - set(self.coords) - set(wave_points.keys()) - snakes_coords
                new_front = new_front.union(new_sub_front)
                for c_point in new_sub_front:
                    if not wave_points.get(c_point):
                        wave_points[c_point] = (l, p_point)
                        if c_point in field.apples or c_point in field.golds:
                            apy, apx = c_point
                            if len({(apy, apx-1), (apy, apx+1), (apy-1, apx), (apy+1, apx)}.intersection(stones_and_walls.union()))<=2:
                                doing = False
                                got = True


            front = new_front.copy()
        route = []
        #print(wave_points)
        if got == True:
            c_point = apy, apx
            while True:
                l, p_point = wave_points[c_point]
                if p_point is None:
                    break
                route.append(c_point)
                c_point = p_point
            #print(l)

        #print(route)
        route.reverse()
        self.route = route

    def define_direction(self, head, step):
        step_y, step_x = step
        head_y, head_x = head
        if step_x == head_x + 1 and step_y == head_y:
            return SnakeAction.RIGHT
        elif step_x == head_x - 1 and step_y == head_y:
            return SnakeAction.LEFT
        elif step_x == head_x and step_y == head_y - 1:
            return SnakeAction.UP
        elif step_x == head_x and step_y == head_y + 1:
            return SnakeAction.DOWN

    def make_step(self, field, snakes=[], enemy_coords=[]):
        print('start step', self.coords, len(self.coords))
        head_y, head_x = self.coords[0]
        self.set_route(field, snakes, enemy_coords)
        print(len(self.route))
        if len(self.route) > 0:
            step_y, step_x = self.route[0]
        else:
            snakes_coords = set()
            if len(snakes) > 0:
                for snake in snakes:
                    snakes_coords = snakes_coords.union(set(snake.coords))

            walls = set(field.walls)
            print('nearest points', walls)
            nearest_points = {(head_y+1, head_x), (head_y-1, head_x), (head_y, head_x+1), (head_y, head_x-1)}
            nearest_points = nearest_points - walls
            if len(nearest_points) == 0:
                print('BAITED')
                return None
            else:
                random_step = random.choice(list(nearest_points))
                step_y, step_x = random_step
        """
        if field.raw_matrix[step_y, step_x] == 4:
            rise = True
        else:
            rise = False
        """
        direction = self.define_direction(head=(head_y, head_x), step=(step_y, step_x))
        #self.move(direction, rise=rise)
        return direction


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
                snake.die()
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































