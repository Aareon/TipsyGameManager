import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk


class LazyFileTree(tk.Frame):
    def __init__(self, parent: tk.Tk, path: Path = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._path = path

        self.nodes = dict()
        self.tree = ttk.Treeview(self)

        ysb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        xsb = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading("#0", text="Library Games", anchor="w")

        self.tree.pack(side="top", anchor="nw", fill="both", expand=True)

        ysb.pack(side="right", anchor="ne", fill="y")

        xsb.pack(side="bottom", anchor="sw", fill="x")

        if self._path is not None:
            abspath = os.path.abspath(path)
            self.insert_node("", abspath, abspath)
            self.tree.bind("<<TreeviewOpen>>", self.open_node)

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, value: Path) -> None:
        if isinstance(value, Path):
            self._path = value
        else:
            raise TypeError(f"`path` must be type `pathlib.Path`, not `{type(value)}`.")

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, "end", text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, "end")

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))
