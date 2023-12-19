from tkinter import *
from tkinter import ttk
from metrics import accuracy, precision, recall, F_score


class CompareTool(Toplevel):
    def __init__(self, parent, song, language):
        super().__init__(parent)
        self.resizable(False, False)

        self.metrics_frame = Frame(self)

        self.accuracy_label = ttk.Label(self.metrics_frame, text='Accuracy:', font='Arial 11')
        self.accuracy_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')
        self.recall_label = ttk.Label(self.metrics_frame, text='Recall:', font='Arial 11')
        self.recall_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')
        self.precision_label = ttk.Label(self.metrics_frame, text='Precision:', font='Arial 11')
        self.precision_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')
        self.f_score_label = ttk.Label(self.metrics_frame, text='F-score', font='Arial 11')
        self.f_score_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')

        self.legend_frame = Frame(self)
        self.TP_label = ttk.Label(self.legend_frame, font='Arial 11')
        self.TN_label = ttk.Label(self.legend_frame, font='Arial 11')
        self.false_label = ttk.Label(self.legend_frame, font='Arial 11')
        self.TP_label.pack(side='top')
        self.TN_label.pack(side='top')
        self.false_label.pack(side='top')

        self.accuracy_label.grid(column=0, row=0)
        self.accuracy_counter_label.grid(column=1, row=0)
        self.recall_label.grid(column=0, row=1)
        self.recall_counter_label.grid(column=1, row=1)
        self.precision_label.grid(column=0, row=2)
        self.precision_counter_label.grid(column=1, row=2)
        self.f_score_label.grid(column=0, row=3)
        self.f_score_counter_label.grid(column=1, row=3)

        self.input_textbox = Text(self, font='Arial 11', wrap='word', width=50)
        self.original_textbox = Text(self, font='Arial 11', wrap='word', width=50)
        self.marked_textbox = Text(self, font='Arial 11', wrap='word', width=50)

        self.input_textbox_label = ttk.Label(self)
        self.original_textbox_label = ttk.Label(self)
        self.marked_textbox_label = ttk.Label(self)

        self.input_textbox_label.grid(column=0, row=0)
        self.original_textbox_label.grid(column=1, row=0)
        self.marked_textbox_label.grid(column=2, row=0)
        self.input_textbox.grid(column=0, row=1)
        self.original_textbox.grid(column=1, row=1)
        self.marked_textbox.grid(column=2, row=1)
        self.metrics_frame.grid(row=2, column=0)
        self.legend_frame.grid(row=2, column=2)

        self.marked_textbox.tag_config('red_text', foreground='red')
        self.marked_textbox.tag_config('green_text', foreground='green')
        self.marked_textbox.tag_config('blue_text', foreground='blue')

        self.original_textbox.tag_config('red_text', foreground='red')
        self.original_textbox.tag_config('green_text', foreground='green')
        self.original_textbox.tag_config('blue_text', foreground='blue')

        if language == 'ru':
            self.original_textbox_label['text'] = 'Размеченный текст'
            self.input_textbox_label['text'] = 'Оригинальный текст'
            self.marked_textbox_label['text'] = 'Текст после работы алгоритма'
            self.false_label['text'] = 'Красный - неверно размеченные части песни'
            self.TP_label['text'] = 'Зеленый - верно размеченный припев'
            self.TN_label['text'] = 'Синий - верно размеченный куплет'
        else:
            self.original_textbox_label['text'] = 'Marked text'
            self.input_textbox_label['text'] = 'Original text'
            self.marked_textbox_label['text'] = 'Text after the algorithm'
            self.false_label['text'] = 'Red – incorrectly marked parts of the song'
            self.TP_label['text'] = 'Green – correctly marked chorus'
            self.TN_label['text'] = 'Blue – correctly marked verse'

        self.fill_input(song.letters)
        self.fill_marked(song.letters)
        self.fill_orig(song.letters)
        self.fill_metrics(song.confusion_matrix)

    def fill_metrics(self, confusion_matrix):
        self.accuracy_counter_label['text'] = str(accuracy(confusion_matrix))
        self.precision_counter_label['text'] = str(precision(confusion_matrix))
        self.recall_counter_label['text'] = str(recall(confusion_matrix))
        self.f_score_counter_label['text'] = str(F_score(confusion_matrix))

    def fill_input(self, letters):
        for i in letters:
            self.input_textbox.insert(END, i.letter)
        self.input_textbox.config(state='disabled')

    def fill_orig(self, letters):
        for i in range(len(letters)):
            if letters[i-1].real_section != letters[i].real_section:
                self.original_textbox.insert(END, '\n')
            if letters[i].real_section == 'c':
                self.original_textbox.insert(END, letters[i].letter, 'green_text')
            if letters[i].real_section == 'n':
                self.original_textbox.insert(END, letters[i].letter, 'blue_text')
        self.original_textbox.config(state='disabled')

    def fill_marked(self, letters):
        for i in letters:
            if i.mistake_class == 'TP' or i.mistake_class == 'TN':
                if i.predicted_section == 'c':
                    self.marked_textbox.insert(END, i.letter, 'green_text')
                if i.predicted_section == 'n':
                    self.marked_textbox.insert(END, i.letter, 'blue_text')
            if i.mistake_class == 'FP' or i.mistake_class == 'FN':
                self.marked_textbox.insert(END, i.letter, 'red_text')
        self.marked_textbox.config(state='disabled')
