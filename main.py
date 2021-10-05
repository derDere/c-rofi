import curses as c
from arguments import Arguments
import sys
import os


def mainScreen(stdscr, args):
  stdscr.addstr('Hello World!')
  stdscr.getkey()
  return "ROFL"


def main(args):
  lines = []
  for line in sys.stdin:
    lines.append(line)
  fi = os.open('/dev/tty', os.O_RDWR|os.O_CREAT)
  fo = os.open('/dev/tty', os.O_RDWR|os.O_CREAT)
  os.dup2(fi, 0)
  os.dup2(1, 1000)
  os.dup2(fo, 1)
  result = c.wrapper(mainScreen, args)
  os.write(1000, (str(lines) + ' ' + result).encode())


if __name__=="__main__":
  args = Arguments()
  main(args)
