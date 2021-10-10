import json
import os

def DefaultTheme():
  return {
    "Layout": {
      "Columns": 1,
      "Margin": {
        "x": "0",
        "y": "0"
      },
      "Border": False,
      "Width": "100%",
      "Height": "100%"
    },
    "LineStyle": "┌─┐└┘├┤┬┴┼│",
    "Background": {
      "Default": 0,
      "SecondLine": 8
    },
    "Foreground": -1,
    "Selection": {
      "Fg": 15,
      "Bg": 12,
    },
    "Title": {
      "Fg": 10,
      "Bg": 0,
    },
    "Lines": {
      "Fg": 2,
      "Bg": 0,
    },
    "Input": {
      "Fg": 7,
      "Bg": 0,
    }
  }

class Theme:
  def __init__(self, argv):
    self.path = argv.theme

    theme = DefaultTheme()
    if os.path.isfile(self.path):
      with open(self.path, 'r') as f:
        theme = json.load(f)

    self.cols = int(theme["Layout"]["Columns"])
    self.margin_x = str(theme["Layout"]["Margin"]["x"])
    self.margin_y = str(theme["Layout"]["Margin"]["y"])
    self.border = bool(theme["Layout"]["Border"])
    self.width = str(theme["Layout"]["Width"])
    self.height = str(theme["Layout"]["Height"])
    self.line_style = str((theme["LineStyle"] + "###########")[:11])
    self.bg1 = int(theme["Background"]["Default"])
    self.bg2 = int(theme["Background"]["SecondLine"])
    self.fg = int(theme["Foreground"])
    self.sFg = int(theme["Selection"]["Fg"])
    self.sBg = int(theme["Selection"]["Bg"])
    self.tFg = int(theme["Title"]["Fg"])
    self.tBg = int(theme["Title"]["Bg"])
    self.lFg = int(theme["Lines"]["Fg"])
    self.lBg = int(theme["Lines"]["Bg"])
    self.iFg = int(theme["Input"]["Fg"])
    self.iBg = int(theme["Input"]["Bg"])

    if argv.columns > 0:
      self.cols = argv.columns
    if self.cols < 1:
      self.cols = 1
    if len(argv.line_style) >= 10:
      self.line_style = (argv.linestyle + "##########")[:10]
    if len(argv.width) > 0:
      self.width = argv.width
    if len(argv.height) > 0:
      self.height = argv.height
    if len(argv.margin_x) > 0:
      self.margin_x = argv.margin_x
    if len(argv.margin_y) > 0:
      self.margin_y = argv.margin_y
    if len(argv.border) > 0:
      self.border = bool(argv.border.lower() in ['true','on','yes','1'])

  def getBounds(self, mY, mX):
    w = self.width
    h = self.height
    x = self.margin_x
    y = self.margin_y

    nW = (w + ' ')[1] == '-'
    nH = (h + ' ')[1] == '-'
    nX = (x + ' ')[1] == '-'
    nY = (y + ' ')[1] == '-'
    if nW: w = w[2:]
    if nH: h = h[2:]
    if nX: x = x[2:]
    if nY: y = y[2:]

    pW = ('  ' + w)[-1] == '%'
    pH = ('  ' + h)[-1] == '%'
    pX = ('  ' + x)[-1] == '%'
    pY = ('  ' + y)[-1] == '%'
    if pW: w = w[:-1]
    if pH: h = h[:-1]
    if pX: x = x[:-1]
    if pY: y = y[:-1]

    w = int(w)
    h = int(h)
    x = int(x)
    y = int(y)

    if pW:
      p = w / 100
      if p > 1: p = 1
      w = round(p * mX)
    if pH:
      p = h / 100
      if p > 1: p = 1
      h = round(p * mY)
    if pX:
      p = x / 100
      if p > 1: p = 1
      x = round(p * mX)
    if pY:
      p = y / 100
      if p > 1: p = 1
      y = round(p * mY)

    if nW:
      w = mX - w
    if nH:
      h = mY - h

    return (h, w, y, x)
