class Letter:
    def __init__(self, letter):
        self.letter = letter
        self.ascii = ord(letter)
        self.real_section = None
        self.predicted_section = 'n'
        self.mistake_class = None
