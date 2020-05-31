import random
from snakebattleclient.internals.SnakeAction import SnakeAction


class Snake:
    def __init__(self, coords, strategy=None):
        self.coords = coords
        self.strategy = strategy
        self.route = None

    def length(self):
        return len(self.coords)

    def get_distance(self, board, target, evil=0):
        pass

    def set_route(self, board, snakes=[], enemy_coords=[]):
        #print('start route search')
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
                #if x < 0 or x > board.raw_matrix.shape[1] or y < 0 or y > board.raw_matrix.shape[0]:
                #    doing = False
                stones_and_walls = set(board.walls).union(board.stones)
                #print('---------------')
                #print('stone and walls:', stones_and_walls)
                #print('self coords:', set(self.coords))
                #print('wave:', set(wave_points.keys()))
                #print('enemies:', snakes_coords)
                #print('---------------')
                new_sub_front = {(y, x-1), (y, x+1), (y-1, x), (y+1, x)} - stones_and_walls - set(self.coords) - set(wave_points.keys()) - snakes_coords
                new_front = new_front.union(new_sub_front)
                for c_point in new_sub_front:
                    if not wave_points.get(c_point):
                        wave_points[c_point] = (l, p_point)
                        if c_point in board.apples or c_point in board.golds:
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

    def make_step(self, board, snakes=[], enemies=[]):
        print('start step', self.coords, len(self.coords))
        head_y, head_x = self.coords[0]
        enemy_coords = []
        self.set_route(board, snakes, enemy_coords)
        print(len(self.route))
        if len(self.route) > 0:
            step_y, step_x = self.route[0]
        else:
            snakes_coords = set()
            if len(snakes) > 0:
                for snake in snakes:
                    snakes_coords = snakes_coords.union(set(snake.coords))

            walls = set(board.walls)
            print('nearest points', walls)
            nearest_points = {(head_y+1, head_x), (head_y-1, head_x), (head_y, head_x+1), (head_y, head_x-1)}
            nearest_points = nearest_points - walls
            if len(nearest_points) == 0:
                print('BAITED')
                return None
            else:
                random_step = random.choice(list(nearest_points))
                step_y, step_x = random_step

        direction = self.define_direction(head=(head_y, head_x), step=(step_y, step_x))
        return direction



























