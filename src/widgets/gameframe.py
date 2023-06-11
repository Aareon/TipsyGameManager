import logging
import tkinter as tk
from pathlib import Path

from gamedetector.game_detect import NonSteamGame, SteamGame

# from src.widgets.customfont_label import CustomFont_Label, truetype_font

RES_PATH = Path("__file__").parent.parent / "res"


# try:
# GIDOLE_18 = truetype_font(RES_PATH / "Gidole-Regular.ttf", 18)
# GIDOLE_12 = truetype_font(RES_PATH / "Gidole-Regular.ttf", 12)
# except OSError:
# logging.error(
# f"Failed to open {str((RES_PATH / 'Gidole-Regular.ttf').resolve())}",
# exc_info=True,
# )
# raise

NL = "\n"
TAB = "\t"


class GameFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master

        # self.game_image = tk.Image()
        # self.game_image.pack(side="top", anchor="nw", padx=10)

        self._no_game = NonSteamGame(
            name="No game selected",
            publisher=None,
            version="N/A",
            description="When you select a game, this will be populated with game info.",
            path=None,
        )
        self.set_game(self._no_game)

    def set_game(self, game: SteamGame | NonSteamGame) -> None:
        logging.debug(f"Showing game: {game}")
        try:
            # Cleanup widgets used for different game
            self.name_label.destroy()
            self.version_label.destroy()
            self.description_label.destroy()
            self.button_frame.destroy()
        except AttributeError:
            pass

        # self.name_label = CustomFont_Label(
        # self, text=game.name, truetype_font=GIDOLE_18
        # )
        self.name_label = tk.Label(self, text=game.name, font=("SegoeUI-Semibold", 18))
        self.name_label.pack(side="top", anchor="center")

        # self.version_label = CustomFont_Label(
        # self, text=f"Version: {game.version}", truetype_font=GIDOLE_12
        # )
        self.version_label = tk.Label(
            self, text=f"Version: {game.version}", font=("SegoeUI-Historic", 12)
        )
        self.version_label.pack(side="left", anchor="n")

        if hasattr(game, "description") and game.description is not None:
            # self.description_label = CustomFont_Label(
            # self,
            # text=f"Description: {game.description}",
            # truetype_font=GIDOLE_12,
            # )
            self.description_label = tk.Label(
                self,
                text=f"Description: {NL}{game.description}"
                if game.description is not None
                else "",
                font=("SegoeUI-Semibold", 12),
                wraplength=400,
                justify="center",
            )
            self.description_label.pack(side="top", anchor="center", fill="x")

        if game.path is not None:
            # create a frame that will let our buttons align correctly
            self.button_frame = tk.Frame(self, background=self["background"])

            self.play_button = tk.Button(self.button_frame, text="Play", border=2, background="green", font=("SegoeUI-Semibold", 14))
            self.play_button.pack(side="top", anchor="center")

            self.settings_button = tk.Button(self.button_frame, text="Settings", border=1, font=("SegoeUI-Semibold", 10))
            self.settings_button.pack(side="right", anchor="ne")

            self.button_frame.pack(side="top", anchor="center", fill="both", expand=True)
