import _curses
import curses as c
from curses import *
import math


INPUT = 1
TITLE = 2
LINES = 3
SELECTION = 4
OPTIONS1 = 5
OPTIONS2 = 6


class Option:
  def __init__(self, screen, name, value):
    self.screen = screen
    self.w = screen.w
    self.name = name
    self.value = value
    self.index = 0
    self.selected = False

  def draw(self, index):
    self.index = index

    mY, _ = self.w.getmaxyx()
    mY -= 2
    if self.screen.theme.border:
      mY -= 2

    y = (self.index % mY) + 2
    if self.screen.theme.border: y += 1
    col = self.index // mY
    x = self.screen.colX[col]
    w = self.screen.colW[col]

    if self.selected:
      color = SELECTION
    elif index % 2 == 1:
      color = OPTIONS2
    else:
      color = OPTIONS1

    if self.screen.theme.option_align == "C":
      leftOver = w - len(self.name)
      frontM = leftOver // 2
      backM = w - frontM
      displayname = ((' ' * frontM) + self.name + (' ' * backM))[:w]
    elif self.screen.theme.option_align == "R":
      displayname = ((" " * w) + self.name)[-w:]
    else:
      displayname = (self.name + (" " * w))[:w]

    try:
      self.w.addstr(y, x, displayname, c.color_pair(color))
    except _curses.error as ce:
      if str(ce) != "addwstr() returned ERR":
        raise ce


class Screen:
  def __init__(self, s, args, theme, lines):
    self.args = args
    self.lines = lines
    self.theme = theme
    self.result = ""
    self.colX = []
    self.colW = []
    self.title = ":"
    self.input = ""

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

  def drawTopLine(self):
    _, w = self.w.getmaxyx()
    titleOff = 0
    if self.theme.border:
      w -= 2
      titleOff = 1

    if self.theme.title_align == "C":
      titleLen = len(self.title)
      inputLen = len(self.input)
      half1 = w // 2
      if titleLen > half1: titleLen = half1
      half2 = w - titleLen
      if inputLen > half2: inputLen = half2
      leftOver = w - titleLen - inputLen
      frontM = leftOver // 2
      backM = leftOver - frontM
      self.w.addstr(titleOff, titleOff, ((' ' * frontM) + self.title)[-(titleLen + frontM):], c.color_pair(TITLE))
      self.w.addstr((self.input + (' ' * backM))[-(inputLen + backM):], c.color_pair(INPUT))

    elif self.theme.title_align == "R":
      inputLen = len(self.input)
      if inputLen > w:
        inputLen = w
      leftSide = w - inputLen
      if leftSide < 5:
        leftSide = 5
      titleLen = len(self.title)
      if titleLen > leftSide:
        titleLen = leftSide
      rightSide = w - leftSide
      if rightSide > inputLen:
        rightSide = inputLen
      self.w.addstr(titleOff, titleOff, ((' ' * (leftSide)) + self.title)[-leftSide:], c.color_pair(TITLE))
      self.w.addstr(self.input[-rightSide:], c.color_pair(INPUT))

    else:
      inputLen = len(self.input)
      if inputLen > w:
        inputLen = w
      leftOver = w - inputLen
      if leftOver < 5:
        leftOver = 5
      titleLen = len(self.title)
      if titleLen > leftOver:
        titleLen = leftOver
      leftOver = w - titleLen
      if inputLen > leftOver:
        inputLen = leftOver
      leftSide = w - titleLen - inputLen
      self.w.addstr(titleOff, titleOff, self.title[-titleLen:], c.color_pair(TITLE))
      self.w.addstr((self.input + (' ' * leftSide))[-leftOver:], c.color_pair(INPUT))

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
      except _curses.error as ce:
        if str(ce) != "add_wch() returned ERR":
          raise ce
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
    colH = h - 2
    if self.theme.border:
      self.colX.append(w)
      colH -= 2
    else:
      self.colX.append(w + 1)
    for i in range(len(self.colX) - 1):
      x = self.colX[i]
      w = self.colX[i+1] - x
      self.colW.append(w - 1)
    self.w.attroff(c.color_pair(LINES))

    # Draw Title
    self.drawTopLine()

    # Redraw Options
    opt = Option(self, "name", "val")
    opt.selected = True
    for i in range(self.theme.cols * colH):
      opt.draw(i)
      opt.selected = False

  def menu(self, s):
    #self.w.addstr("HW!\n\n")
    #for l in self.lines:
    #  self.w.addstr("%s\n" % l)
    self.w.getch()
    self.result = "ROFLMAO"
