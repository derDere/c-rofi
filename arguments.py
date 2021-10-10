from argparse import *


def Arguments():
  modi = [ 'run', 'tmux', 'json', 'options' ]

  parser = ArgumentParser(description="Bla Bla")

  parser.add_argument('files', metavar='file', type=str, nargs='*',
                      help='Files containing the options to select. File content can be used additional to piping.')

  parser.add_argument('-t', '--title', metavar='title', type=str, default='',
                      help='Defines the title shown at the top of the menu. (Default is :)')

  parser.add_argument('--option-align', metavar='align', choices=['L','C','R'], default='',
                      help='Defines the text alignment for the options. (Default is L)')

  parser.add_argument('--title-align', metavar='align', choices=['L','C','R'], default='',
                      help='Defines hot the input and title is aligned at the top of the menu. (Default is L)')

  parser.add_argument('-c', '--columns', type=int, default=0, metavar='columncount',
                      help='Defines the number of columns to display the options in. (default is 1)')

  parser.add_argument('-o', '--options', type=str, metavar='opt', nargs='*', default=[],
                      help='Additional options to add into selection.')

  parser.add_argument('--line-style', type=str, metavar='style', default='',
                      help='Changes the characters used to display lines. (default is ┌─┐└┘├┤┬┴┼│)')

  parser.add_argument('--width', type=str, metavar='W', default='',
                      help='Defines the width used to display the content. You can use fixed values like W=20 to define a width of 20 chars. You can also use percentages like W=50%% or you can use negative values to subtract from the window maxwidth. Keeping the argument syntax, negative values have to start with a one letter folowed by the minus. If you use for example "W-20" the menu will keep being 20 chars less then the max width even if it gets resized. You can also combine percentage an negatve values for example "W-5%%". (default is 100%%)')

  parser.add_argument('--height', type=str, metavar='H', default='',
                      help='Same usage as --width except it\'s for the height. (default is 100%%)')

  parser.add_argument('--margin-x', type=str, metavar='MX', default='',
                      help='This will add a margin to the outer left side of the menu. Similar usage as --width and --height except no negative values. (default is 0)')

  parser.add_argument('--margin-y', type=str, metavar='MY', default='',
                      help='Same as --margin-x except it\'s for the top outer side.')

  parser.add_argument('--border', default="", choices=['1', 'true', 'yes', 'on', '0', 'false', 'no', 'off'], metavar='bool',
                      help='Adds a border around the menu. The border will move according to the margin and width and height.')

  parser.add_argument('-s', '--show', choices=modi, default='options', metavar='mode',
                      help='Run c-rofi in a specific mode. Options are: %s.' % (', '.join(modi)))

  parser.add_argument('--mode-info', choices=modi, metavar='mode', default='',
                      help='Displays more information about the given mode.')

  parser.add_argument('--theme', type=str, metavar='themefile', default='~/.config/c-rofi/default.json',
                      help='Switches the color file to a given path. Defining different colors to use. (default is ~/.config/c-rofi/colors.json) You can use --save-default-colors to get an example.')

  parser.add_argument('--save-default-theme', type=str, metavar='outputfile', default='',
                      help='Saves the default theme file to a given path.')

  parser.add_argument('--search', type=str, metavar='command',
                      help='Define a command to return options after each new inserted char. the run mode for example uses "compgen -c %%s".')

  parser.add_argument('--print-colors', default=False, const=True, action='store_const',
                      help='Prints all available color codes to your terminal.')
  #compgen -c vi

  args = parser.parse_args()
  return args
