import matplotlib.pyplot as plt
from matrixprofile.visualize import plot_snippets
import matrixprofile as mp


def find_snippet(letters, snippet_size, num_snippets, w):
    snippets = mp.discover.snippets(letters, snippet_size, num_snippets, window_size=int(round(snippet_size*w)))
    return snippets


def plot_snippet(snippets, array):
    for i in range(len(snippets)):
        print('** Snippet-' + str(i + 1) + ' **')
        print('Index:', snippets[i]['index'])
        print('Fraction:', snippets[i]['fraction'])
        print()
    plot_snippets(snippets, array)
    plt.show()
