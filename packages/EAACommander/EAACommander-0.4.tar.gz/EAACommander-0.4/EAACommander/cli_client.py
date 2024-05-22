import curses
from art import text2art

try:
    from .settings import load_settings, display_message, settings
except ImportError:
    from settings import load_settings, display_message, settings


TITLE = "EAA Commander"

def check_health(stdscr):
    config = load_settings()
    hostname = config['Server'].get('Hostname', 'astro')
    port = config['Server'].get('Port', '50000')
    message = f"Checking Health...\nHostname: {hostname}\nPort: {port}"
    display_message(stdscr, message)

def find_mode(stdscr):
    display_message(stdscr, "Finding Mode")

def live_stacking_mode(stdscr):
    display_message(stdscr, "Live Stacking Mode")

def confirm_exit(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Do you really want to exit (y/n)? Default is (y): ")
    stdscr.refresh()
    while True:
        choice = stdscr.getch()
        if choice == ord('y') or choice == 10:  # 10 is the Enter key, treated as default 'y'
            return True
        elif choice == ord('n'):
            return False

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    # Generate ASCII art for the title using 'standard' font
    menu_title = text2art(TITLE, font='standard')

    menu_options = [
        "1. Check Health",
        "2. Find Mode",
        "3. Live Stacking Mode",
        "4. Settings",
        "0. Exit"
    ]

    while True:
        stdscr.clear()
        # Display the ASCII art title
        for idx, line in enumerate(menu_title.split("\n")):
            stdscr.addstr(1 + idx, 2, line, curses.A_BOLD)
        
        # Adjust the position of the menu options
        for idx, option in enumerate(menu_options):
            stdscr.addstr(7 + idx, 6, option, curses.A_BOLD)
        
        stdscr.addstr(12, 6, "Enter choice: _")
        stdscr.refresh()
        
        choice = stdscr.getch()
        stdscr.clear()
        if choice == ord('0'):
            if confirm_exit(stdscr):
                break
        elif choice == ord('1'):
            check_health(stdscr)
        elif choice == ord('2'):
            find_mode(stdscr)
        elif choice == ord('3'):
            live_stacking_mode(stdscr)
        elif choice == ord('4'):
            settings(stdscr)
        else:
            display_message(stdscr, "Invalid choice")

def main_entry_point():
    curses.wrapper(main)

if __name__ == "__main__":
    main_entry_point()
