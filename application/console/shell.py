import cmd
import curses
import logging
import queue
import sys
import threading

from application.console.curses_handler import CursesHandler
from application.console.log_handler import QueueHandler
from application.logger.logger import Logger
from application.p2p.deprecated_node import Node


class DeShell(cmd.Cmd):
    prompt = '> '

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)

        self.stdscr = None
        self.logwin = None
        self.cmdwin = None

        logger = Logger.get_logger().logger
        logger.addHandler(self.queue_handler)


    def emptyline(self):
        pass

    def do_sayhello(self, args):
        Logger.get_logger().info("Hello!")

    def do_connect(self, args):
        Logger.get_logger().info("connect to: " + args)
        self.node.connect_to(args, 65432)

    def do_msg(self, args):
        message = "msg " + args
        Logger.get_logger().info("sent message: " + message)
        self.node.message(message)

    def do_address(self, args):
        Logger.get_logger().info(f"address: {self.node.onion}")

    def do_exit(self, arg):
        return True

    def precmd(self, line):
        # Put the command into the log queue
        self.log_queue.put(line)
        return line

    def cmd_loop(self):
        while True:
            # Get input from the user
            self.cmdwin.clear()
            self.cmdwin.addstr(self.prompt)
            self.cmdwin.refresh()
            user_input = self.cmdwin.getstr().decode('utf-8')

            # Handle user input
            self.onecmd(user_input)

    def log_loop(self):
        while True:
            try:
                # Get a command from the log queue
                line = self.log_queue.get()

                # Print the command to the log window
                self.logwin.addstr(line + '\n')
                self.logwin.refresh()

                logger = Logger.get_logger().logger
                while not logger.handlers[0].queue.empty():
                    log_record = logger.handlers[0].queue.get()
                    log_message = logger.handlers[0].format(log_record)

                    # Add the log message to the log queue
                    self.log_queue.put(log_message)

            except KeyboardInterrupt:
                break

    def cmdloop(self, *args, **kwargs):
        # Initialize curses
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.echo()
        self.stdscr.keypad(True)

        # Create a window for the logging messages
        height, width = self.stdscr.getmaxyx()
        self.logwin = self.stdscr.subwin(height - 2, width, 0, 0)
        self.logwin.scrollok(False)

        # Create a window for the input commands
        self.cmdwin = self.stdscr.subwin(1, width, height - 1, 0)

        curses_handler = CursesHandler(self.logwin)
        Logger.get_logger().logger.addHandler(curses_handler)

        # Start the logging thread
        log_thread = threading.Thread(target=self.log_loop)
        log_thread.daemon = True
        log_thread.start()

        # Start the command input loop
        self.cmd_loop()


