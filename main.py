from Metrics import *
from CompareTool import *
from SnippetFinder import *
from Parser import *


def main():
    parser = Parser()
    parser.parse_xml('songs_txts/Parallel_Universe.xml')
    letters = parser.letters

    snippets = find_snippet([i.ascii for i in letters])
    plot_snippet(snippets, [i.ascii for i in letters])

    mark_results(letters, snippets)
    mistakes = confusion_matrix(letters)

    print('Accuracy:', accuracy(mistakes))
    print('Precision:', precision(mistakes))
    print('Recall:', recall(mistakes))
    print('F-score:', F_score(precision(mistakes), recall(mistakes), 1))

    cmptool = CompareTool(letters)


if __name__ == '__main__':
    main()
