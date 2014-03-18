from corpus import Corpus
import processing

__author__ = 'bengt'
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('train', help='Path to training corpus.')
    parser.add_argument('corpus', help='Path to corpus.')
    parser.add_argument('n', help='Tag sentences shorter than this length.')
    args = parser.parse_args()

    train_corpus = Corpus(args.train)
    corpus = Corpus(args.corpus)
    n = int(args.n)

    pos_frequencies = processing.pos_frequencies(train_corpus)
    poses_for_word_from_train, total_pos_count = processing.calculate_poses_for_word(train_corpus)
    pos_bigram_probabilities_train = processing.calculate_pos_bigram_probabilities(train_corpus)
    word_pos_probabilities_train = processing.calculate_word_pos_probabilities(train_corpus)

    sentences = [sentence for sentence in corpus.get_sentences() if len(sentence) < n]

    WORD_GIVEN_POS = 0
    POS_GIVEN_PREVPOS = 1

    for sentence in sentences:
        prev_pos = '<s>'
        columns = {}
        current_sentence = []
        for word in sentence:
            id, form, lemma, plemma, pos, ppos = word

            current_sentence.append([id, form, lemma, plemma, pos])

            columns[id] = {}
            if form in poses_for_word_from_train:
                for (pos_for_word, pos_for_word_count) in poses_for_word_from_train[form].items():
                    p_word_given_pos = word_pos_probabilities_train['{0} {1}'.format(form, pos_for_word)]

                    pos_bigram = '{0} {1}'.format(prev_pos, pos_for_word)
                    if pos_bigram in pos_bigram_probabilities_train:
                        p_pos_given_prevpos = pos_bigram_probabilities_train[pos_bigram]
                    else:
                        p_pos_given_prevpos = 0.00001 # Low chance that this is what we want

                    columns[id][pos_for_word] = {}
                    columns[id][pos_for_word][WORD_GIVEN_POS] = p_word_given_pos
                    columns[id][pos_for_word][POS_GIVEN_PREVPOS] = p_pos_given_prevpos
            else:
                most_common_pos = max(pos_frequencies.items(), key=lambda x: x[1])

                if form in word_pos_probabilities_train:
                    p_word_given_pos = word_pos_probabilities_train['{0} {1}'.format(form, most_common_pos[0])]
                else:
                    p_word_given_pos = 0.00001  # Low chance that this is what we want

                p_pos_given_prevpos = pos_bigram_probabilities_train['{0} {1}'.format(prev_pos, most_common_pos[0])]

                columns[id][most_common_pos[0]] = {}
                columns[id][most_common_pos[0]][WORD_GIVEN_POS] = p_word_given_pos
                columns[id][most_common_pos[0]][POS_GIVEN_PREVPOS] = p_pos_given_prevpos

            prev_pos = pos

        path = {}
        trellis = {}
        for (column_id, poses) in sorted(columns.items(), key=lambda x: int(x[0])):
            column_id = int(column_id)
            trellis[column_id] = {}
            for (current_pos, data) in poses.items():
                current_word_given_pos = data[WORD_GIVEN_POS]
                current_pos_given_prevpos = data[POS_GIVEN_PREVPOS]
                if column_id == 0:
                    break
                elif column_id == 1:
                    trellis[column_id][current_pos] = current_word_given_pos * current_pos_given_prevpos
                else:

                    max_prev_column = max([(id, data * current_pos_given_prevpos) for id, data in
                                           trellis[column_id - 1].items()
                                          ], key=lambda x: x[1])
                    p = max_prev_column[1] * current_word_given_pos
                    trellis[column_id][current_pos] = p

            if column_id == 0:
                continue
            else:
                path[column_id] = (max(trellis[column_id].items(), key=lambda x: x[1])[0])

        for (id, predicted) in sorted(path.items(), key=lambda x: x[0]):
            if id == 1:
                print()
            id, form, lemma, plemma, pos = current_sentence[id]
            print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(id, form, lemma, plemma, pos, predicted))


if __name__ == '__main__':
    main()