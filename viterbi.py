import argparse
import gc
import operator
from corpus import Corpus
import processing

__author__ = 'bengt'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help='Path to corpus file.')
    args = parser.parse_args()

    corpus = Corpus(args.corpus)

    #pos_frequencies = processing.pos_frequencies(corpus)
    word_pos_probabilities = processing.calculate_word_pos_probabilities(corpus)
    bigram_probabilities = processing.calculate_pos_bigram_probabilities(corpus)
    poses_for_words, total_pos_count = processing.calculate_poses_for_word(corpus)

    new_sentences = []
    for sentence in corpus.get_sentences():
        parent_trellis = {'<s>': {'probability': 1, 'parent': None}}

        for word in sentence:
            id, form, lemma, plemma, current_word_pos, ppos = word
            form = form.lower()  # to canonical form

            trellis = {}

            # P(W|T)
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

        optimal = max(trellis.items(), key=lambda x: x[1]['probability'])
        prev_path = { optimal[0]: optimal[1] }
        current_id = int(sentence[-1][0])-1

        while prev_path != None:
            predicted = prev_path.keys()
            sentence[current_id][-1] = list(predicted)[0]
            prev_path = prev_path[list(predicted)[0]]['parent']
            current_id -= 1

        for word in sentence:
            id, form, lemma, plemma, pos, ppos = word
            # if id == 1:
            #     print()
            # else:
            print(id, '\t', form, '\t', lemma, '\t', plemma, '\t', pos, '\t', ppos)
    print()
    print()

if __name__ == '__main__':
    main()
