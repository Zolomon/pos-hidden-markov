__author__ = 'bengt'

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('train', help='Path to the training file.')
    parser.add_argument('corpus', help='Path to the corpus file.')

    args = parser.parse_args()

    training_corpus = [line.replace('\n', '') for line in open(args.train).readlines()]

    predictions, mcp = most_common_pos(training_corpus)

    print()

    corpus = [line.replace('\n', '') for line in open(args.corpus).readlines()]
    tagged_corpus = tag_predictions(corpus, predictions, mcp)

    for line in tagged_corpus:
        print(line)

def most_common_pos(training_corpus):
    # Most common part-of-speech
    pos_count = {}
    mcp = {}
    for line in training_corpus:
        if len(line.split('\t')) != 6:
            continue

        ID, FORM, LEMMA, PLEMMA, POS, PPOS = line.split('\t')
        FORM = FORM.lower()

        if POS in pos_count:
            pos_count[POS] += 1
        else:
            pos_count[POS] = 1

        if FORM in mcp:
            if POS in mcp[FORM]:
                mcp[FORM][POS] += 1
            else:
                mcp[FORM][POS] = 1
        else:
            mcp[FORM] = {}
            if POS in mcp[FORM]:
                mcp[FORM][POS] += 1
            else:
                mcp[FORM][POS] = 1

    predictions = {}
    for (form, predicted_pos) in mcp.items():
        max_pos = max(predicted_pos, key=predicted_pos.get)
        predictions[form] = max_pos

    return predictions, max(pos_count, key=pos_count.get)


def tag_predictions(corpus, predictions, most_common_pos):
    result = []
    for line in corpus:
        if len(line.split('\t')) != 6:
            result.append('')
            continue

        ID, FORM, LEMMA, PLEMMA, POS, PPOS = line.split('\t')
        FORM_lower = FORM.lower()  # to canonical form

        prediction = most_common_pos
        if FORM_lower in predictions:
            prediction = predictions[FORM_lower]

        result.append('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'\
                         .format(ID, FORM, LEMMA, PLEMMA, POS, prediction))

    return result

if __name__ == '__main__':
    main()
