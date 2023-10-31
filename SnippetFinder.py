import matplotlib.pyplot as plt
import matrixprofile as mp
from matrixprofile.visualize import plot_snippets


def find_snippet(array):
    snippet_size = 90
    num_snippets = 2
    snippets = mp.discover.snippets(array, snippet_size, num_snippets)
    return snippets


def plot_snippet(snippets, array):
    for i in range(len(snippets)):
        print('** Snippet-' + str(i + 1) + ' **')
        print('Index:', snippets[i]['index'])
        print('Fraction:', snippets[i]['fraction'])
        print()
    plot_snippets(snippets, array)
    plt.show()
