import curses as c
from curses import *
import math


INPUT = 1
TITLE = 2
LINES = 3
SELECTION = 4
OPTIONS1 = 5
OPTIONS2 = 6


class Screen:
  def __init__(self, s, args, theme, lines):
    self.args = args
    self.lines = lines
    self.theme = theme
    self.result = ""
    self.colX = []
    self.colW = []
    self.title = ":"

    if len(args.title) > 0:
      self.title = args.title

    c.curs_set(0)
    c.start_color()
    c.use_default_colors()
    c.init_pair(INPUT, theme.iFg, theme.iBg)
    c.init_pair(TITLE, theme.tFg, theme.tBg)
    c.init_pair(LINES, theme.lFg, theme.lBg)
    c.init_pair(SELECTION, theme.sFg, theme.sBg)
    c.init_pair(OPTIONS1, theme.fg, theme.bg1)
    c.init_pair(OPTIONS2, theme.fg, theme.bg2)

    self.w = c.newwin(10, 10, 10, 10)
    self.reprintFullWindow(s)

  def reprintFullWindow(self, s):
    mY, mX = s.getmaxyx()

    minW = self.theme.cols * 2 - 1
    minH = 3
    if self.theme.border:
      minW += 2
      minH += 2

    h, w, y, x = self.theme.getBounds(mY, mX)

    if h < minH: h = minH
    if w < minW: w = minW

    self.w.mvwin(y, x)
    self.w.resize(h, w)

    L_TL = self.theme.line_style[ 0]
    L_HL = self.theme.line_style[ 1]
    L_TR = self.theme.line_style[ 2]
    L_BL = self.theme.line_style[ 3]
    L_BR = self.theme.line_style[ 4]
    L_CL = self.theme.line_style[ 5]
    L_CR = self.theme.line_style[ 6]
    L_CT = self.theme.line_style[ 7]
    L_CB = self.theme.line_style[ 8]
    L_CM = self.theme.line_style[ 9]
    L_VL = self.theme.line_style[10]

    self.w.border()

    # Draw Lines
    self.w.attron(c.color_pair(LINES))
    if self.theme.border:
      self.w.addstr(0, 0, L_TL + (L_HL * (w - 2)) + L_TR)
      self.w.addstr(1, 0, L_VL)
      self.w.addstr(1, w - 1, L_VL)
      self.w.addstr(2, 0, L_CL + (L_HL * (w - 2)) + L_CR)
      for y in range(3, h - 1):
        self.w.addstr(y, 0, L_VL)
        self.w.addstr(y, w - 1, L_VL)
      self.w.addstr(h - 1, 0, L_BL + (L_HL * (w - 2)))
      try:
        self.w.addch(h-1,w-1,L_BR)
      except Exception:
        pass
    else:
      self.w.addstr(1, 0, L_HL * w)

    # Draw Columns and fill col XWs
    colStart = 1
    colOff = 0
    colBot = L_VL
    colSub = 0
    if self.theme.border:
      colOff = 1
      colStart = 2
      colBot = L_CB
      colSub = 2
    colW = ((w - colSub) - (self.theme.cols - 1)) / self.theme.cols
    self.colX = []
    self.colW = []
    for y in range(colStart, h):
      for i in range(self.theme.cols):
        x = round(i * (colW + 1) + colOff)
        if y == colStart:
          if i == 0:
            self.colX.append(x)
          else:
            self.colX.append(x + 1)
        if i != 0:
          if y == colStart:
            self.w.addstr(y, x, L_CT)
          elif y == h-1:
            self.w.addstr(y, x, colBot)
          else:
            self.w.addstr(y, x, L_VL)
    if self.theme.border:
      self.colX.append(w)
    else:
      self.colX.append(w + 1)
    for i in range(len(self.colX) - 1):
      x = self.colX[i]
      w = self.colX[i+1] - x
      self.colW.append(w - 1)
    #for i in range(len(self.colX) - 1):
    #  x = self.colX[i]
    #  w = self.colW[i]
    #  self.w.addstr(4, x, str(i) * w)
    self.w.attroff(c.color_pair(LINES))

    # Draw Title
    title_off = 0
    if self.theme.border:
      title_off = 1
    self.w.addstr(title_off, title_off, self.title, c.color_pair(TITLE))

  def menu(self, s):
    #self.w.addstr("HW!\n\n")
    #for l in self.lines:
    #  self.w.addstr("%s\n" % l)
    self.w.getch()
    self.result = "ROFLMAO"
