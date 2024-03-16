import time
import sys
from dataclasses import dataclass

import pyautogui as pg
import mouse

pg.PAUSE = 0

# from src import detection

coordinates = {
    'monitor-1-full-screen': {
        'lvl-up-1': (180, 460),
        'monster': (1440, 570)
    },
    'vmware': {
        'monster': (1301, 560)
    },
    'vmware-half-screen': {
        'monster': (1660, 450),
        'scroll-down-button': (1420, 670),
        'last-unlocked-upgrade': (1100, 500),
        'farm-mode-toggle': (1880, 320),
        'skill-upgrade-1': (1160, 510),
        'skill-upgrade-2': (1190, 510),
        'skill-upgrade-3': (1220, 510),
        'skill-1': (1475, 320),
        'skill-2': (1475, 360),
        'skill-3': (1475, 400),
        'skill-4': (1475, 440),
        'skill-5': (1475, 480),
        'skill-6': (1475, 520),
        'skill-7': (1475, 560),
        'skill-8': (1475, 600),
        'skill-9': (1475, 640),
    }
}['vmware-half-screen']


def click(x: int, y: int, delay_after: float = .025):
    pg.click(x, y)
    if delay_after:
        time.sleep(delay_after)


def mouse_down(x: int, y: int):
    pg.mouseDown(x, y)


def mouse_up(x: int, y: int):
    pg.mouseUp(x, y)


def mouse_down_on_component(name: str):
    x, y = coordinates[name]
    mouse_down(x, y)


def mouse_up_on_component(name: str):
    x, y = coordinates[name]
    mouse_up(x, y)


def click_component(name: str):
    x, y = coordinates[name]
    click(x, y)


def generate_clicks(count: int | float):
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
    click_count = float('inf')

    click_component('monster')

    initial_xy = pg.position()
    clicks = generate_clicks(click_count - 1)
    i = 0

    while True:
        click_component('monster')

        if i % 500 == 0:
            print(f'Index: {i % 10_000}/10,000')

        if i % 10 == 0:
            current_xy = pg.position()

            if initial_xy != current_xy:
                print('Position changed')
                break

        if i % 2_000 == 0:
            print('scrolling down')
            mouse_down_on_component('scroll-down-button')
            time.sleep(3)
            mouse_up_on_component('scroll-down-button')
            time.sleep(.25)

        if i % 2_000 == 0:
            print('upgrading')
            click_component('skill-upgrade-1')
            click_component('skill-upgrade-2')
            click_component('skill-upgrade-3')

            for _ in range(50):
                click_component('last-unlocked-upgrade')

        if i % 10_000 == 0:
            print('toggling farm mode')
            click_component('farm-mode-toggle')
            time.sleep(.25)

            for j in range(1, 10):
                click_component(f'skill-{j}')
                time.sleep(.1)

            time.sleep(.25)

        i += 1


if __name__ == '__main__':
    # cusotm logic
    if len(sys.argv) > 1:

        if sys.argv[1] == 'position':
            time.sleep(2)
            print(pg.position())

    else:
        main()
