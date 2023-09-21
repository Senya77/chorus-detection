import matplotlib.pyplot as plt
import matrixprofile as mp
from matrixprofile.visualize import plot_snippets


def text_to_array(path):
    char_array = []
    with open(path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
    for line in lines:
        char_array += list(line)
    return char_array


def char_to_ascii(char_array):
    ascii_array = []
    for c in char_array:
        ascii_array.append(str(ord(c)))
    return ascii_array


def plot_series(array):
    time = [i for i in range(1, len(array)+1)]
    plt.plot(time, array)
    plt.show()


def find_snippet(array):
    snippet_size = 90
    num_snippets = 1
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
    chars = text_to_array('text.txt')
    ascii_chars = char_to_ascii(chars)
    snippets = find_snippet(ascii_chars)
    plot_snippet(snippets, ascii_chars)


if __name__ == '__main__':
    main()
