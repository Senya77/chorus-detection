import tkinter.scrolledtext
from tkinter import *
from tkinter import ttk
from metrics import accuracy, precision, recall, F_score, covering
from matrixprofile.visualize import plot_snippets
import matplotlib.pyplot as plt
import seaborn as sns

class CompareTool(Toplevel):
    def __init__(self, parent, song, language):
        super().__init__(parent)
        self.resizable(False, False)

        self.menu = Menu()
        self.menu.add_cascade(command=lambda: self.plot_snippets(song, language))
        self.config(menu=self.menu)

        self.metrics_frame = Frame(self)

        self.accuracy_label = ttk.Label(self.metrics_frame, text='Accuracy:', font='Arial 11')
        self.accuracy_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')
        self.recall_label = ttk.Label(self.metrics_frame, text='Recall:', font='Arial 11')
        self.recall_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')
        self.precision_label = ttk.Label(self.metrics_frame, text='Precision:', font='Arial 11')
        self.precision_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')
        self.f_score_label = ttk.Label(self.metrics_frame, text='F-score', font='Arial 11')
        self.f_score_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')
        self.covering_label = ttk.Label(self.metrics_frame, text='Covering', font='Arial 11')
        self.covering_counter_label = ttk.Label(self.metrics_frame, text='0', font='Arial 11')

        self.legend_frame = Frame(self)
        self.TP_label = ttk.Label(self.legend_frame, font='Arial 11', foreground='green')
        self.TN_label = ttk.Label(self.legend_frame, font='Arial 11', foreground='blue')
        self.false_label = ttk.Label(self.legend_frame, font='Arial 11', foreground='red')
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
        self.covering_label.grid(column=0, row=4)
        self.covering_counter_label.grid(column=1, row=4)

        self.input_textbox = tkinter.scrolledtext.ScrolledText(self, font='Arial 11', wrap='word', width=50)
        self.original_textbox = tkinter.scrolledtext.ScrolledText(self, font='Arial 11', wrap='word', width=50)
        self.marked_textbox = tkinter.scrolledtext.ScrolledText(self, font='Arial 11', wrap='word', width=50)

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
            self.menu.entryconfigure(1, label='Представить в виде временного ряда')
            self.original_textbox_label['text'] = 'Размеченный текст'
            self.input_textbox_label['text'] = 'Оригинальный текст'
            self.marked_textbox_label['text'] = 'Текст после работы алгоритма'
            self.false_label['text'] = 'Красный — неверно размеченные части песни'
            self.TP_label['text'] = 'Зеленый — верно размеченный припев'
            self.TN_label['text'] = 'Синий — верно размеченный куплет'
        else:
            self.menu.entryconfigure(1, label='Show as time series')
            self.original_textbox_label['text'] = 'Marked text'
            self.input_textbox_label['text'] = 'Original text'
            self.marked_textbox_label['text'] = 'Text after the algorithm'
            self.false_label['text'] = 'Red — incorrectly marked parts of the song'
            self.TP_label['text'] = 'Green — correctly marked chorus'
            self.TN_label['text'] = 'Blue — correctly marked verse'

        if song.marked:
            self.fill_input(song.letters)
            self.fill_orig(song.letters)
            self.fill_marked(song.letters)
            self.fill_metrics(song)
        else:
            self.fill_input(song.letters)
            self.fill_unmarked(song.letters)
            self.menu.entryconfigure(1, state='disabled')

    # Функция, отображающая информацию о метриках
    def fill_metrics(self, song):
        self.accuracy_counter_label['text'] = str(accuracy(song.confusion_matrix))
        self.precision_counter_label['text'] = str(precision(song.confusion_matrix))
        self.recall_counter_label['text'] = str(recall(song.confusion_matrix))
        self.f_score_counter_label['text'] = str(F_score(song.confusion_matrix))
        self.covering_counter_label['text'] = str(covering(song))

    # Функция, отображающая текст без разметки
    def fill_input(self, letters):
        for i in letters:
            self.input_textbox.insert(END, i.letter)
        self.input_textbox.config(state='disabled')

    # Функция, отображающая текст с оригинальной разметкой
    def fill_orig(self, letters):
        for i in range(len(letters)):
            if letters[i - 1].real_section != letters[i].real_section:
                self.original_textbox.insert(END, '\n')
            if letters[i].real_section == 'c':
                self.original_textbox.insert(END, letters[i].letter, 'green_text')
            if letters[i].real_section == 'n':
                self.original_textbox.insert(END, letters[i].letter, 'blue_text')
        self.original_textbox.config(state='disabled')

    # Функция, отображающая текст с предсказанной разметкой (в случае, если был загружен xml файл)
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

    # Функция, отображающая текст с предсказанной разметкой (в случае, если был загружен txt файл)
    def fill_unmarked(self, letters):
        for i in letters:
            if i.predicted_section == 'c':
                self.marked_textbox.insert(END, i.letter, 'green_text')
            if i.predicted_section == 'n':
                self.marked_textbox.insert(END, i.letter, 'blue_text')
        self.original_textbox.insert(END, 'No data')

    # Функция разделяющая текст на сегменты, в зависимости от разметки
    def make_segments(self, segment):
        segments = []
        i_prev = 0
        indexes = []
        letters = []
        for i,j in segment:
            if i == i_prev+1:
                letters.append(j)
                indexes.append(i)
                i_prev = i
            else:
                segments.append((indexes, letters))
                i_prev = i
                letters = [j]
                indexes = [i]
        segments.append((indexes, letters))
        return segments

    # Функция отображающая текст песни в виде временного ряда (в двух разных разметках)
    def plot_snippets(self, song, language):
        true_title = 'Истинная разметка текста' if language == 'ru' else 'Ground truth markup'
        predicted_title = 'Предсказанная разметка текста' if language == 'ru' else 'Predicted markup'

        chorus_r = self.make_segments([(i[0], i[1].ascii) for i in enumerate(song.letters) if i[1].real_section == 'c'])
        verse_r = self.make_segments([(i[0], i[1].ascii) for i in enumerate(song.letters) if i[1].real_section == 'n'])
        chorus_p = self.make_segments([(i[0], i[1].ascii) for i in enumerate(song.letters) if i[1].mistake_class == 'TP'])
        verse_p = self.make_segments([(i[0], i[1].ascii) for i in enumerate(song.letters) if i[1].mistake_class == 'TN'])
        false = self.make_segments([(i[0], i[1].ascii) for i in enumerate(song.letters) if i[1].mistake_class == 'FP' or i[1].mistake_class == 'FN'])

        plt.subplot(211)
        plt.title(true_title)
        for i,j in chorus_r:
            plt.plot(i, j, color='green')
        for i,j in verse_r:
            plt.plot(i, j, color='blue')

        plt.subplot(212)
        plt.title(predicted_title)
        for i, j in chorus_p:
            plt.plot(i, j, color='green')
        for i, j in verse_p:
            plt.plot(i, j, color='blue')
        for i, j in false:
            plt.plot(i, j, color='red')
        plt.show()