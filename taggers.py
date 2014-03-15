import operator
from corpus import Corpus
import processing

__author__ = 'bengt'

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('train', help='Path to the training file.')
    parser.add_argument('corpus', help='Path to the corpus file.')

    args = parser.parse_args()

    train_corpus = Corpus(args.train)
    corpus = Corpus(args.corpus)

    pos_frequencies = processing.pos_frequencies(corpus)
    most_occuring_pos = max(pos_frequencies, key=pos_frequencies.get)
    poses_for_word, total_pos_count = processing.calculate_poses_for_word(corpus)
    mcp = get_most_common_pos_per_word(train_corpus, poses_for_word, most_occuring_pos)
    tagged_corpus = tag_predictions(corpus, mcp, most_occuring_pos)

    for line in tagged_corpus:
        print(line)


def get_most_common_pos(corpus):
    pos_count = {}
    for sentence in corpus.get_sentences():
        for word in sentence:
            ID, FORM, LEMMA, PLEMMA, POS, PPOS = word
            if POS in pos_count:
                pos_count[POS] += 1
            else:
                pos_count[POS] = 1
    return pos_count


def get_most_common_pos_per_word(training_corpus, poses_for_word, most_occuring_pos):
    # Most common part-of-speech
    mcp = {}
    for sentence in training_corpus.get_sentences():
        for word in sentence:
            ID, FORM, LEMMA, PLEMMA, POS, PPOS = word
            #FORM = FORM.lower()

            if FORM in poses_for_word:
                PPOS = max(poses_for_word[FORM].items(), key=operator.itemgetter(1))
            else:
                PPOS = most_occuring_pos
            if FORM not in mcp:
                mcp[FORM] = PPOS
            else:
                continue

    return mcp


def tag_predictions(corpus, predictions, most_occuring_pos):
    result = []
    for sentence in corpus.get_sentences():
        for word in sentence:
            ID, FORM, LEMMA, PLEMMA, POS, PPOS = word

            prediction = most_occuring_pos
            if FORM in predictions:
                prediction = predictions[FORM][0]

            result.append('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(ID, FORM, LEMMA, PLEMMA, POS, PPOS))
        result.append('\n')

    return result


if __name__ == '__main__':
    main()
