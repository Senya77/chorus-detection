import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import copy

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
        self.resizable(False, False)
        self.title('Поиск припева песни')

        self.__language = 'ru'
        self.__params_mode = 'common'

        # Выпадающее меню
        self.menu = Menu()
        self.menu.add_cascade(command=lambda: self.change_language(self.__language))
        self.menu.add_cascade(command=self.load_file)
        self.menu.add_cascade(command=self.open_markup_tool)
        self.menu.add_cascade(command=self.open_compare_tool)
        self.menu.add_cascade(command=self.show_statistic)
        self.menu.add_cascade(command=lambda: self.change_params_window(self.__params_mode))
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
        self.window_spinbox.set(0.50)

        # Кнопки установить параметры и начать выполнение
        self.update_button = ttk.Button(self.params_frame, command=self.set_params)
        self.start_button = ttk.Button(self.params_frame, command=self.run)

        self.num_label.grid(row=3, column=0)
        self.num_spinbox.grid(row=3, column=1)

        self.size_label.grid(row=4, column=0)
        self.size_spinbox.grid(row=4, column=1)

        self.window_label.grid(row=5, column=0)
        self.window_spinbox.grid(row=5, column=1)

        # self.algos = ['Snippet finder']
        # self.algo_label = ttk.Label(self.params_frame)
        # self.algo_combobox = ttk.Combobox(self.params_frame, values=self.algos, state='readonly')
        # self.algo_combobox.grid(row=6, columnspan=2)

        self.start_button.grid(row=7, columnspan=2)

        self.listbox_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.settings_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.change_language('en')

        self.load_songs()
        self.mainloop()

    def __validate_num_size_spinbox(self, P):
        if P.strip() == "":
            return True
        try:
            value = float(P)
            if 1 <= value <= 1000 and value.is_integer():
                return True
            else:
                return False
        except ValueError:
            return False

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

    def parse_songs(self, filenames, directory):
        # TODO Добавить обработку исключений
        for filename in filenames:
            song = parse_xml(os.path.join(directory, filename))
            song.name = os.path.basename(filename).rstrip('.xml')
            self.all_songs_list.append(song)
            self.all_songs_var.set(self.all_songs_list)

    def load_songs(self):
        directory = 'songs_xmls\\'
        filenames = os.listdir(directory)
        self.parse_songs(filenames, directory)

    def load_file(self):
        files = filedialog.askopenfiles(filetypes=[('*.xml files', '.xml')])
        filenames = [file.name for file in files]
        directory = 'songs_xmls\\'
        self.parse_songs(filenames, directory)

    def set_params(self):
        if self.selected_songs_listbox.curselection():
            song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
            song.num_snippets = int(self.num_spinbox.get())
            song.snippets_size = int(self.size_spinbox.get())
            # TODO Убрать костыль
            if float(self.window_spinbox.get()) < 0.05:
                song.window_size = float(0.05)
            else:
                song.window_size = float(self.window_spinbox.get())

    def get_params(self, event):
        if self.selected_songs_listbox.curselection():
            song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
            self.num_counter_label['text'] = str(song.num_snippets)
            self.size_counter_label['text'] = str(song.snippets_size)
            self.window_size_counter_label['text'] = str(song.window_size)

    def add_selected(self):
        selected_songs = self.all_songs_listbox.curselection()
        self.selected_songs_list += ([copy.deepcopy(self.all_songs_list[i]) for i in selected_songs])
        self.selected_songs_var.set(self.selected_songs_list)

    def delete_selected(self):
        if self.selected_songs_listbox.curselection():
            self.selected_songs_list.pop(self.selected_songs_listbox.curselection()[0])
            self.selected_songs_var.set(self.selected_songs_list)

    def add_all(self):
        self.selected_songs_list = self.all_songs_list
        self.selected_songs_var.set(self.selected_songs_list)

    def delete_all(self):
        self.selected_songs_list = []
        self.selected_songs_var.set(self.selected_songs_list)

    def open_markup_tool(self):
        MarkupTool(self, self.__language)

    # TODO Переписать запуск алгоритмов
    def run_common(self):
        num_snippets = self.num_spinbox.get()
        snippets_size = self.size_spinbox.get()
        window_size = self.window_spinbox.get()
        if not (num_snippets and snippets_size and window_size):
            tkinter.messagebox.showerror('Ошибка', 'Заполнены не все поля')
        else:
            if not self.selected_songs_list:
                tkinter.messagebox.showerror('Ошибка', 'Не выбраны песни')
            else:
                for song in self.selected_songs_list:
                    letters = [i.ascii for i in song.letters]
                    song.snippets = find_snippet(letters, int(snippets_size), int(num_snippets), float(window_size))
                    mark_results(song.letters, song.snippets)
                    song.confusion_matrix = confusion_matrix(song.letters)

    def run_single(self):
        if not self.selected_songs_list:
            tkinter.messagebox.showerror('Ошибка', 'Не выбраны песни')
        else:
            for song in self.selected_songs_list:
                letters = [i.ascii for i in song.letters]
                song.snippets = find_snippet(letters, song.snippets_size, song.num_snippets, song.window_size)
                mark_results(song.letters, song.snippets)
                song.confusion_matrix = confusion_matrix(song.letters)

    def run(self):
        if self.__params_mode == 'common':
            self.run_common()
        if self.__params_mode == 'single':
            self.run_single()

    def open_compare_tool(self):
        if self.selected_songs_listbox.curselection():
            song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
            if song.snippets:
                CompareTool(self, song, self.__language)
            else:
                tkinter.messagebox.showerror('Ошибка', 'Нет данных о сниппетах')

    def show_statistic(self):
        params = {'snippet_size' : self.size_spinbox.get(),
                  'num_spippets': self.num_spinbox.get(),
                  'window_size' : self.window_spinbox.get()}
        make_boxplot(self.selected_songs_list, params)

    # TODO Придумать название получше
    def change_params_window(self, params_mode):
        if params_mode == 'common':
            self.__params_mode = 'single'
            self.num_show_label.grid(row=0, column=0)
            self.num_counter_label.grid(row=0, column=1)
            self.size_show_label.grid(row=1, column=0)
            self.size_counter_label.grid(row=1, column=1)
            self.window_size_show_label.grid(row=2, column=0)
            self.window_size_counter_label.grid(row=2, column=1)
            self.update_button.grid(row=6, columnspan=2)
        if params_mode == 'single':
            self.__params_mode = 'common'
            self.num_show_label.grid_forget()
            self.num_counter_label.grid_forget()
            self.size_show_label.grid_forget()
            self.size_counter_label.grid_forget()
            self.window_size_show_label.grid_forget()
            self.window_size_counter_label.grid_forget()
            self.update_button.grid_forget()

    def change_language(self, lang):
        if lang == 'en':
            self.__language = 'ru'
            self.menu.entryconfigure(1, label='Ru')
            self.menu.entryconfigure(2, label='Загрузить')
            self.menu.entryconfigure(3, label='Разметить')
            self.menu.entryconfigure(4, label='Сравнить')
            self.menu.entryconfigure(5, label='Статистика')
            self.menu.entryconfigure(6, label='Режим параметров')
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
            self.menu.entryconfigure(6, label='Parameters mode')
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
