import curses
import logging
import threading

from deprotocol.app.logger import Logger


class CursesLogHandler(logging.Handler):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def emit(self, record):
        self.setFormatter(Logger.get_logger().handlers[0].formatter)
        self.window.addstr(self.format(record) + '\n')
        self.window.refresh()


class ConsoleUI(threading.Thread):
    """A console for the application."""

    def __init__(self, deprotocol):
        super().__init__()
        self.deprotocol = deprotocol
        self.terminate_flag = threading.Event()

    def shell(self, stdscr):
        try:
            self.loop(stdscr)
        except KeyboardInterrupt:
            Logger.get_logger().error("User requested stopping the protocol, stopping!")
        except Exception as exc:
            Logger.get_logger().error(f"An exception is stopping DeProtocol! ({exc})")
        finally:
            self.deprotocol.on_stop()

    def stop(self):
        self.terminate_flag.set()

    def loop(self, stdscr):
        # Clear the screen and hide the cursor
        stdscr.clear()

        # Calculate the height of the screen and the input window
        sh, sw = stdscr.getmaxyx()
        input_height = 1

        # Define the input window
        input_win = curses.newwin(input_height, sw, sh - input_height - 1, 0)
        input_win.keypad(True)

        # Define the output window
        output_win = curses.newwin(sh - input_height, sw, 0, 0)
        output_win.addstr("Welcome to the shell. Press Ctrl-C to exit.\n")
        output_win.setscrreg(0, sh - input_height - 1)
        output_win.scrollok(True)

        curses_handler = CursesLogHandler(output_win)
        Logger.get_logger().addHandler(curses_handler)

        # Initialize the prompt and command variables
        prompt = '> '
        command = ''

        while not self.terminate_flag.is_set():
            # Print the output window
            input_win.refresh()
            output_win.refresh()

            # Print the prompt and current command in the input window
            input_win.clear()
            input_win.addstr(prompt)
            input_win.addstr(command)

            input_win.refresh()
            output_win.refresh()

            # Get user input
            c = input_win.getch()

            # Process input
            if c == ord('\n'):
                # Handle command
                self.deprotocol.command_handler.handle_command(command)
                command = ''  # clear command
            elif c in [127, curses.KEY_BACKSPACE, 8]:
                # Handle backspace
                command = command[:-1]
                input_win.delch()
            elif c in [3, 26]:  # Ctrl-C
                self.stop()
            else:
                # Add character to command
                command += chr(c)

    def run(self):
        while not self.terminate_flag.is_set():
            try:
                curses.wrapper(self.shell)
            except KeyboardInterrupt:
                Logger.get_logger().error("User requested stopping the protocol, stopping!")
                self.terminate_flag.set()
            except Exception as exc:
                Logger.get_logger().error(f"An exception is stopping DeProtocol! ({exc})")
                self.terminate_flag.set()
        if self.terminate_flag.is_set():
            Logger.get_logger().info("DeProtocol console closed by user, stopping!")
            self.deprotocol.on_stop()
        else:
            Logger.get_logger().info("DeProtocol successfully closed, see you soon!")

