import xml.etree.ElementTree as ET
from letter import Letter
from song import Song


def parse_txt(path):
    letters = []
    with open(path, 'r') as file:
        for c in file.read():
            lt = Letter(c)
            letters.append(lt)
    return letters


def parse_xml(path):
    song = Song()
    letters = []
    tree = ET.parse(path)
    text = tree.getroot()
    for elem in text:
        if elem.tag == 'chorus':
            for c in elem.text:
                lt = Letter(c)
                lt.real_section = 'c'
                letters.append(lt)
        elif elem.tag == 'verse':
            for c in elem.text:
                lt = Letter(c)
                lt.real_section = 'n'
                letters.append(lt)
        elif elem.tag == 'chorus_length':
            song.snippets_size = int(elem.text)
        elif elem.tag == 'sections_number':
            song.num_snippets = int(elem.text) - 1
    song.letters = letters
    return song
