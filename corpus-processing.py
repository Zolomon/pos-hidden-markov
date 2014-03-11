__author__ = 'bengt'

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help='Path to the corpus file.')
    parser.add_argument('--word', help='Show word frequencies.', action='store_true')
    parser.add_argument('--pos', help='Show part-of-speech frequencies.', action='store_true')
    args = parser.parse_args()

    corpus_file = open(args.corpus)
    corpus = [line.replace('\n', '') for line in corpus_file.readlines()]

    if args.word:
        [print('{0}'.format(str(frequency).rjust(12)), ' ', word) for word, frequency in word_frequencies(corpus)]

    if args.pos:
        [print('{0}'.format(str(frequency).rjust(12)), ' ', pos) for pos, frequency in pos_frequencies(corpus)]


def frequencies(corpus, index):
    """ Will calculate the frequency of tokens in column /index/.
    """
    frequencies = {}
    for line in corpus:
        if len(line.split('\t')) != 6:
            continue

        row = line.split('\t')
        key = row[index]

        if key in frequencies:
            frequencies[key] += 1
        else:
            frequencies[key] = 1

    import operator

    sorted_words = sorted(frequencies.items(), key=operator.itemgetter(1))
    return sorted_words


def word_frequencies(corpus):
    """ Will calculate the frequency for each word.
    """
    return frequencies(corpus, 1)


def pos_frequencies(corpus):
    """ Will calculate the frequency for each part-of-speech.
    """
    return frequencies(corpus, -2)


if __name__ == '__main__':
    main()
