import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.cbook import boxplot_stats

# Функция, присваивающая буквам предсказанный класс
def mark_results(letters, snippets):
    for l in letters:
        l.predicted_section = 'n'
    for i in snippets:
        letters[i].predicted_section = 'c'

# Функция вычисления матрицы ошибок
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

# Функция для деления текста на сегменты в зависимости от части песни
def make_segments(song, type):
    section = 'real_section' if type == True else 'predicted_section'
    segments = []
    segment = set()
    curr_seg = getattr(song.letters[0], section)
    for i, l in enumerate(song.letters):
        if getattr(l, section) == curr_seg:
            segment.add(l)
        else:
            curr_seg = getattr(l, section)
            segments.append(segment)
            segment = set([l])
    segments.append(segment)
    return segments

# Функция для подсчета меры covering
def covering(song):
    T = len(song.letters)
    segs_T = make_segments(song, True)
    segs_pred = make_segments(song, False)
    cov = 0
    for s_T in segs_T:
        s_len = len(s_T)
        jaccard = []
        for s_pred in segs_pred:
            union = len(s_pred.union(s_T))
            intersection = len(s_pred.intersection(s_T))
            jaccard.append(intersection/union)
        cov += s_len * max(jaccard)
    cov /= T
    return round(cov, 4)


def accuracy(mistakes):
    try:
        return round(
            (mistakes['TP'] + mistakes['TN']) / (mistakes['TP'] + mistakes['TN'] + mistakes['FP'] + mistakes['FN']), 4)
    except ZeroDivisionError:
        return 0


def recall(mistakes):
    try:
        return round(mistakes['TP'] / (mistakes['TP'] + mistakes['FN']), 4)
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
        return round((2 * p * r) / (p + r), 4)
    except ZeroDivisionError:
        return 0

# Функция для сбора информации о метриках
def make_dataframe(songs):
    columns = ['accuracy', 'recall', 'precision', 'F_score', 'covering']
    df_list = []
    for song in songs:
        a = accuracy(song.confusion_matrix)
        r = recall(song.confusion_matrix)
        p = precision(song.confusion_matrix)
        f = F_score(song.confusion_matrix)
        c = covering(song)
        df_list.append(pd.DataFrame([[a, r, p, f, c]], columns=columns))
    df = pd.concat(df_list, ignore_index=True)
    return df

# Функция создания диаграммы размаха
def make_boxplot(dataframe):
    dataframe_stats = [boxplot_stats(dataframe[col].dropna().values)[0] for col in dataframe.columns]
    stats = pd.DataFrame(dataframe_stats, index=dataframe.columns).iloc[:, [4, 5, 7, 8, 9]].round(2)
    with sns.axes_style("whitegrid"):
        boxplot = sns.boxplot(data=dataframe, color='0.8')
    for xtick in boxplot.get_xticks():
        for col in stats.columns:
            boxplot.text(xtick, stats.loc[:, col].iloc[xtick], stats.loc[:, col].iloc[xtick],
                         horizontalalignment='left', verticalalignment='top', size='small',
                         color='k', weight='semibold')
    plt.ylim(0,1)
    plt.show()

