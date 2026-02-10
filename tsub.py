import sys
import curses
import threading
import flash_i2c
import keyboard
import configparser


__shutdown = False


def shutdown():
    global __shutdown
    __shutdown = True


def main(stdscr):
    config = configparser.ConfigParser()
    config.read('tsub.ini')
    all_sections = config.sections()

    # Clear screen
    stdscr.clear()

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

    stdscr.addstr(len(sensors) + 1, 0, 'Press "F12" to exit...')
    stdscr.refresh()

    max_len = 0
    for i in range(len(sensors)):
        sens_str = f'{sensors[i]['name']}: '
        if len(sens_str) > max_len:
            max_len = len(sens_str)
        stdscr.addstr(i, 0, sens_str)
    stdscr.refresh()

    while not __shutdown:
        exp_thr = []
        for i in range(len(exps)):
            exp_thr.append(threading.Thread(target=exps[i].run, name=f'exp{i}'))
            exp_thr[i].start()

        for thr in exp_thr:
            thr.join()

        for i in range(len(sensors)):
            stdscr.addstr(i, max_len, f'{exps[sensors[i]['n']].result[sensors[i]['input']]}')
            stdscr.refresh()
            exps[sensors[i]['n']].cnt += 1

    stdscr.getch()  # Wait for keypress


if __name__ == '__main__':
    keyboard.add_hotkey("F12", shutdown)
    # try:
    #     curses.wrapper(main)
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)

    curses.wrapper(main)
