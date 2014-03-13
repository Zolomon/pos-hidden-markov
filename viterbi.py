import argparse
import processing

__author__ = 'bengt'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help='Path to corpus file.')

    args = parser.parse_args()

    with open(args.corpus) as corpus:
        sentences = processing.parse_sentences(corpus)
        for sentence in sentences:


if __name__ == '__main__':
    main()
