__author__ = 'bengt'

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help='Path to the corpus file.')

    args = parser.parse_args()

    corpus = [line.replace('\n', '') for line in open(args.corpus).readlines()]

    print('Accuracy: ')
    accuracies, total_match_count, total_pos_count = calculate_accuracy(corpus)
    for (pos, accuracy) in accuracies.items():
        print('{0:>12.2%}'.format(accuracy), pos)

    print('Total Accuracy: {0:>12.2%}'.format(total_match_count/total_pos_count))

    print()
    print('Confusion Matrix:')
    matrix, pos = calculate_confusion_matrix(corpus)
    draw_confusion_matrix(matrix, pos)


def calculate_accuracy(corpus):
    occurances = {}
    for line in corpus:
        if len(line.split('\t')) != 6:
            continue

        ID, FORM, LEMMA, PLEMMA, POS, PPOS = line.split('\t')

        if POS == PPOS:
            if POS in occurances:
                matches, total = occurances[POS]
                occurances[POS] = (matches + 1, total + 1)
            else:
                occurances[POS] = (1, 1)
        else:
            if POS in occurances:
                matches, total = occurances[POS]
                occurances[POS] = (matches, total + 1)
            else:
                occurances[POS] = (0, 1)
    total_pos_count = 0
    total_match_count = 0
    accuracies = {}
    for (key, value) in occurances.items():
        matches, total = value
        accuracies[key] = matches / float(total)
        total_match_count += matches
        total_pos_count += total
    return accuracies, total_match_count, total_pos_count


def calculate_confusion_matrix(corpus):
    pos = []

    # Create a list of parts of speaches..
    for line in corpus:
        if len(line.split('\t')) != 6:
            continue

        ID, FORM, LEMMA, PLEMMA, POS, PPOS = line.split('\t')

        if not POS in pos:
            pos.append(POS)

    # Confusion matrix
    matrix = {key: {p: 0 for p in pos} for key in pos}

    for line in corpus:
        if len(line.split('\t')) != 6:
            continue
        ID, FORM, LEMMA, PLEMMA, POS, PPOS = line.split('\t')
        matrix[POS][PPOS] += 1

    return matrix, pos


def draw_confusion_matrix(matrix, pos):
    print('    ', end='')
    #for p in pos:
    for (k,v) in matrix.items():
        print('{0:>4}'.format(k), end='')

    print()

    for (correct_pos, row) in matrix.items():
        print('{0:>4}'.format(correct_pos), end='')
        for (predicted_pos, value) in row.items():
            print('{0:>4}'.format(value), end='')
        print()

if __name__ == '__main__':
    main()
