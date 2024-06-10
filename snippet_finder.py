from matrixprofile.discover import snippets

# Функция нахождения сниппетов
def find_snippet(letters, snippet_size, num_snippets, window):
    letters_ascii = [l.ascii for l in letters]
    _snippets = snippets(letters_ascii, snippet_size, num_snippets, window_size=window)
    return _snippets
