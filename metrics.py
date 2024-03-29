import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    try:
        return round((mistakes['TP'] + mistakes['TN']) / (mistakes['TP'] + mistakes['TN'] + mistakes['FP'] + mistakes['FN']), 4)
    except ZeroDivisionError:
        return 0

def recall(mistakes):
    try:
        return round(mistakes['TP'] / (mistakes['TP'] + mistakes['TN']), 4)
    except ZeroDivisionError:
        return 0

def precision(mistakes):
    try:
        return round(mistakes['TP'] / (mistakes['TP'] + mistakes['FP']), 4)
    except ZeroDivisionError:
        return 0

def F_score(mistakes, B=1):
    p = precision(mistakes)
    r = recall(mistakes)
    try:
        return round(((1+B**2) * p * r) / ((B**2 * p) + r), 4)
    except ZeroDivisionError:
        return 0

def make_boxplot(songs, params: dict):
    columns = ['accuracy', 'recall', 'precision', 'F_score']
    df = pd.DataFrame(columns=columns)
    for song in songs:
        a = accuracy(song.confusion_matrix)
        r = recall(song.confusion_matrix)
        p = precision(song.confusion_matrix)
        f = F_score(song.confusion_matrix)
        df = pd.concat([df, pd.DataFrame([[a, r, p, f]], columns=columns)], ignore_index=True)
    boxplot = sns.boxplot(data=df)


    plt.show()