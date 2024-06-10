import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
import os
import copy
import threading

from metrics import *
from markup_tool import MarkupTool
from parsing_tool import *
from song import Song
from compare_tool import *
from snippet_finder import *


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('720x480')
        self.title('Поиск припева песни')

        self.__language = 'ru'

        # Выпадающее меню
        self.menu = Menu()
        self.menu.add_cascade(command=lambda: self.change_language(self.__language))
        self.menu.add_cascade(command=self.load_file)
        self.menu.add_cascade(command=self.open_markup_tool)
        self.menu.add_cascade(command=self.open_compare_tool)
        self.menu.add_cascade(command=self.show_statistic)
        self.config(menu=self.menu)

        # Рамка для списков
        self.listbox_frame = ttk.Frame(self)

        # Список с загруженными песнями
        self.all_songs_list = []
        self.all_songs_var = Variable(value=self.all_songs_list)
        self.all_songs_frame = ttk.Frame(self.listbox_frame)
        self.all_songs_listbox = Listbox(self.all_songs_frame, selectmode=EXTENDED, listvariable=self.all_songs_var)

        self.all_songs_scrollbar = ttk.Scrollbar(self.all_songs_frame, orient='vertical',
                                                 command=self.all_songs_listbox.yview)
        self.all_songs_listbox['yscrollcommand'] = self.all_songs_scrollbar.set
        self.all_songs_listbox.pack(expand=True, fill=BOTH, side=LEFT)
        self.all_songs_scrollbar.pack(side=RIGHT, fill=Y)

        # Кнопки перемещения песен
        self.movement_frame = ttk.Frame(self.listbox_frame)
        self.add_button = ttk.Button(self.movement_frame, text='↓', command=self.add_selected)
        self.delete_button = ttk.Button(self.movement_frame, text='↑', command=self.delete_selected)
        self.add_all_button = ttk.Button(self.movement_frame, text='', command=self.add_all)
        self.delete_all_button = ttk.Button(self.movement_frame, text='', command=self.delete_all)
        self.add_button.pack(side=LEFT)
        self.delete_button.pack(side=LEFT)
        self.add_all_button.pack(side=LEFT)
        self.delete_all_button.pack(side=LEFT)

        # Список с выбранными песнями
        self.selected_songs_list = []
        self.selected_songs_var = Variable(value=self.selected_songs_list)
        self.selected_songs_frame = ttk.Frame(self.listbox_frame)
        self.selected_songs_listbox = Listbox(self.selected_songs_frame,
                                              selectmode=SINGLE, listvariable=self.selected_songs_var)
        self.selected_songs_scrollbar = ttk.Scrollbar(self.selected_songs_frame, orient='vertical',
                                                      command=self.selected_songs_listbox.yview)
        self.selected_songs_listbox['yscrollcommand'] = self.selected_songs_scrollbar.set
        self.selected_songs_listbox.bind('<<ListboxSelect>>', self.get_params)
        self.selected_songs_listbox.pack(expand=True, fill=BOTH, side=LEFT)
        self.selected_songs_scrollbar.pack(side=RIGHT, fill=Y)

        # Расположение списков песен и кнопок для них
        self.all_songs_frame.pack(expand=True, fill=BOTH)
        self.movement_frame.pack()
        self.selected_songs_frame.pack(expand=True, fill=BOTH)

        # Рамка настроек (нужна, чтобы поместить туда рамку с параметрами)
        self.settings_frame = ttk.Frame(self)

        # Рамка с настройками параметров алгоритма
        self.params_frame = ttk.Frame(self.settings_frame)
        self.params_frame.pack(expand=True)

        # Количество сниппетов в песне (для просмотра информации)
        self.num_show_label = ttk.Label(self.params_frame)
        self.num_counter_label = ttk.Label(self.params_frame, text='0')

        # Размер сниппетов (для просмотра информации)
        self.size_show_label = ttk.Label(self.params_frame)
        self.size_counter_label = ttk.Label(self.params_frame, text='0')

        # Размер окна в алгоритме (для просмотра информации)
        self.window_size_show_label = ttk.Label(self.params_frame)
        self.window_size_counter_label = ttk.Label(self.params_frame, text='0')

        # Количество сниппетов в песне (для задания параметра)
        self.num_label = ttk.Label(self.params_frame)
        self.validate_num_size_command = self.register(self.__validate_num_size_spinbox)
        self.num_spinbox = ttk.Spinbox(self.params_frame, from_=1, to=1000,
                                       validate="key", validatecommand=(self.validate_num_size_command, '%P'))

        # Размер сниппетов в песне (для задания параметра)
        self.size_label = ttk.Label(self.params_frame)
        self.size_spinbox = ttk.Spinbox(self.params_frame, from_=1, to=1000,
                                        validate="key", validatecommand=(self.validate_num_size_command, '%P'))

        # Размер окна в алгоритме (для задания параметра)
        self.window_label = ttk.Label(self.params_frame)
        self.validate_window_command = self.register(self.__validate_window_spinbox)

        self.window_spinbox = ttk.Spinbox(self.params_frame, from_=0.05, to=0.95, increment=0.01,
                                          wrap=True, validate="key",
                                          validatecommand=(self.validate_window_command, '%P'))
        self.num_spinbox.set(3)
        self.size_spinbox.set(150)
        self.window_spinbox.set(0.50)


        # Кнопки установить параметры и начать выполнение
        self.update_button = ttk.Button(self.params_frame, command=self.set_params)
        self.start_button = ttk.Button(self.params_frame, command=self.run)

        self.num_show_label.grid(row=0, column=0)
        self.num_counter_label.grid(row=0, column=1)
        self.size_show_label.grid(row=1, column=0)
        self.size_counter_label.grid(row=1, column=1)
        self.window_size_show_label.grid(row=2, column=0)
        self.window_size_counter_label.grid(row=2, column=1)
        self.update_button.grid(row=6, columnspan=2)

        self.num_label.grid(row=3, column=0)
        self.num_spinbox.grid(row=3, column=1)

        self.size_label.grid(row=4, column=0)
        self.size_spinbox.grid(row=4, column=1)

        self.window_label.grid(row=5, column=0)
        self.window_spinbox.grid(row=5, column=1)

        self.start_button.grid(row=7, columnspan=2)

        self.listbox_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.settings_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.menu.entryconfigure(5, state='disabled')
        self.change_language('en')
        self.load_songs()
        self.mainloop()

    # Функция для валидации введённых значений в поля "Количество сниппетов", "Размер сниппетов"
    def __validate_num_size_spinbox(self, P):
        if P.strip() == "":
            return True
        try:
            value = int(P)
            if 0 < value <= 1000:
                return True
            else:
                return False
        except ValueError:
            return False

    # Функция для валидации введённого значения в поле "Размер окна"
    def __validate_window_spinbox(self, P):
        if P.strip() == "":
            return True
        try:
            value = float(P)
            if 0 <= value <= 0.95:
                return True
            else:
                return False
        except ValueError:
            return False

    # Функция для парсинга песен из файлов
    def parse_songs(self, filenames, dirs):
        for filename, dir in zip(filenames, dirs):
            extension = os.path.splitext(filename)[1]
            if extension == '.xml':
                song = parse_xml(os.path.join(dir, filename))
            elif extension == '.txt':
                song = parse_txt(os.path.join(dir, filename))
            else:
                return
            song.name = os.path.basename(filename).rstrip(extension)
            self.all_songs_list.append(song)
            self.all_songs_var.set(self.all_songs_list)

    # Функция для загрузки песен из папки songs_xmls (если есть)
    def load_songs(self):
        if not os.path.exists('songs_xmls'):
            return
        filenames = os.listdir('songs_xmls')
        dirs = [os.path.join(os.getcwd(), 'songs_xmls') for i in filenames]
        self.parse_songs(filenames, dirs)

    # Функция для выбора файлов, которые необходимо загрузить
    def load_file(self):
        existed_songs = [song.name for song in self.all_songs_list]
        files = filedialog.askopenfiles(filetypes=[('*.xml files', '.xml'), ('*.txt files', '.txt')])
        files = [file.name for file in files]
        filenames = [os.path.basename(file) for file in files]
        filenames = [filename for filename in filenames if os.path.splitext(filename)[0] not in existed_songs]
        dirs = [os.path.dirname(file) for file in files]
        self.parse_songs(filenames, dirs)

    # Функция для обновления параметров песен
    def set_params(self):
        if self.selected_songs_listbox.curselection():
            song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
            song.num_snippets = int(self.num_spinbox.get()) if self.num_spinbox.get() else 3
            song.snippets_size = int(self.size_spinbox.get()) if self.size_spinbox.get() else 150
            song.window_size = float(self.window_spinbox.get()) if self.window_spinbox.get() else 0.5

    # Функция для парсинга параметров из полей "Количество сниппетов", "Размер сниппетов", "Размер окна"
    def get_params(self, event):
        if self.selected_songs_listbox.curselection():
            song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
            self.num_counter_label['text'] = str(song.num_snippets)
            self.size_counter_label['text'] = str(song.snippets_size)
            self.window_size_counter_label['text'] = str(song.window_size)

    # Функция, добавляющая выбранные песни в тестовый набор
    def add_selected(self):
        selected_songs = self.all_songs_listbox.curselection()
        self.selected_songs_list += ([copy.deepcopy(self.all_songs_list[i]) for i in selected_songs])
        self.selected_songs_var.set(self.selected_songs_list)

    # Функция, удаляющая выбранную песню из тестового набора
    def delete_selected(self):
        if self.selected_songs_listbox.curselection():
            self.selected_songs_list.pop(self.selected_songs_listbox.curselection()[0])
            self.selected_songs_var.set(self.selected_songs_list)

    # Функция, добавляющая все песни в тестовый набор
    def add_all(self):
        self.selected_songs_list = self.all_songs_list
        self.selected_songs_var.set(self.selected_songs_list)

    # Функция, удаляющая все песни из тестового набора
    def delete_all(self):
        self.selected_songs_list = []
        self.selected_songs_var.set(self.selected_songs_list)

    # Функция, открывающая утилиту разметки
    def open_markup_tool(self):
        MarkupTool(self, self.__language)

    # Функция для проверки параметров запуска алгоритма
    def check_params(self, song):
        if song.snippets_size < 4:
            msg = 'Размер сниппета должен быть >= 4' if self.__language == 'ru' else 'Snippet size must be >= 4'
            tkinter.messagebox.showerror('Ошибка', f'{song.name}:\n {msg}' )
            return False
        if len(song.letters) < (2 * song.snippets_size):
            msg = 'Размер песни слишком мал отностительно размера сниппета' if self.__language == 'ru' else 'Time series is too short relative to snippet length'
            tkinter.messagebox.showerror('Ошибка', f'{song.name}:\n {msg}')
            return False
        if song.window_size >= song.snippets_size:
            msg = 'Размер окна должен должен быть меньше размера сниппета' if self.__language == 'ru' else 'Window size must be smaller than snippet size'
            tkinter.messagebox.showerror('Ошибка', f'{song.name}:\n {msg}')
            return False
        if song.window_size < 0.05:
            msg = 'Размер окна должен быть >= 0.05' if self.__language == 'ru' else 'Window size must be >= 0.05'
            tkinter.messagebox.showerror('Ошибка', f'{song.name}:\n {msg}')
            return False
        return True

    # Функция, передающая параметры песен в алгоритм поиска сниппетов
    def run_snippet_finder(self):
        for song in self.selected_songs_list:
            size = song.snippets_size
            num = song.num_snippets
            window = song.window_size
            letters = song.letters
            song.snippets = find_snippet(letters, int(size), int(num), int(window))
            mark_results(letters, song.snippets[0]['neighbors'])
            if song.marked:
                song.confusion_matrix = confusion_matrix(song.letters)
        self.start_button.config(state='normal')
        self.menu.entryconfigure(5, state='normal')

    # Функция, запускающая алгоритм в отдельном потоке
    def run(self):
        if not self.selected_songs_list:
            tkinter.messagebox.showerror('Ошибка', 'Не выбраны песни')
            return

        for song in self.selected_songs_list:
            if not self.check_params(song):
                return

        self.start_button.config(state='disabled')
        self.menu.entryconfigure(5, state='disabled')
        threading.Thread(target=self.run_snippet_finder, daemon=True).start()

    # Функция открывающая утилиту сравнения
    def open_compare_tool(self):
        if self.selected_songs_listbox.curselection():
            song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
            if song.snippets:
                CompareTool(self, song, self.__language)
            else:
                tkinter.messagebox.showerror('Ошибка', 'Нет данных о сниппетах')

    # Функция для вызова построения диаграммы размаха
    def show_statistic(self):
        if not self.selected_songs_list:
            tkinter.messagebox.showerror('Ошибка', 'Не выбраны песни')
            return
        else:
            songs = []
            for song in self.selected_songs_list:
                if song.marked:
                    songs.append(song)
            if not songs:
                tkinter.messagebox.showerror('Ошибка', 'Нет подходящих песен')
                return
            dataframe = make_dataframe(songs)
            make_boxplot(dataframe)

    # Функция для смены языка в приложении
    def change_language(self, lang):
        if lang == 'en':
            self.__language = 'ru'
            self.menu.entryconfigure(1, label='Ru')
            self.menu.entryconfigure(2, label='Загрузить')
            self.menu.entryconfigure(3, label='Разметить')
            self.menu.entryconfigure(4, label='Сравнить')
            self.menu.entryconfigure(5, label='Статистика')
            self.add_all_button['text'] = 'Добавить все'
            self.delete_all_button['text'] = 'Удалить все'
            self.num_show_label['text'] = 'Количество сниппетов'
            self.size_show_label['text'] = 'Размер сниппетов'
            self.window_size_show_label['text'] = 'Размер окна'
            self.num_label['text'] = 'Количество \nсниппетов'
            self.size_label['text'] = 'Размер \nсниппетов'
            self.update_button['text'] = 'Установить параметры'
            self.window_label['text'] = 'Размер окна'
            self.start_button['text'] = 'Начать выполнение'
        if lang == 'ru':
            self.__language = 'en'
            self.menu.entryconfigure(1, label='En')
            self.menu.entryconfigure(2, label='Load')
            self.menu.entryconfigure(3, label='Mark up')
            self.menu.entryconfigure(4, label='Compare')
            self.menu.entryconfigure(5, label='Statistic')
            self.add_all_button['text'] = 'Select all'
            self.delete_all_button['text'] = 'Delete all'
            self.num_show_label['text'] = 'Snippets amount'
            self.size_show_label['text'] = 'Snippets size'
            self.window_size_show_label['text'] = 'Window size'
            self.num_label['text'] = 'Snippets \namount'
            self.size_label['text'] = 'Snippets \nsize'
            self.update_button['text'] = 'Set parameters'
            self.window_label['text'] = 'Window size'
            self.start_button['text'] = 'Run algorithm'


def main():
    MainWindow()


if __name__ == '__main__':
    main()
