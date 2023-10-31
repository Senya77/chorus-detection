from tkinter import *


class CompareTool:
    def __init__(self, letters):
        self.window = Tk()
        self.window.resizable(False, False)

        self.original_textbox = Text(self.window, font='Arial 12', wrap='word', width=60)
        self.marked_textbox = Text(self.window, font='Arial 12', wrap='word', width=60)

        self.original_textbox.pack(side='left')
        self.marked_textbox.pack(side='right')

        self.marked_textbox.tag_config('red_text', foreground='red')
        self.marked_textbox.tag_config('green_text', foreground='green')

        self.fill_orig(letters)
        self.fill_marked(letters)

        self.window.mainloop()

    def fill_orig(self, letters):
        for i in letters:
            self.original_textbox.insert(END, i.letter)

    def fill_marked(self, letters):
        for i in letters:
            if i.mistake_class == 'TP' or i.mistake_class == 'TN':
                self.marked_textbox.insert(END, i.letter, 'green_text')
            if i.mistake_class == 'FP' or i.mistake_class == 'FN':
                self.marked_textbox.insert(END, i.letter, 'red_text')

