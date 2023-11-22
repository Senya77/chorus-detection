import xml.etree.ElementTree as ET
from letter import Letter


class Parser:
    def __init__(self):
        self.letters = []

    def parse_txt(self, path):
        with open(path, 'r') as file:
            for c in file.read():
                lt = Letter(c)
                self.letters.append(lt)

    def parse_xml(self, path):
        tree = ET.parse(path)
        text = tree.getroot()[1]
        for elem in text:
            if elem.tag == 'chorus':
                for c in elem.text:
                    lt = Letter(c)
                    lt.real_section = 'c'
                    self.letters.append(lt)
            else:
                for c in elem.text:
                    lt = Letter(c)
                    lt.real_section = 'n'
                    self.letters.append(lt)
