from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import (
    Tk,
    Button,
    Label,
    Frame,
    Canvas,
    BOTH,
    VERTICAL,
    RIGHT,
    LEFT,
    Y
    )
from api import Api
import os

class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.api = Api()
        self.geometry('800x600')
        self.path = os.path.dirname(os.path.dirname(__file__)) + '\\kidkodNotesApp\\staticbase\\media\\'
        self.button = Button(
            self,
            text='Show all ToDos',
            padx=30,
            pady=20,
            command=self.show_todos
        )
        self.button.pack()

    def show_todos(self):
        self.set_window()
        todos = self.api.get_all_todos()['todos']
        for todo in todos:
            title = Label(self.main_frame, text=f"Title: {todo['header']}")
            desc = Label(self.main_frame, text=f"Description: {todo['body']}")
            image_path = todo['image']
            image = Image.open(self.path + image_path)
            display = ImageTk.PhotoImage(image)
            image_label = Label(self.main_frame, image=display)
            image_label.image = display
            title.pack()
            desc.pack()
            image_label.pack()
    
    def set_window(self):
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scroll_bar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.main_frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.main_frame, anchor='nw')

        self.main_frame.bind("<Enter>", self.entered)
        self.main_frame.bind("<Leave>", self.left)

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def entered(self):
        self.canvas.bind_all('<MouseWheel>', self._on_mouse_wheel)

    def left(self):
        self.canvas.unbind_all("<MouseWheel>")
