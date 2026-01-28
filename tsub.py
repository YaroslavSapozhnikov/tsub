import sys
import curses


def main(stdscr):
    # Clear screen
    stdscr.clear()

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


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)