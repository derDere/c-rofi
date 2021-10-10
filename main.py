import curses as c
from arguments import Arguments
import sys
import os
import theme
import json
import re
import screen


def mainScreen(stdscr, args, lines):
  t = theme.Theme(args)
  s = screen.Screen(stdscr, args, t, lines)
  s.menu(stdscr)
  #stdscr.addstr('Hello World!\n\n')
  #for l in lines:
  #  stdscr.addstr("%s\n" % l)
  #stdscr.getch()
  return s.result


def printColors(stdscr):
  c.start_color()
  c.use_default_colors()
  for i in range(0, c.COLORS):
    c.init_pair(i + 1, i, -1)
  try:
    for i in range(0, 255):
      stdscr.addstr("%i\t" % (i - 1), c.color_pair(i))
  except c.ERR:
    pass
  stdscr.addstr("\n\nPress any key to exit ...")
  stdscr.getch()


def printModeInfo(args):
  infos = {
    "run":
"""RUN
Description comming soon
""",
    "tmux":
"""TMUX
Description comming soon
""",
    "json":
"""JSON
Description comming soon
""",
    "options":
"""OPTIONS
Description comming soon
"""
  }
  if args.mode_info in infos:
    print(infos[args.mode_info])
  else:
    print("No informations for mode: %s" % args.mode_info)


def cleanLines(lines):
  r = []
  for l in lines:
    l = l.replace("\n", '')
    l = re.sub("^\s+", '', l)
    l = re.sub("\s+$", '', l)
    if len(l) > 0:
      r.append(l)
  return r


def main(args):
  # Print colors if requested
  if args.print_colors:
    c.wrapper(printColors)
    return

  # Save Theme if requestd
  if len(args.save_default_theme) > 0:
    jj = json.dumps(theme.DefaultTheme(), indent=2, sort_keys=True)
    with open(args.save_default_theme, 'w') as f:
      f.write(jj)
    return

  # Print mode info is requested
  if len(args.mode_info) > 0:
    printModeInfo(args)
    return

  # Read lines from stdin if piped
  lines = []
  if not sys.stdin.isatty():
    for line in sys.stdin:
      lines.append(line)

  # stiwch stream for curses to not fup the output/input
  fi = os.open('/dev/tty', os.O_RDWR|os.O_CREAT)
  fo = os.open('/dev/tty', os.O_RDWR|os.O_CREAT)
  os.dup2(fi, 0)
  os.dup2(1, 1000)
  os.dup2(fo, 1)

  # read lines from given files
  for file in args.files:
    with open(file, 'r') as f:
      for line in f:
        lines.append(line)

  # add options to lines
  for opt in args.options:
    lines.append(opt)

  # clean up list
  if args.show != 'json':
    lines = cleanLines(lines)

  result = c.wrapper(mainScreen, args, lines)
  # Write result to original output stream
  os.write(1000, result.encode())


if __name__=="__main__":
  args = Arguments()
  main(args)
