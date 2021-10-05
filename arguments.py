from argparse import *


def Arguments():
  modi = [ 'run', 'tmux', 'json' ]

  parser = ArgumentParser(description="Bla Bla")

  parser.add_argument('files', metavar='file', type=str, nargs='*',
                      help='Files containing the options to select. File content can be used additional to piping.')

  parser.add_argument('-c', '--columns', type=int, default=1, metavar='N',
                      help='Defines the number (N) of columns to display the options in. (default is N=1)')

  parser.add_argument('-o', '--options', type=str, metavar='opt', nargs='*', default=[],
                      help='Additional options to add into selection.')

  parser.add_argument('--line-style', type=str, metavar='style', default='┌─┐└┘├┤┬┴┼│',
                      help='Changes the characters used to display lines. (default is ┌─┐└┘├┤┬┴┼│)')

  parser.add_argument('--width', type=str, metavar='W', default='100%%',
                      help='Defines the width used to display the content. You can use fixed values like W=20 to define a width of 20 chars. You can also use percentages like W=50%% or you can use negative values to subtract from the window maxwidth. If you use for example W=-20 the menu will keep being 20 chars less then the max width even if it gets resized. (default is 100%%)')

  parser.add_argument('--height', type=str, metavar='H', default='100%%',
                      help='Same usage as --width except it\'s for the height. (default is 100%%)')

  parser.add_argument('--margin-x', type=str, metavar='MX', default='0',
                      help='This will add a margin to the outer left side of the menu. Similar usage as --width and --height except no negative values. (default is 0)')

  parser.add_argument('--margin-y', type=str, metavar='MY', default='0',
                      help='Same as --margin-x except it\'s for the top outer side.')

  parser.add_argument('--border', default=False, const=True, action='store_const',
                      help='Adds a border around the menu. The border will move according to the margin and width and height.')

  parser.add_argument('-s', '--show', choices=modi, default='options', metavar='mode',
                      help='Run c-rofi in a specific mode. Options are: %s.' % (', '.join(modi)))

  parser.add_argument('--mode-info', choices=modi, default=None, metavar='mode',
                      help='Displays more information about the given mode.')

  parser.add_argument('--color-config', type=str, metavar='colorfile', default='~/.config/c-rofi/colors.json',
                      help='Switches the color file to a given path. Defining different colors to use. (default is ~/.config/c-rofi/colors.json) You can use --save-default-colors to get an example.')

  parser.add_argument('--save-default-colors', type=str, metavar='outputfile',
                      help='Saves the default color file to a given path.')

  parser.add_argument('--search', type=str, metavar='command',
                      help='Define a command to return options after each new inserted char. the run mode for example uses "compgen -c %%s".')
  #compgen -c vi

  args = parser.parse_args()
  return args
