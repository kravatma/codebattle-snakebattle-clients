from snakebattleclient.SnakeBattleClient import GameClient
import random
import logging
import mysnake
import os

from snakebattleclient.internals.SnakeAction import SnakeAction
from snakebattleclient.internals.Board import Board

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)

external_memory = None

def turn(gcb: Board):
    global external_memory
    gcb.set_params()
    my_snake = gcb.me
    enemies_ex = gcb.enemies
    pills = gcb.pills
    if enemies_ex == []:
        external_memory = None
        return random.choice(list(SnakeAction))

    if not external_memory:
        for i, _ex in enumerate(enemies_ex):
            _ex['id'] = i
    else:
        for j, _ex in enumerate(enemies_ex):
            for i, prev_enm in enumerate(external_memory['enemies']):
                if _ex['coords'][1] == prev_enm['coords'][0]:
                    _ex['id'] = prev_enm['id']
                    if prev_enm['evil_capacity'] > 0:
                        _ex['evil_capacity'] = prev_enm['evil_capacity'] - 1
                    else:
                        _ex['evil_capacity'] = 0

                    if _ex['coords'][0] in external_memory['pills']:
                        _ex['evil_capacity'] = _ex['evil_capacity'] + 10



        if external_memory['my_snake']['evil_capacity'] > 0:
            my_snake['evil_capacity'] = external_memory['my_snake']['evil_capacity'] - 1

        if my_snake['coords'][0] in external_memory['pills']:
            my_snake['evil_capacity'] = my_snake['evil_capacity'] + 10

    external_memory = {'enemies': enemies_ex.copy(),
                       'my_snake': my_snake.copy(),
                       'pills': pills
    }

    #print(external_memory)

    #if len(gcb.enemies)>0:

    if gcb.me:
        print(gcb.enemies)
        my_snake = mysnake.Snake(gcb)
        direction = my_snake.make_step()
        print('---------', direction, '---------')
        return direction
    else:
        return random.choice(list(SnakeAction))


def main():
    gcb = GameClient(
        "http://codebattle-pro-2020s1.westeurope.cloudapp.azure.com/codenjoy-contest/board/player/gys2717qyh2vbep0o82m?code=6235490413342144723")
    print('---------------------------------------------------------------------')
    gcb.run(turn)

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as exc:
            print(exc)