import colorama

from colorama import Fore, Back, Style


class Colors:
    """A utility collection of custom terminal coloring."""

    def __init__(self):
        # Setup Console & Attributes
        colorama.just_fix_windows_console()
        self.default_color = Fore.LIGHTGREEN_EX

        # Update Default Console Color
        print(self.default_color)

    def print_colored(self, text: str, color: str, end: str='\n') -> None:
        """Print a custom colored text."""
        print(color + text + self.default_color, end=end)

    def print_success(self, text: str, end: str='\n') -> None:
        """Print a cyan colored text."""
        print(Fore.LIGHTCYAN_EX + text + self.default_color, end=end)

    def print_warning(self, text: str, end: str='\n') -> None:
        """Print a yellow colored text."""
        print(Fore.LIGHTYELLOW_EX + text + self.default_color, end=end)

    def print_error(self, text: str, end: str='\n') -> None:
        """Print a red colored text."""
        print(Fore.LIGHTRED_EX + text + self.default_color, end=end)

    def input(self, string: str) -> str:
        """Input statement with a white input text."""
        user_input = input(string + Fore.LIGHTWHITE_EX)
        print(self.default_color, end='')

        return user_input

    def reset(self) -> None:
        """Reset the color of the console."""
        print(Fore.RESET)
        print(Back.RESET)
        print(Style.RESET_ALL)
