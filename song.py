class Song:
    def __init__(self, name=None):
        self.name = name
        self.letters = None
        self.snippets = None
        self.num_snippets = 0
        self.snippets_size = 0
        self.confusion_matrix = 0
        self.window_size = 0.5
        self.marked = False

    def __str__(self):
        return self.name
