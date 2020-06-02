import random
from snakebattleclient.internals.SnakeAction import SnakeAction

def tree_search(tree, end):
    c_point = end
    route = []
    while True:
        l, p_point = tree[c_point]
        if p_point is None:
            break
        route.append(c_point)
        c_point = p_point
    route.reverse()
    return route

class Snake:
    def __init__(self, board):
        self.board = board
        self.route = None
        self.evil_capacity = 0
        self.me = board.me
        self.enemies = board.enemies

    def length(self, snake):
        return len(snake['coords'])

    def find_nearest_obj(self, snake, objects, check=True, isyum=1):
        print('searching nearest obj')
        head_y, head_x = snake['coords'][0]
        wave_points = {(head_y, head_x): (0, None)}
        front = {(head_y, head_x)}
        evil_cap = self.evil_capacity
        route = []

        l = 0
        doing = True
        got = False
        while doing == True:
            new_front = set()
            l += 1
            if l > 50:
                doing = False
            for p_point in front:
                y, x = p_point
                # if x < 0 or x > board.raw_matrix.shape[1] or y < 0 or y > board.raw_matrix.shape[0]:
                #    doing = False
                stones_and_walls = set(self.board.walls)
                enemies_coords = []
                for enemy in self.enemies:
                    enemies_coords.extend(enemy['coords'])

                if l >= evil_cap:
                    stones_and_walls = stones_and_walls.union(set(self.board.stones))
                new_sub_front = {(y,x-1),(y,x+1),(y-1,x),(y+1,x)} - stones_and_walls - set(self.me['coords'][l:]) - set(wave_points.keys()) - set(enemies_coords*isyum)
                new_front = new_front.union(new_sub_front)
                for c_point in new_sub_front:
                    if not wave_points.get(c_point):
                        wave_points[c_point] = (l, p_point)
                        if c_point in objects:
                            apy, apx = c_point
                            if len({(apy, apx - 1), (apy, apx + 1), (apy - 1, apx), (apy + 1, apx)}.intersection(
                                    stones_and_walls.union())) >= 3:
                                continue
                            route = tree_search(wave_points, (apy, apx))
                            if check == True:
                                fake_snake = {'coords': route[-len(snake):]}
                                ch_rt = self.find_nearest_obj(fake_snake, objects, check=False)
                                if ch_rt == []:
                                    continue
                            doing = False
                            got = True

            front = new_front.copy()
        return route

    def set_route(self):
        #print('start route search')
        head_y, head_x = self.me['coords'][0]
        n_apple = self.find_nearest_obj(self.me, self.board.apples)
        n_gold = self.find_nearest_obj(self.me, self.board.golds)
        n_pill = self.find_nearest_obj(self.me, self.board.pills)
        ways = {int(len(n_apple)*self.length(self.me)/3): n_apple}
        ways[int(len(n_gold)*self.length(self.me)/5)] = n_gold
        ways[len(n_pill)] = n_pill

        best_way = min(ways.keys())

        self.route = ways[best_way]
        if self.me['evil'] is True:
            snks = [c['coords'][0] for c in self.enemies]
            fight_route = self.find_nearest_obj(self.me, snks, isyum=0)
            if len(fight_route) < self.me['evil_capacity'] + 3:
                self.route = fight_route
                print('AIMED')

        print(self.route)

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

    def make_step(self):
        head_y, head_x = self.me['coords'][0]
        self.set_route()
        print(len(self.route))
        if len(self.route) > 0:
            step_y, step_x = self.route[0]
        else:
            snakes_coords = set()
            for enemy in self.enemies:
                snakes_coords = snakes_coords.union(set(enemy['coords']))

            walls = set(self.board.walls)
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



























