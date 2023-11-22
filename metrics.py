def mark_results(letters, snippets):
    for i in snippets[0]['neighbors']:
        letters[i].predicted_section = 'c'


def confusion_matrix(letters):
    TP, TN, FP, FN = 0, 0, 0, 0
    for i in range(len(letters)):
        if letters[i].real_section == 'c' and letters[i].predicted_section == 'c':
            letters[i].mistake_class = 'TP'
            TP += 1
        elif letters[i].real_section == 'n' and letters[i].predicted_section == 'c':
            letters[i].mistake_class = 'FP'
            FP += 1
        elif letters[i].real_section == 'n' and letters[i].predicted_section == 'n':
            letters[i].mistake_class = 'TN'
            TN += 1
        elif letters[i].real_section == 'c' and letters[i].predicted_section == 'n':
            letters[i].mistake_class = 'FN'
            FN += 1
    return {'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN}


def accuracy(mistakes):
    return (mistakes['TP'] + mistakes['TN']) / (mistakes['TP'] + mistakes['TN'] + mistakes['FP'] + mistakes['FN'])


def recall(mistakes):
    return mistakes['TP'] / (mistakes['TP'] + mistakes['TN'])


def precision(mistakes):
    return mistakes['TP'] / (mistakes['TP'] + mistakes['FP'])


def F_score(precision, recall, B):
    return ((1+B**2) * precision * recall) / ((B**2 * precision) + recall)
