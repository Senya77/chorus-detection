class Song:
    def __init__(self, name):
        self.name = name
        self.letters = None
        self.snippets = None
        self.num_snippets = 0
        self.snippets_size = 0
        self.confusion_matrix = 0

    def __str__(self):
        return self.name
