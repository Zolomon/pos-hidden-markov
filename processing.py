#!/usr/bin/python3
__author__ = 'bengt'

import operator
import argparse

print('!!!')


def calculate_poses_for_word(sentences):
    total_pos_count = {}
    poses_for_word = {}
    # For each word, find all POSes.
    for sentence in sentences:
        for word in sentence:
            id, form, lemma, plemma, pos, ppos = word
            form = form.lower()

            if pos in total_pos_count:
                total_pos_count[pos] += 1
            else:
                total_pos_count[pos] = 1

            if form in poses_for_word:
                if pos in poses_for_word[form]:
                    poses_for_word[form][pos] += 1
                else:
                    poses_for_word[form][pos] = 1
            else:
                poses_for_word[form] = {pos: 1}

    return poses_for_word, total_pos_count


def calculate_word_pos_probabilities(file_contents):
    sentences = parse_sentences(file_contents)
    poses_for_word, total_pos_count = calculate_poses_for_word(sentences)
    probabilities = {}
    for (word, poses) in poses_for_word.items():
        for (pos, count) in poses.items():
            probabilities['{0} {1}'.format(word, pos)] = count / float(total_pos_count[pos])
    return probabilities


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help='Path to the corpus file.')
    parser.add_argument('--word', help='Show word frequencies.', action='store_true')
    parser.add_argument('--pos', help='Show part-of-speech frequencies.', action='store_true')
    parser.add_argument('--bigrams', help='Print bigrams', action='store_true')
    parser.add_argument('--posprob', help='Print bigram probablities', action='store_true')
    parser.add_argument('--wordposprob', help='Probably for word given part-of-speech', action='store_true')
    args = parser.parse_args()

    with open(args.corpus) as corpus_file:
        file_contents = corpus_file.readlines()
        corpus = [line.replace('\n', '') for line in file_contents]

        if args.word:
            for word, frequency in word_frequencies(corpus):
                print('{0}'.format(str(frequency).rjust(12)), ' ', word)

        if args.pos:
            for pos, frequency in pos_frequencies(corpus):
                print('{0}'.format(str(frequency).rjust(12)), ' ', pos)

        if args.bigrams:
            bigrams = calculate_pos_bigrams(file_contents)

            for (k, v) in sorted(bigrams.items(), key=operator.itemgetter(1)):
                print(v, '\t', k)

        if args.posprob:
            bigrams = calculate_pos_bigram_probabilities(file_contents)

            bigrams = sorted(bigrams.items(), key=lambda x: x[1])

            for (bigram, probability) in bigrams:
                print('{0:>12.5f}'.format(probability), ' ', bigram)

        if args.wordposprob:
            probabilities = calculate_word_pos_probabilities(file_contents)
            probabilities = sorted(probabilities.items(), key=lambda x: x[1])

            for (word_pos, probability) in probabilities:
                print('{0:>12.5f}'.format(probability), ' ', word_pos)

def frequencies(corpus, index, to_lower=False):
    """ Will calculate the frequency of tokens in column /index/.
    :rtype : dict[str, int]
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
    :rtype : dict[str, int]
    """
    return frequencies(corpus, 1, to_lower=True)


def pos_frequencies(corpus):
    """ Will calculate the frequency for each part-of-speech.
    :rtype : dict[str, int]
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


def calculate_pos_bigrams(file_contents):
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


def calculate_pos_bigram_probabilities(file_contents):
    sentences = parse_sentences(file_contents)
    bigrams = {}

    for sentence in sentences:
        prev_pos = '<s>'
        for word in sentence:
            id, form, lemma, plemma, pos, ppos = word
            if prev_pos in bigrams:
                if pos in bigrams[prev_pos]:
                    bigrams[prev_pos][pos] += 1
                else:
                    bigrams[prev_pos][pos] = 1
            else:
                bigrams[prev_pos] = {pos: 1}
            prev_pos = pos

    total_bigrams = 0
    for (pos, next_poses) in bigrams.items():
        for (next_pos, next_pos_count) in next_poses.items():
            total_bigrams += next_pos_count

    probabilities = {}
    for (pos, next_poses) in bigrams.items():
        total_pos_count = sum(next_poses.values())
        for (next_pos, next_pos_count) in next_poses.items():
            probabilities[pos + ' ' + next_pos] = (next_pos_count / float(total_pos_count))

    return probabilities


if __name__ == '__main__':
    main()
