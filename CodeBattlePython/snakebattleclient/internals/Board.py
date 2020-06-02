from builtins import enumerate

from math import sqrt
from snakebattleclient.internals.Element import Element, SEARCH_HELPER
from snakebattleclient.internals.Point import Point

heads_elements = [Element('ENEMY_HEAD_DOWN'), Element('ENEMY_HEAD_LEFT'),
                  Element('ENEMY_HEAD_RIGHT'), Element('ENEMY_HEAD_UP'),
                  Element('ENEMY_HEAD_EVIL'), Element('ENEMY_HEAD_DEAD'),
                  Element('HEAD_DOWN'), Element('HEAD_LEFT'),
                  Element('HEAD_RIGHT'), Element('HEAD_UP'),
                  Element('HEAD_EVIL'), Element('HEAD_DEAD')]

class Board:
    """ Class describes the Board field for Bomberman game."""

    def __init__(self, board_string):
        self._string = board_string.replace('\n', '')
        self._len = len(self._string)  # the length of the string
        self._size = int(sqrt(self._len))  # size of the board
        self.walls = None
        self.stones = None
        self.golds = None
        self.apples = None
        self.enemies = None
        self.me = None
        self.cells = None
        self.pills = None

    def get_point_by_shift(self, shift):
        return Point(shift % self._size, shift / self._size)

    def find_first_element(self, *element_types):
        _result = []
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            for eltype in element_types:
                if self.has_element_at(point, eltype):
                    return point._y, point._x
        return None

    def _find_all(self, *element_types):
        """ Returns the list of points for the given element type."""
        _points = []
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            for eltype in element_types:
                if self.has_element_at(point, eltype):
                    _points.append((point._y, point._x))
        return _points

    def get_free_space(self):
        return self._find_all(Element('NONE'))

    def get_my_tail(self):
        return self.find_first_element(Element('TAIL_END_DOWN'), Element('TAIL_END_LEFT'), Element('TAIL_END_UP'),
                                       Element('TAIL_END_RIGHT'))

    def get_enemies_tails(self):
        return self._find_all(Element('ENEMY_TAIL_END_DOWN'), Element('ENEMY_TAIL_END_LEFT'),
                                       Element('ENEMY_TAIL_END_UP'), Element('ENEMY_TAIL_END_RIGHT'))

    def find_snake_by_tail(self, tail):
        cur_y, cur_x = tail
        cur_elem = self.get_element_at(Point(cur_x, cur_y))
        snake_coords = [(cur_y, cur_x)]

        while cur_elem not in heads_elements:
            #print(cur_elem.get_char(), end='')
            #print(self.get_element_type_at(cur_x, cur_y - 1).get_char(), end='')
            #print(self.get_element_type_at(cur_x, cur_y + 1).get_char(), end='')
            #print(self.get_element_type_at(cur_x - 1, cur_y).get_char(), end='')
            #print(self.get_element_type_at(cur_x + 1, cur_y).get_char(), end='\n')
            got = 0
            for crnt, direction, nxt in SEARCH_HELPER:
                if direction == 'UP' and Element(crnt) == cur_elem and self.get_element_type_at(cur_x, cur_y - 1) == Element(nxt):
                    if (cur_y - 1, cur_x) not in snake_coords:
                        cur_x, cur_y = cur_x, cur_y - 1
                        got = 1
                        break
                if direction == 'DOWN' and Element(crnt) == cur_elem and self.get_element_type_at(cur_x, cur_y + 1) == Element(nxt):
                    if (cur_y + 1, cur_x) not in snake_coords:
                        cur_x, cur_y = cur_x, cur_y + 1
                        got = 1
                        break
                if direction == 'LEFT' and Element(crnt) == cur_elem and self.get_element_type_at(cur_x - 1, cur_y) == Element(nxt):
                    if (cur_y, cur_x - 1) not in snake_coords:
                        cur_x, cur_y = cur_x - 1, cur_y
                        got = 1
                        break
                if direction == 'RIGHT' and Element(crnt) == cur_elem and self.get_element_type_at(cur_x + 1, cur_y) == Element(nxt):
                    if (cur_y, cur_x + 1) not in snake_coords:
                        cur_x, cur_y = cur_x + 1, cur_y
                        got = 1
                        break

            if got == 0:
                break



            cur_elem = self.get_element_at(Point(cur_x, cur_y))

            snake_coords.append((cur_y, cur_x))

        snake_coords.reverse()
        evil = cur_elem in [Element('ENEMY_HEAD_EVIL'), Element('HEAD_EVIL')]
        snake = {'coords': snake_coords, 'evil': evil, 'evil_capacity': 0}

        return snake

    def get_my_snake(self):
        my_tail = self.get_my_tail()
        my_snake = None
        if my_tail:
            my_snake = self.find_snake_by_tail(my_tail)
        return my_snake


    def get_enemies(self):
        enemies_tails = self.get_enemies_tails()
        #print(enemies_tails)
        enemies = []
        walls = self.get_walls()
        rocks = self.get_stones()
        for enemy_tail in enemies_tails:
            #print(enemy_tail)
            enemy = self.find_snake_by_tail(enemy_tail)
            hy, hx = enemy['coords'][0]
            enemy['posible_steps'] = {(hy, hx-1), (hy, hx+1), (hy-1, hx), (hy+1, hx)} - set(self.walls) - set(self.stones*(enemy['evil']==False))
            enemies.append(enemy)

        return enemies


    def get_walls(self):
        walls = self._find_all(Element('WALL'))
        start_points = self._find_all(Element('START_FLOOR'))
        return walls + start_points



    def get_stones(self):
        return self._find_all(Element('STONE'))

    def get_barriers(self):
        """ Return the list of barriers Points."""
        points = set()
        points.update(self._find_all(Element('WALL'), Element('START_FLOOR'), Element('ENEMY_HEAD_SLEEP'),
                                     Element('ENEMY_TAIL_INACTIVE'), Element('TAIL_INACTIVE'), Element('STONE')))
        return list(points)

    def is_barrier_at(self, point):
        return self.get_barriers().__contains__(point)

    def get_apples(self):
        return self._find_all(Element('APPLE'))

    def am_i_evil(self):
        return self._find_all(Element('HEAD_EVIL')).__contains__(self.get_my_head())

    def am_i_flying(self):
        return self._find_all(Element('HEAD_FLY')).__contains__(self.get_my_head())

    def get_flying_pills(self):
        return self._find_all(Element('FLYING_PILL'))

    def get_furry_pills(self):
        return self._find_all(Element('FURY_PILL'))

    def get_golds(self):
        return self._find_all(Element('GOLD'))

    def get_start_points(self):
        return self._find_all(Element('START_FLOOR'))

    def get_element_at(self, point):
        """ Return an Element object at coordinates x,y."""
        return Element(self._string[self._xy2strpos(point.get_x(), point.get_y())])

    def get_element_type_at(self, x, y):
        """ Return an Element object at coordinates x,y."""
        return self.get_element_at(Point(x, y))

    def has_element_at(self, point, element_object):
        if point.is_out_of_board(self._size):
            return False
        return element_object == self.get_element_at(point)

    def find_element(self, type):
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            if self.has_element_at(point, type):
                return point
        return None

    def get_shift_by_point(self, point):
        return point.get_y() * self._size + point.get_x()

    def _strpos2pt(self, strpos):
        return Point(*self._strpos2xy(strpos))

    def _strpos2xy(self, strpos):
        return (strpos % self._size, strpos // self._size)

    def _xy2strpos(self, x, y):
        return self._size * y + x

    def print_board(self):
        print(self._line_by_line())

    def _line_by_line(self):
        return '\n'.join([self._string[i:i + self._size]
                          for i in range(0, self._len, self._size)])

    def to_string(self):
        return "Board:\n{brd}".format(brd=self._line_by_line())

    def set_params(self):
        print('awsgpc')
        self.apples = self.get_apples()
        self.walls = self.get_walls()
        self.stones = self.get_stones()
        self.golds = self.get_golds()
        self.pills = self.get_furry_pills()
        self.cells = self.get_free_space()
        print('enemies')
        self.enemies = self.get_enemies()
        print('me')
        self.me = self.get_my_snake()
        print('got')


if __name__ == '__main__':
    with open('testmap2.txt', encoding='utf-8') as f:
        rows = ''.join(f.readlines())
        brd = Board(rows)
        brd.set_params()
