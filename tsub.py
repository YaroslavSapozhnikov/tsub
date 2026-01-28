import sys
import curses
import threading
import flash_i2c


def main(stdscr):
    # Clear screen
    stdscr.clear()

    exp = []
    exp_thr = []
    for i in range(3):
        exp.append(flash_i2c.FlashI2C(0x0a+i))
        exp_thr.append(threading.Thread(target=exp[i].run, name=f'exp{i}'))
        exp_thr[i].start()

    # Prompt user
    stdscr.addstr(0, 0, 'V1 = ')
    stdscr.addstr(1, 0, 'V2 = ')
    stdscr.addstr(2, 0, 'V3 = ')

    # Get input from user
    v1 = stdscr.getstr(0, 5, 10).decode('utf-8')
    stdscr.addstr(0, 0, f'V1 = {v1}')
    stdscr.refresh()
    v2 = stdscr.getstr(1, 5, 10).decode('utf-8')
    stdscr.addstr(1, 0, f'V2 = {v2}')
    stdscr.refresh()
    v3 = stdscr.getstr(2, 5, 10).decode('utf-8')
    stdscr.addstr(2, 0, f'V3 = {v3}')
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
