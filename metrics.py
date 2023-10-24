def mark_results(initial_array, snippets):
    result_array = []
    for i in initial_array:
        result_array += [[i, 'n']]
    for i in snippets[0]['neighbors']:
        result_array[i][1] = 'c'
    return result_array


def confusion_matrix(result_array, marked_array):
    TP, TN, FP, FN = 0, 0, 0, 0
    for i in range(len(marked_array)):
        if marked_array[i][1] == 'c' and result_array[i][1] == 'c':
            result_array[i].append('TP')
            TP += 1
        elif marked_array[i][1] == 'n' and result_array[i][1] == 'c':
            result_array[i].append('FP')
            FP += 1
        elif marked_array[i][1] == 'n' and result_array[i][1] == 'n':
            result_array[i].append('TN')
            TN += 1
        elif marked_array[i][1] == 'c' and result_array[i][1] == 'n':
            result_array[i].append('FN')
            FN += 1
    return result_array, {'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN}


def accuracy(mistakes):
    return (mistakes['TP'] + mistakes['TN']) / (mistakes['TP'] + mistakes['TN'] + mistakes['FP'] + mistakes['FN'])


def recall(mistakes):
    return mistakes['TP'] / (mistakes['TP'] + mistakes['TN'])


def precision(mistakes):
    return mistakes['TP'] / (mistakes['TP'] + mistakes['FP'])


def F_score(precision, recall, B):
    return ((1+B**2) * precision * recall) / ((B**2 * precision) + recall)
