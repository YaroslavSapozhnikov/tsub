import sys
import curses
import threading
import flash_i2c


def main(stdscr):
    # Clear screen
    stdscr.clear()

    exp = []
    exp_thr = []
    lock = threading.Lock()
    for i in range(3):
        exp.append(flash_i2c.FlashI2C(0x0a+i, lock))
        exp_thr.append(threading.Thread(target=exp[i].run, name=f'exp{i}'))
        exp_thr[i].start()

    # Get input from user
    for i in range(3):
        v = stdscr.getstr(i, 5, 10).decode('utf-8')
        stdscr.addstr(i, 0, f'V{i} = {v}')
        stdscr.refresh()

    # Display results
    stdscr.addstr(8, 0, 'Press any key to exit...')

    stdscr.getch()  # Wait for keypress

    for i in range(3):
        exp_thr[i].join()


if __name__ == '__main__':
    # try:
    #     curses.wrapper(main)
    # except Exception as e:
    #     print(f"Error: {e}")
    #     sys.exit(1)

    curses.wrapper(main)
