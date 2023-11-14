from tkinter import *


class CompareTool:
    def __init__(self, letters):
        self.window = Tk()
        self.window.resizable(False, False)

        self.input_textbox = Text(self.window, font='Arial 11', wrap='word', width=50)
        self.original_textbox = Text(self.window, font='Arial 11', wrap='word', width=50)
        self.marked_textbox = Text(self.window, font='Arial 11', wrap='word', width=50)

        self.input_textbox.pack(side='left')
        self.original_textbox.pack(side='left')
        self.marked_textbox.pack(side='left')

        self.marked_textbox.tag_config('red_text', foreground='red')
        self.marked_textbox.tag_config('green_text', foreground='green')
        self.marked_textbox.tag_config('blue_text', foreground='blue')

        self.original_textbox.tag_config('red_text', foreground='red')
        self.original_textbox.tag_config('green_text', foreground='green')
        self.original_textbox.tag_config('blue_text', foreground='blue')

        self.fill_input(letters)
        self.fill_marked(letters)
        self.fill_orig(letters)

        self.window.mainloop()

    def fill_input(self, letters):
        for i in letters:
            self.input_textbox.insert(END, i.letter)

    def fill_orig(self, letters):
        for i in range(len(letters)):
            if letters[i-1].real_section != letters[i].real_section:
                self.original_textbox.insert(END, '\n')
            if letters[i].real_section == 'c':
                self.original_textbox.insert(END, letters[i].letter, 'green_text')
            if letters[i].real_section == 'n':
                self.original_textbox.insert(END, letters[i].letter, 'blue_text')

    def fill_marked(self, letters):
        for i in letters:
            if i.mistake_class == 'TP' or i.mistake_class == 'TN':
                if i.predicted_section == 'c':
                    self.marked_textbox.insert(END, i.letter, 'green_text')
                if i.predicted_section == 'n':
                    self.marked_textbox.insert(END, i.letter, 'blue_text')
            if i.mistake_class == 'FP' or i.mistake_class == 'FN':
                self.marked_textbox.insert(END, i.letter, 'red_text')
