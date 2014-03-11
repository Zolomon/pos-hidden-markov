__author__ = 'bengt'

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help="Path to the corpus file.")
    parser.add_argument('word', nargs='?', help="Show word frequencies.")
    parser.add_argument('pos', nargs='?', help="Show part-of-speech frequencies.")
    args = parser.parse_args()

    if args.word:
        [print(frequency, ' ', word) for word, frequency in word_frequencies(args.corpus)]

    if args.pos:
        [print(frequency, ' ', pos) for pos, frequency in pos_frequencies(args.corpus)]


def word_frequencies(filename):
    word_freq = {}
    corpus = open(filename)
    # read file and
    # calculate word frequencies
    for line in corpus:
        line = line.replace('\n', '')
        if len(line.split('\t')) != 6:
            continue
        ID, FORM, LEMMA, PLEMMA, POS, PPOS = line.split('\t')

        if LEMMA in word_freq:
            word_freq [LEMMA] += 1
        else:
            word_freq [LEMMA] = 1

    import operator

    sorted_words = sorted(word_freq.items(), key=operator.itemgetter(1))
    return sorted_words

def pos_frequencies(filename):
    pos_freq = {}
    corpus = open(filename)
    # read file and
    # calculate pos frequencies
    for line in corpus:
        line = line.replace('\n', '')
        if len(line.split('\t')) != 6:
            continue
        ID, FORM, LEMMA, PLEMMA, POS, PPOS = line.split('\t')

        if POS in pos_freq:
            pos_freq[POS] += 1
        else:
            pos_freq[POS] = 1

    import operator

    sorted_words = sorted(pos_freq.items(), key=operator.itemgetter(1))
    return sorted_words


if __name__ == '__main__':
    main()
