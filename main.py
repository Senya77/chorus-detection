import matplotlib.pyplot as plt
import matrixprofile as mp
from matrixprofile.visualize import plot_snippets
import xml.etree.ElementTree as ET
from metrics import *


def text_to_array(path):
    tree = ET.parse(path)
    text = tree.getroot()[1]
    marked_char_array = []
    for elem in text:
        if elem.tag == 'chorus':
            for c in elem.text:
                marked_char_array += [[c, 'c']]
        else:
            for c in elem.text:
                marked_char_array += [[c, 'n']]
    return marked_char_array


def char_to_ascii(char_array):
    marked_ascii_array = []
    simple_ascii_array = []
    for c in char_array:
        marked_ascii_array.append([str(ord(c[0])), c[1]])
        simple_ascii_array.append(str(ord(c[0])))
    return marked_ascii_array, simple_ascii_array


def plot_series(array):
    time = [i for i in range(1, len(array) + 1)]
    plt.plot(time, array)
    plt.show()


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


def main():
    chars = text_to_array('songs_txts/Parallel_Universe.xml')
    marked_ascii_array, simple_ascii_array = char_to_ascii(chars)

    snippets = find_snippet(simple_ascii_array)
    plot_snippet(snippets, simple_ascii_array)

    result_array = mark_results(simple_ascii_array, snippets)
    result_array, mistakes = confusion_matrix(result_array, marked_ascii_array)

    print('Accuracy:', accuracy(mistakes))
    print('Precision:', precision(mistakes))
    print('Recall:', recall(mistakes))
    print('F-score:', F_score(precision(mistakes), recall(mistakes), 1))


if __name__ == '__main__':
    main()
