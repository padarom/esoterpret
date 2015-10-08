import curses

class InteractiveCLI:
	_screen = None

	def __init__(self):
		self._screen = curses.initscr()	

		curses.start_color()	# Working w/ colors
		curses.noecho()			# Don't echo
		curses.cbreak()			# Breaks
		curses.curs_set(False)	# Don't show cursor

	def unset(self):
		curses.nocbreak()
		self._screen.keypad(0)
		curses.echo()
		curses.endwin()

	def menu(self):
		screen = self._screen

		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
		screen.keypad(1)
		pos = 1
		x = None
		h = curses.color_pair(1)
		n = curses.A_NORMAL

		options = ["1 - Show Help", "2 - Execute Program", "3 - Exit"]
		while x != ord('q'):
			screen.clear()
			screen.border()
			screen.addstr(2, 3, "ESOTERPRET", curses.A_STANDOUT)
			screen.addstr(3, 3, "Interactive CLI Interpreter for esoteric programming languages.")
			screen.addstr(5, 3, "Please select an option.", curses.A_BOLD)

			for index, option in enumerate(options):
				color = h if (pos - 1) == index else n
				screen.addstr(index + 6, 4, option, color);

			x = screen.getch()
			if   x == curses.KEY_DOWN:
				pos += 1
				if pos > len(options):
					pos = 1

			elif x == curses.KEY_UP:
				pos -= 1
				if pos < 1:
					pos = len(options)