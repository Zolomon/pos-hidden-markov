#!/bin/sh
# Create results directory
RESULT_DIR="results"
mkdir -p $RESULT_DIR

echo "Applying baseline tagger ..."
python3 taggers.py data/train.set data/development.set > $RESULT_DIR/baseline.txt

echo "Evaluating the baseline results ..."
python3 evaluation.py $RESULT_DIR/baseline.txt > $RESULT_DIR/baseline_accuracy.txt

echo "Applying noisy channel model ..."
python3 noise_channel.py data/train.set data/development.set 100 > $RESULT_DIR/noisy.txt

echo "Evaluating the baseline results ..."
python3 evaluation.py $RESULT_DIR/noisy.txt > $RESULT_DIR/noisy_accuracy.txt

echo "Applying viterbi tagger ..."
python3 viterbi.py data/train.set data/development.set > $RESULT_DIR/viterbi.txt

echo "Evaluating the viterbi results ..."
python3 evaluation.py $RESULT_DIR/viterbi.txt > $RESULT_DIR/viterbi_accuracy.txt

echo "Done. Results in ${RESULT_DIR}"