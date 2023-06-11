import tkinter as tk
from tkinter import ttk

from gamedetector.game_detect import NonSteamGame, SteamGame


class GameTreeView(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.tree = ttk.Treeview(self)
        self.tree.bind('<ButtonRelease-1>', master.master.find_game_to_show)

        ysb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

        self.tree.configure(
            columns=(
                "game_appid",
                "game_name",
                "game_version",
            )
        )

        self.tree.heading("game_appid", text="AppId")
        self.tree.heading("game_name", text="Name")
        self.tree.heading("game_version", text="Version")

        self.tree['show'] = 'headings'  # only show columns with headings

        ysb.pack(side="right", anchor="ne", fill="y")
        xsb.pack(side="bottom", anchor="sw", fill="x")

        self.tree.pack(side="top", anchor="center", fill="both", expand=True)

    def insert_game(self, game: SteamGame | NonSteamGame):
        if isinstance(game, SteamGame):
            self.tree.insert("", tk.END, values=(game.appid, game.name, game.version))
        elif isinstance(game, NonSteamGame):
            self.tree.insert("", tk.END, values=("", game.name, game.version))
        else:
            raise Exception(f"Cannot insert_game, bad game type: {type(game)}")
