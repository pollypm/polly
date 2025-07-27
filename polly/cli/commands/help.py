import os

def hex_to_ansi(hex_color):
  hex_color = hex_color.lstrip('#')
  r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
  return f'\033[38;2;{r};{g};{b}m'

RESET = '\033[0m'

PRIMARY_COLOR = '#4F8EF7'    # Example: blue
SECONDARY_COLOR = '#F7B32B'  # Example: orange

def read_ascii_art(file_path):
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      return f.read()
  except FileNotFoundError:
    return "[ASCII art not found]"

def display_help():
  ascii_art_path = os.path.join(os.path.dirname(__file__), '../polly.txt')
  ascii_art = read_ascii_art(ascii_art_path)

  help_text = """{p}Polly {g}- {s}Help
{g}Version 1.0.0

{s}Usage:
  {p}polly {g}<command> [options]

{s}Available Commands:
  {p}help        {g}Show this help message
  {p}install     {g}Install a Polly package
  {p}uninstall   {g}Uninstall a Polly package
  {p}list        {g}List installed Polly packages
  {p}search      {g}Search for Polly packages
  {p}inspect     {g}Show information about a Polly package
  {p}upgrade     {g}Upgrade Polly packages

{s}For more information, visit: {p}https://github.com/pollypm/polly
"""

  art_lines = ascii_art.splitlines()
  help_lines = help_text.splitlines()

  max_lines = max(len(art_lines), len(help_lines))
  art_lines += [''] * (max_lines - len(art_lines))
  help_lines += [''] * (max_lines - len(help_lines))

  spacing = '   '
  primary_color = hex_to_ansi(PRIMARY_COLOR)
  secondary_color = hex_to_ansi(SECONDARY_COLOR)
  grey_color = hex_to_ansi('#808080')

  print("\n\n", end="")
  for art, help_line in zip(art_lines, help_lines):
    help_line = help_line.replace('{p}', primary_color).replace('{s}', secondary_color).replace('{g}', grey_color)
    print(f"  {art:<40}{RESET}{spacing}{help_line}{RESET}")
  print("\n\n", end="")

if __name__ == "__main__":
  display_help()