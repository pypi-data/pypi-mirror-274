import msvcrt
import os
from ..textUtils import textUtils


class Checkmark:
    def __init__(self, text="Please select options:", options=["Option 1", "Option 2", "Option 3"], prefixes=["| 🟩", "| ⬛"]):
        self.options = options
        self.text = textUtils.format("{bold}" + text)
        self.selected_options = [False] * len(options)
        self.prefixes = prefixes

    def display(self):
        option_index = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
            print(self.text)
            for i, option in enumerate(self.options):
                prefix = self.prefixes[0] if self.selected_options[i] else self.prefixes[1]
                prefix_color = "{green}" if i == option_index else "{gray}"
                option_color = "{white}" if i == option_index else "{gray}"
                print(textUtils.format(prefix_color + prefix) + " " + textUtils.format(option_color + option))
            key = msvcrt.getch()
            if key in [b'H', b'P']:  # Up or Down arrow
                if key == b'H':  # Up arrow
                    option_index = (option_index - 1) % len(self.options)
                elif key == b'P':  # Down arrow
                    option_index = (option_index + 1) % len(self.options)
            elif key == b' ':  # Space key
                self.selected_options[option_index] = not self.selected_options[option_index]
            elif key == b'\r':  # Enter key
                return [option for i, option in enumerate(self.options) if self.selected_options[i]]