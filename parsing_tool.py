import xml.etree.ElementTree as ET
from letter import Letter
from song import Song

# Функция для парсинга песен из txt файлов
def parse_txt(path):
    song = Song()
    letters = []
    with open(path, 'r', encoding='UTF-8') as file:
        for c in file.read():
            lt = Letter(c)
            letters.append(lt)
    song.letters = letters
    return song

# Функция для парсинга песен из xml файлов
def parse_xml(path):
    song = Song()
    letters = []
    tree = ET.parse(path)
    text = tree.getroot()
    for elem in text:
        if elem.tag == 'chorus':
            for c in elem.text:
                letter = Letter(c)
                letter.real_section = 'c'
                letters.append(letter)
        elif elem.tag == 'verse':
            for c in elem.text:
                letter = Letter(c)
                letter.real_section = 'n'
                letters.append(letter)
        elif elem.tag == 'chorus_length':
            song.snippets_size = int(elem.text)
        elif elem.tag == 'verse_number':
            song.num_snippets = int(elem.text) + 1
        elif elem.tag == 'chorus_number':
            song.chorus_number = int(elem.text)
    song.letters = [i for i in letters if ord(i.letter) != 8242]
    song.marked = True
    return song
