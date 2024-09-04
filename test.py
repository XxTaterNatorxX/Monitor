import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Define buttons
    buttons = ["Button 1", "Button 2", "Button 3", "Button 4"]
    selected = 0

    while True:
        stdscr.clear()
        
        # Display buttons
        for idx, button in enumerate(buttons):
            if idx == selected:
                stdscr.addstr(idx, 0, button, curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, button)
        
        # Get user input
        key = stdscr.getch()

        # Navigate buttons
        if key == ord('w') and selected > 0:
            selected -= 1
        elif key == ord('s') and selected < len(buttons) - 1:
            selected += 1
        elif key == ord('a'):
            stdscr.addstr(len(buttons) + 1, 0, "Left action")
        elif key == ord('d'):
            stdscr.addstr(len(buttons) + 1, 0, "Right action")
        elif key == ord('q'):
            break
        elif key == ord('e'):  # Enter key
            stdscr.clear()
            stdscr.addstr(0, 0, f"Selected: {buttons[selected]}")
            stdscr.refresh()
            stdscr.getch()  # Wait for another key press to exit
            break

        stdscr.refresh()

curses.wrapper(main)
