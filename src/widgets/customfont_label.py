import tkinter as tk
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageTk


def truetype_font(font_path: Path, size):
    return ImageFont.truetype(str(font_path.resolve()), size)


class CustomFont_Label(tk.Label):
    def __init__(
        self,
        master,
        text,
        foreground="black",
        truetype_font=None,
        font_path=None,
        family=None,
        size=None,
        **kwargs
    ):
        super().__init__(master, background=master["background"])

        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path cannot be None")

            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)

        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width, height), color=master["background"])
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=truetype_font, fill=foreground)
        self._photoimage = ImageTk.PhotoImage(image)
        self.configure(image=self._photoimage)
