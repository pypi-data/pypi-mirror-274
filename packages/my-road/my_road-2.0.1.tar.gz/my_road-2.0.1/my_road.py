__all__ = ['my_road']

import time


def cycle():
    string = '.'
    a = 0
    b = True
    while b:
        if a <= 15:
            for i in range(1, 65 + 1):
                print(f'{string * i:97}.{string * i:>97}')
                a += 1
                time.sleep(0.025)
                if a == 65:
                    for i in range(65, 0, -1):
                        print(f"{string * i:97}.{string * i:>97}")
                        time.sleep(0.025)
                        if i == 1:
                            b = False


def my_road(num):
    for i in range(1, num + 1):
        cycle()
