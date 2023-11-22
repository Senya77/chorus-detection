# from metrics import *
# from compare_tool import *
# from snippet_finder import *
# from parsing_tool import *
from tkinter import *
from tkinter import ttk


class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('720x480')
        self.window.resizable(False, False)

        self.listbox_frame = ttk.Frame(self.window)

        self.all_songs_list = []
        self.all_songs_var = Variable(value=self.all_songs_list)
        self.all_songs_frame = ttk.Frame(self.listbox_frame)
        self.all_songs_listbox = Listbox(self.all_songs_frame, selectmode=EXTENDED, listvariable=self.all_songs_var)

        self.all_songs_scrollbar = ttk.Scrollbar(self.all_songs_frame, orient='vertical',
                                                 command=self.all_songs_listbox.yview)
        self.all_songs_listbox['yscrollcommand'] = self.all_songs_scrollbar.set
        self.all_songs_listbox.pack(expand=True, fill=BOTH, side=LEFT)
        self.all_songs_scrollbar.pack(side=RIGHT, fill=Y)

        self.movement_frame = ttk.Frame(self.listbox_frame)
        self.add_button = ttk.Button(self.movement_frame, text='↓', command=self.add_selected)
        self.delete_button = ttk.Button(self.movement_frame, text='↑', command=self.delete_selected)
        self.add_all_button = ttk.Button(self.movement_frame, text='Добавить все', command=self.add_all)
        self.delete_all_button = ttk.Button(self.movement_frame, text='Удалить все', command=self.delete_all)
        self.add_button.pack(side=LEFT)
        self.delete_button.pack(side=LEFT)
        self.add_all_button.pack(side=LEFT)
        self.delete_all_button.pack(side=LEFT)

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

        self.all_songs_frame.pack(expand=True, fill=BOTH)
        self.movement_frame.pack()
        self.selected_songs_frame.pack(expand=True, fill=BOTH)

        self.settings_frame = ttk.Frame(self.window)

        self.params_frame = ttk.Frame(self.settings_frame)
        self.num_label = ttk.Label(self.params_frame, text='Количество \nсниппетов')
        self.size_label = ttk.Label(self.params_frame, text='Размер \nсниппетов')

        self.num_spinbox = ttk.Spinbox(self.params_frame, from_=1, to=1000)
        self.size_spinbox = ttk.Spinbox(self.params_frame, from_=1, to=1000)
        self.params_frame.pack(expand=True)

        self.num_label.grid(row=2, column=0)
        self.size_label.grid(row=3, column=0)

        self.num_spinbox.grid(row=2, column=1)
        self.size_spinbox.grid(row=3, column=1)

        self.update_button = ttk.Button(self.params_frame, text='Установить параметры', command=self.set_params)
        self.update_button.grid(row=4, columnspan=2)

        self.algo_label = ttk.Label(self.params_frame, text='Выберите алгоритм')
        self.algo_combobox = ttk.Combobox(self.params_frame)
        self.start_button = ttk.Button(self.params_frame, text='Начать выполнение')
        self.algo_label.grid(row=5, columnspan=2)
        self.algo_combobox.grid(row=6, columnspan=2)
        self.start_button.grid(row=7, columnspan=2)

        self.listbox_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.settings_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.window.mainloop()

    def set_params(self):
        song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
        song.snippets_num = int(self.num_spinbox.get())
        song.snippets_len = int(self.size_spinbox.get())

    def get_params(self, event):
        song = self.selected_songs_list[self.selected_songs_listbox.curselection()[0]]
        self.num_spinbox.set(song.snippets_num)
        self.size_spinbox.set(song.snippets_len)

    def add_selected(self):
        selected_songs = self.all_songs_listbox.curselection()
        self.selected_songs_list += ([self.all_songs_list[i] for i in selected_songs])
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


def main():
    win = MainWindow()


if __name__ == '__main__':
    main()
