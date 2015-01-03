import subprocess
from subprocess import CalledProcessError

from i3pystatus import IntervalModule


class KeyboardLayout(IntervalModule):
    """
    Shows the current keyboard layout and allows the layout to be changed by
    scrolling. It requires setxkbmap.

    Formatters:
        {layout} : the base layout name (usually two-letter code like `us`)
        {variant} : variant of the layout (e.g. `qwertz` vs. `qwerty`)
    """

    interval = 1

    settings = (
        ("format", "Format string used for output."),
        ("layouts", "List of layouts."),
        ("color", "Standard color."),
    )

    format = "kbd: {layout} {variant}"
    layouts = ["us", "de qwerty"]
    color = "#FFFFFF"
    fdict = {}
    current_index = 0

    on_leftclick = "next_layout"

    def run(self):
        layout_strings = self.layouts[self.current_index].split(" ")
        self.fdict['layout'] = ''
        self.fdict['variant'] = ''
        if len(layout_strings) > 0:
            self.fdict['layout'] = layout_strings[0]
        if len(layout_strings) > 1:
            self.fdict['variant'] = layout_strings[1]

        full_text = self.format.format(**self.fdict)
        self.output = {
            "full_text": full_text,
            "color": self.color,
        }

    def set_layout(self, layout):
        command = ["setxkbmap"]
        command.extend(layout.split(" "))
        try:
            subprocess.check_call(command)
        except CalledProcessError as e:
            # invalid layout string
            pass
        except OSError as e:
            # setxkbmap not installed
            pass 

    def next_layout(self):
        i = self.current_index + 1
        if i >= len(self.layouts):
            i = 0

        self.current_index = i

        self.set_layout(self.layouts[self.current_index])

