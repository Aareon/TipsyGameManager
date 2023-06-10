import tkinter as tk
from pathlib import Path
from queue import Queue
from threading import Thread
from tkinter import filedialog, ttk
from src.widgets.gameframe import GameFrame
from src.widgets.lazyfiletree import LazyFileTree

from gamedetector.game_detect import detect_folder


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs) -> tk.Frame:
        super().__init__(*args, **kwargs)

        self.frame = tk.Frame(self)

        # TODO: open config file and get managed folders for saved states

        self.managed_folder = Path()
        self.select_managed_folder()  # get user selection

        self.managed_game_folders = []

    def delete_frame_widgets(self):
        # TODO make this a decorator for making more one-off windows
        for widget in self.frame.winfo_children():
            widget.destroy()
        if hasattr(self, "done_button"):
            self.done_button.destroy()
        print("Cleaned up `self.frame`")

    def select_managed_folder(self):
        """Window to prompt the user to select a games library folder to manage."""
        self.delete_frame_widgets()
        label = tk.Label(
            self.frame,
            text="Select a game library folder. This folder should contain a number of games.\n"
            "You can add more folders to manage later.",
        )
        label.pack(side="top", anchor="center")

        self.folder_entry = tk.Entry(self.frame)
        self.folder_entry.pack(
            side="left", anchor="nw", fill="x", expand=True, padx=10, pady=10
        )

        folder_button = tk.Button(
            self.frame,
            text="Select Folder",
            command=self.folder_dialog_command,
            height=1,
        )
        folder_button.pack(side="top", anchor="e", pady=10)

        self.done_button = tk.Button(
            self, text="Next", command=self.show_library_window
        )
        self.done_button.pack(side="bottom", anchor="s", pady=10, ipadx=4)
        self.frame.pack()

    def folder_dialog_command(self) -> None:
        """Command used by `folder_button`.
        Opens a filedialog folder select dialog and sets `self.managed_folder`

        Args:
            None
        Returns:
            None"""
        folder = filedialog.askdirectory(mustexist=True)
        self.managed_folder = Path(folder) if folder != "" else Path()
        if folder != "":
            # update entrybox
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, str(self.managed_folder.resolve()))
            print(f"Selected folder to manage: {folder}")
        else:
            print("Did not select folder to manage.")

    def add_game_to_tree(self, game_folder, game_name):
        game = {
            "folder": game_folder,
            "name": game_name,
        }
        if game not in self.managed_game_folders:
            self.managed_game_folders.append(game)
            self.file_tree.insert_node("", game_name, "")

    def parse_game_folders(self, library_path: Path) -> str:
        progress_bar = self.progress_bar
        q = Queue()
        for fp in library_path.iterdir():
            if fp.is_dir():
                q.put(fp)

        def target():
            while not q.empty():
                game_folder = q.get(block=True)
                game_name = detect_folder(game_folder)
                self.add_game_to_tree(game_folder, game_name)
            progress_bar.stop()

        thread = Thread(target=target)
        thread.start()

    def show_library_window(self):
        if self.managed_folder == Path("."):
            return

        self.delete_frame_widgets()
        self.geometry("600x600")

        self.file_tree = LazyFileTree(self.frame)
        self.file_tree.pack(side="top", anchor="nw", fill="both", expand=True)

        game_frame = GameFrame(self.frame, relief="sunken", bg="gray", border=2)
        game_frame.pack(side="top", anchor="nw", fill="both", expand=True)

        self.progress_bar = ttk.Progressbar(
            game_frame, orient="horizontal", mode="indeterminate", length=100
        )
        self.progress_bar.pack(side="bottom", anchor="sw", fill="x", expand=True)

        self.frame.pack(fill="both", expand=True)

        # start checking game folders
        self.progress_bar.start()
        self.parse_game_folders(self.managed_folder)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
