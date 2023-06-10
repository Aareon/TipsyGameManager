import tkinter as tk
from pathlib import Path

from src.models import Game
from src.widgets.customfont_label import CustomFont_Label, truetype_font

RES_PATH = Path("__file__").parent.parent / "res"

GIDOLE_18 = truetype_font(RES_PATH / "Gidole-Regular.ttf", 18)
GIDOLE_12 = truetype_font(RES_PATH / "Gidole-Regular.ttf", 12)


class GameFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # self.game_image = tk.Image()
        # self.game_image.pack(side="top", anchor="nw", padx=10)

        self.name_label = CustomFont_Label(
            self, text="No game selected", truetype_font=GIDOLE_18
        )
        self.name_label.pack(side="top", anchor="center")

        self.version_label = CustomFont_Label(
            self, text="Version:", truetype_font=GIDOLE_12
        )
        self.version_label.pack(side="left", anchor="n")

        self.description_label = CustomFont_Label(
            self,
            text="Description: When you select a game, this will be populated with game info.",
            truetype_font=GIDOLE_12,
        )
        self.description_label.pack(side="top", anchor="center")
