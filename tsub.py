#import sys
#import curses
import os
import time
import threading
import flash_i2c
import configparser
import math
from pynput import keyboard


__shutdown = False


def kbd_f12():
    global __shutdown
    # В этом блоке будет работать слушатель событий.
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.f12:
                __shutdown = True
                break


def shutdown():
    global __shutdown
    __shutdown = True


def main():
    config = configparser.ConfigParser()
    config.read('tsub.ini')
    all_sections = config.sections()

    # Clear screen
    lock = threading.Lock()
    exps = []
    sensors = []
    for sect in all_sections:
        try:
            addr = int(sect)
            if 9 < addr < 128:
                sens_list = []
                options = config.options(sect)
                for opt in options:
                    try:
                        sens = int(opt)
                        if 0 <= sens < 8:
                            sens_list.append(sens)
                            sensors.append({'n': len(exps), 'addr': addr, 'input': sens, 'name': config.get(sect, opt)})
                    except ValueError:
                        continue
                exps.append(flash_i2c.FlashI2C(addr, lock, sens_list=sens_list))
        except ValueError:
            continue

    time.sleep(2)
    col_width = max([len(sens['name']) for sens in sensors]) + 4
    readouts_num = int(config.get('DEFAULT', 'ReadoutsNum'))

    for sens in sensors:
        print(f'{sens['name']}: '.ljust(col_width, ' '), end='')

        avrg = 0
        avrg2 = 0
        exp_n = sens['n']
        exp_in = sens['input']
        for _ in range(readouts_num):
            readout = exps[exp_n].read(exp_in)
            avrg += readout
            avrg2 += readout ** 2

        print(f'{round(avrg/(readouts_num/2), 2)}'.ljust(10, ' '), end='')
        print(f'{round(math.sqrt(avrg2/(readouts_num/2)), 2)}'.ljust(10, ' '), end='')
        print('')


if __name__ == '__main__':
    # thr = threading.Thread(target=kbd_f12, name=f'kbd_f12')
    # thr.start()

    main()
    # try:
    #     curses.wrapper(main)
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)

    # thr.join()
