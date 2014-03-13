import operator

__author__ = 'bengt'

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help='Path to the corpus file.')
    parser.add_argument('--word', help='Show word frequencies.', action='store_true')
    parser.add_argument('--pos', help='Show part-of-speech frequencies.', action='store_true')
    parser.add_argument('--bigrams', help='Print bigrams', action='store_true')
    args = parser.parse_args()

    print(args)

    with open(args.corpus) as corpus_file:
        file_contentes = corpus_file.readlines()
        corpus = [line.replace('\n', '') for line in file_contentes]

        if args.word:
            [print('{0}'.format(str(frequency).rjust(12)), ' ', word) for word, frequency in word_frequencies(corpus)]

        if args.pos:
            [print('{0}'.format(str(frequency).rjust(12)), ' ', pos) for pos, frequency in pos_frequencies(corpus)]

        if args.bigrams:
            bigrams = calculate_bigrams(file_contentes)

            for (k, v) in sorted(bigrams.items(), key=operator.itemgetter(1)):
                print(v, '\t', k)


def frequencies(corpus, index, to_lower=False):
    """ Will calculate the frequency of tokens in column /index/.
    """
    frequencies = {}
    for line in corpus:
        if len(line.split('\t')) != 6:
            continue

        row = line.split('\t')
        key = row[index]
        if to_lower:
            key = key.lower()  # to canonical form

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
    return frequencies(corpus, 1, to_lower=True)


def pos_frequencies(corpus):
    """ Will calculate the frequency for each part-of-speech.
    """
    return frequencies(corpus, -2)


def parse_sentences(file_contentes):
    sentences = []
    sentence = []
    for line in file_contentes:
        if line == '\n':
            # new sentence
            sentences.append(sentence)
            sentence = []
            continue

        sentence.append(line.split('\t'))
    return sentences


def calculate_bigrams(file_contents):
    sentences = parse_sentences(file_contents)
    bigrams = {}
    for sentence in sentences:
        prev_pos = '<s>'
        for id, form, lemma, plemma, pos, ppos in sentence:
            bigram = '{0} {1}'.format(prev_pos, pos)
            if bigram in bigrams:
                bigrams[bigram] += 1
            else:
                bigrams[bigram] = 1

            prev_pos = pos
    return bigrams


if __name__ == '__main__':
    main()
