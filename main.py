import time
from dataclasses import dataclass

import pyautogui as pg
import mouse

from src import detection

coordinates = {
    'monitor-1-full-screen': {
        'lvl-up-1': (180, 460),
        'monster': (1440, 570)
    }
}


def click(x: int, y: int, delay_after: float = .025):
    mouse.move(x, y, absolute=True, duration=0)
    mouse.click()
    time.sleep(delay_after)


def get_variant():
    return 'monitor-1-full-screen'


def click_monster():
    x, y = coordinates[get_variant()]['monster']
    click(x, y)


def click_level_up(position: int = 1):
    x, y = coordinates[get_variant()][f'lvl-up-{position}']
    click(x, y)


def print_current_position(delay: int = 1):
    time.sleep(delay)
    position = pg.position()
    print(position)
    return position


def get_click_iterator(count: int | float):
    i = 0

    if count == float('inf'):
        while True:
            yield i
            i += 1

    else:
        for _ in range(count):
            yield i
            i += 1


def main():
    # action = 'click_level_up'
    action = 'click_monster'
    # click_count = 25
    click_count = float('inf')

    action_lookup = {
        'click_monster': click_monster,
        'click_level_up': click_level_up
    }

    # minus one from iterator
    action_lookup[action]()

    initial_xy = pg.position()
    iterator = get_click_iterator(click_count - 1)

    for i in iterator:
        action_lookup[action]()

        if i % 10 == 0:
            current_xy = pg.position()

            if initial_xy != current_xy:
                print('Position changed')
                break

        # if i % 100 == 0:
        #     for j in range(5):
        #         click_level_up(1)


if __name__ == '__main__':
    main()
