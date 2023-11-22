class Song:
    def __init__(self, name):
        self.name = name
        self.letters = None
        self.snippets = None
        self.snippets_num = None
        self.snippets_len = None
        self.l = None
        self.k = None

    def __str__(self):
        return self.name
