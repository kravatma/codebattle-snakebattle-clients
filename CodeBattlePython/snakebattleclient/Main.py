from snakebattleclient.SnakeBattleClient import GameClient
import random
import logging
import mysnake.mysnake as mysnake

from snakebattleclient.internals.SnakeAction import SnakeAction
from snakebattleclient.internals.Board import Board

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)

def turn(gcb: Board):
    apples = gcb.get_apples()
    walls = gcb.get_walls()
    stones = gcb.get_stones()
    golds = gcb.get_gold()
    cells = gcb.get_free_space()

    my_head = gcb.get_my_head()
    my_body = gcb.get_my_body()
    my_tail = gcb.get_my_tail()

    enemy_heads = gcb.get_my_head()
    enemy_bodies = gcb.get_my_body()
    enemy_tails = gcb.get_my_tail()

    """
    print(apples)
    print(walls)
    print(stones)
    print(golds)
    print(cells)
    print(my_head)
    print(my_body)
    print(my_tail)
    print(enemy_heads)
    print(enemy_bodies)
    print(enemy_tails)
    """
    if my_head is None:
        return random.choice(list(SnakeAction))


    field = mysnake.Field(cells=cells, apples=apples, walls=walls, stones=stones, golds=golds)
    my_snake = mysnake.Snake(coords=[my_head]+my_body+my_tail)
    enemy_coords = [enemy_heads] + enemy_bodies + enemy_tails
    direction = my_snake.make_step(field=field, enemy_coords=enemy_coords)

    #return random.choice(list(SnakeAction))
    print(direction)
    return direction


def main():
    gcb = GameClient(
        "http://codebattle-pro-2020s1.westeurope.cloudapp.azure.com/codenjoy-contest/board/player/2rc950jnn534djwrnvuu?code=8143934113055717078&gameName=snakebattle")
    gcb.run(turn)

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as exc:
            print(exc)