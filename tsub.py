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
	
    col_width = 0
    for i in range(len(sensors)):
        sens_str = f'{sensors[i]['name']}: '
        if len(sens_str) > col_width:
            col_width = len(sens_str)
    col_width += 2

    for i in range(len(sensors)):
        print(f'{sensors[i]['name']}'.ljust(col_width, ' '), end='')
    print('')

    readouts_num = int(config.get('DEFAULT', 'ReadoutsNum'))
    avrg = [0] * len(sensors)
    avrg2 = [0] * len(sensors)
    for _ in range(readouts_num):
        exp_thr = []
        for i in range(len(exps)):
            exp_thr.append(threading.Thread(target=exps[i].run, name=f'exp{i}'))
            exp_thr[i].start()

        for thr in exp_thr:
            thr.join()

        for i in range(len(sensors)):
            readout = exps[sensors[i]['n']].result[sensors[i]['input']]
            avrg[i] += readout
            avrg2[i] += readout ** 2
#            print(f'{readout}'.ljust(col_width, ' '), end='')
            exps[sensors[i]['n']].cnt += 1
#        print('')

    print('-' * len(sensors) * col_width)
    for i in range(len(sensors)):
        print(f'{round(avrg[i]/(readouts_num/2), 2)}'.ljust(col_width, ' '), end='')
    print('')
    for i in range(len(sensors)):
        print(f'{round(math.sqrt(avrg2[i]/(readouts_num/2)), 2)}'.ljust(col_width, ' '), end='')
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
