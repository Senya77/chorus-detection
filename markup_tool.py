from tkinter import *
from tkinter import filedialog
from tkinter import ttk


class MarkupTool(Toplevel):
    def __init__(self, parent, language):
        super().__init__(parent)

        self.title('Markup tool for XML')

        self.text_frame = Frame(self)
        self.options_frame = Frame(self)

        self.text_frame.pack(side='left', fill='both', expand=1)
        self.options_frame.pack(side='right', fill='both', expand=1)

        self.textbox = Text(self, font='Arial 12', wrap='word')
        self.scrollbar = Scrollbar(self)

        self.scrollbar['command'] = self.textbox.yview
        self.textbox['yscrollcommand'] = self.scrollbar.set

        self.textbox.pack(side='left', fill='both', expand=1)
        self.scrollbar.pack(side='right', fill='y')

        self.menu = Menu()
        self.menu.add_cascade(command=self.load_file)
        self.menu.add_cascade(command=self.save_file)
        self.config(menu=self.menu)

        self.sections = ['verse', 'chorus']
        self.sections_listbox = ttk.Combobox(self.options_frame, values=self.sections, state='readonly')

        self.metadata = ['chorus_length', 'chorus_number', 'verse_number', 'sections_number']
        self.metadata_listbox = ttk.Combobox(self.options_frame, values=self.metadata, state='readonly')

        self.spinbox = ttk.Spinbox(self.options_frame, from_=1, to=15, increment=1)

        self.mark_button = ttk.Button(self.options_frame, command=self.add_tags)

        self.meta_button = ttk.Button(self.options_frame, command=self.add_metadata)

        self.section_label = ttk.Label(self.options_frame)
        self.metadata_label = ttk.Label(self.options_frame)
        self.number_label = ttk.Label(self.options_frame)

        self.number_label.pack()
        self.spinbox.pack()
        self.section_label.pack()
        self.sections_listbox.pack()
        self.mark_button.pack()
        self.metadata_label.pack()
        self.metadata_listbox.pack()
        self.meta_button.pack()

        if language == 'ru':
            self.menu.entryconfigure(1, label='Загрузить')
            self.menu.entryconfigure(2, label='Сохранить')
            self.mark_button['text'] = 'Разметить'
            self.meta_button['text'] = 'Добавить данные'
            self.section_label['text'] = 'Выбор раздела'
            self.metadata_label['text'] = 'Выбор типа данных'
            self.number_label['text'] = 'Номер'
        else:
            self.menu.entryconfigure(1, label='Load')
            self.menu.entryconfigure(2, label='Save')
            self.mark_button['text'] = 'Mark up'
            self.meta_button['text'] = 'Add data'
            self.section_label['text'] = 'Choose section'
            self.metadata_label['text'] = 'Choose metadata'
            self.number_label['text'] = 'Number'

    # Функция для загрузки файла
    def load_file(self):
        fn = filedialog.askopenfilename(filetypes=[('*.txt files', '.txt'), ('*.xml files', '.xml')])
        if not fn:
            return
        self.textbox.delete('1.0', 'end')
        if fn.endswith('.txt'):
            self.textbox.insert('1.0', '<?xml version="1.0" encoding="UTF-8"?>\n')
            self.textbox.insert('2.0', '<song>\n')
            self.textbox.insert('end', '\n</song>')
        with open(fn, 'rt', encoding="UTF-8") as file:
            text = file.read()
            self.textbox.insert('3.0', text)
        return

    # Функция для сохранения файла
    def save_file(self):
        fn = filedialog.asksaveasfilename(filetypes=[('*.xml files', '.xml'), ('*.txt files', '.txt')],
                                          defaultextension='xml')
        if not fn:
            return
        with open(fn, 'w', encoding='UTF-8') as file:
            file.write(self.textbox.get('1.0', 'end'))
        return

    # Функция для добавления тега метаданных
    def add_metadata(self):
        if self.metadata_listbox.get() == 'chorus_length':
            length = len(self.textbox.selection_get())
            self.textbox.insert('3.0', f'<chorus_length>{length}</chorus_length>\n')
        else:
            number = self.spinbox.get()
            meta = self.metadata_listbox.get()
            self.textbox.insert('3.0', f'<{meta}>{number}</{meta}>\n')
        return

    # Функция для добавления тега частей песни
    def add_tags(self):
        s0 = self.textbox.index('sel.first')
        s1 = self.textbox.index('sel.last')
        section = self.sections_listbox.get()
        if self.spinbox.get() == '':
            self.textbox.insert(s1, f'\n</{section}>')
            self.textbox.insert(s0, f'<{section}>')
        else:
            number = self.spinbox.get()
            self.textbox.insert(s1, f'\n</{section}>')
            self.textbox.insert(s0, f'<{section} number="{number}">')
        return
