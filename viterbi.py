import argparse
import gc
import operator
from corpus import Corpus
import processing

__author__ = 'bengt'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('train', help='Path to training corpus.')
    parser.add_argument('corpus', help='Path to corpus file.')
    args = parser.parse_args()

    train_corpus = Corpus(args.train)
    corpus = Corpus(args.corpus)

    pos_frequencies = processing.pos_frequencies(corpus)
    word_pos_probabilities = processing.calculate_word_pos_probabilities(train_corpus)
    bigram_probabilities = processing.calculate_pos_bigram_probabilities(train_corpus)
    poses_for_words, total_pos_count = processing.calculate_poses_for_word(train_corpus)

    for sentence in corpus.get_sentences():
        parent_trellis = {'<s>': {'probability': 1, 'parent': None}}

        for word in sentence:
            id, form, lemma, plemma, current_word_pos, ppos = word

            if word == [0, '<s>', '<s>', '<s>', '<s>', '<s>']:
                continue

            trellis = {}

            # P(W|T)
            if form not in poses_for_words:
                most_common_pos = max(pos_frequencies.items(), key=lambda x: x[1])
                probability_pos_given_prevpos = {}
                for prev_pos in parent_trellis:
                    probability = parent_trellis[prev_pos]['probability']
                    bigram = '{0} {1}'.format(prev_pos, pos_for_word)
                    if not bigram in bigram_probabilities:
                        probability_bigram = 0.000001
                    else:
                        # P(T_i|T_i-1)
                        probability_bigram = bigram_probabilities[bigram]
                    probability *= probability_bigram
                    probability_pos_given_prevpos[prev_pos] = probability
                max_probability = max(probability_pos_given_prevpos.items(), key=lambda x: x[1])

                trellis[most_common_pos[0]] = {}
                trellis[most_common_pos[0]]['probability'] = 0.000001
                trellis[most_common_pos[0]]['parent'] = {max_probability[0]: parent_trellis[max_probability[0]]}
            else:
                for (pos_for_word, count) in poses_for_words[form].items():
                    probability_word_given_pos = word_pos_probabilities['{0} {1}'.format(form, pos_for_word)]

                    probability_pos_given_prevpos = {}
                    for prev_pos in parent_trellis:
                        probability = parent_trellis[prev_pos]['probability']
                        bigram = '{0} {1}'.format(prev_pos, pos_for_word)
                        if not bigram in bigram_probabilities:
                            probability_bigram = 0.000001
                        else:
                            # P(T_i|T_i-1)
                            probability_bigram = bigram_probabilities[bigram]
                        probability *= probability_bigram
                        probability_pos_given_prevpos[prev_pos] = probability
                    max_probability = max(probability_pos_given_prevpos.items(), key=lambda x: x[1])

                    trellis[pos_for_word] = {}
                    trellis[pos_for_word]['probability'] = probability_word_given_pos * max_probability[1]
                    trellis[pos_for_word]['parent'] = {max_probability[0]: parent_trellis[max_probability[0]]}

            parent_trellis = trellis

        optimal_path = max(trellis.items(), key=lambda x: x[1]['probability'])
        prev_path = {optimal_path[0]: optimal_path[1]}
        current_id = int(sentence[-1][0])

        while prev_path != None:
            predicted = prev_path.keys()
            if current_id == 0:
                break
            sentence[current_id][-1] = list(predicted)[0]
            prev_path = prev_path[list(predicted)[0]]['parent']
            current_id -= 1

        for word in sentence:
            id, form, lemma, plemma, pos, ppos = word
            if id == 0:
                print()
            else:
                print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(id, form, lemma, plemma, pos, ppos))


if __name__ == '__main__':
    main()
